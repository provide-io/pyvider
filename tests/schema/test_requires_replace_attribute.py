#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for the requires_replace flag on schema attributes."""

import pytest

from pyvider.conversion.schema_adapter import _pvs_attribute_to_proto
from pyvider.schema import a_obj, a_str, b_list, b_set, b_single, s_resource


class TestRequiresReplaceFlag:
    def test_defaults_to_false(self) -> None:
        assert a_str().requires_replace is False

    def test_can_be_set_on_a_required_attribute(self) -> None:
        assert a_str(required=True, requires_replace=True).requires_replace is True

    def test_can_be_set_on_an_optional_computed_attribute(self) -> None:
        """Optional+computed is practitioner-settable, so replacement is meaningful."""
        attr = a_str(optional=True, computed=True, requires_replace=True)

        assert attr.requires_replace is True

    def test_rejected_on_a_computed_only_attribute(self) -> None:
        with pytest.raises(ValueError, match="requires_replace cannot be set on a computed-only"):
            a_str(computed=True, requires_replace=True)

    def test_rejected_on_a_write_only_attribute(self) -> None:
        """Write-only values are null in prior and planned state, so a diff can never appear."""
        with pytest.raises(ValueError, match="requires_replace cannot be set on a write-only"):
            a_str(required=True, write_only=True, requires_replace=True)

    def test_rejected_on_a_write_only_attribute_inside_a_schema(self) -> None:
        """b_main re-creates attributes, so the rejection must also fire during schema build."""
        with pytest.raises(ValueError, match="requires_replace cannot be set on a write-only"):
            s_resource({"password": a_str(optional=True, write_only=True, requires_replace=True)})

    def test_write_only_alone_is_allowed(self) -> None:
        assert a_str(optional=True, write_only=True).write_only is True

    def test_requires_replace_alone_is_allowed(self) -> None:
        assert a_str(optional=True, requires_replace=True).requires_replace is True

    def test_survives_schema_construction(self) -> None:
        """b_main re-creates each attribute to stamp its name; the flag must ride along."""
        schema = s_resource({"name": a_str(required=True, requires_replace=True)})

        assert schema.block.attributes["name"].requires_replace is True

    def test_is_not_sent_over_the_wire(self) -> None:
        """tfplugin6 has no schema-level replacement field; it is a plan-response concern."""
        proto = _pvs_attribute_to_proto(a_str(name="name", required=True, requires_replace=True))

        assert not any(f.name == "requires_replace" for f, _ in proto.ListFields())


class TestRequiresReplaceInsideNesting:
    """Replacement paths are flat and top-level, so nesting makes the flag unreachable."""

    def test_rejected_inside_a_list_block(self) -> None:
        with pytest.raises(ValueError, match="requires_replace cannot be set on an attribute inside"):
            b_list("disk", attributes={"size": a_str(required=True, requires_replace=True)})

    def test_rejected_inside_a_set_block(self) -> None:
        with pytest.raises(ValueError, match="requires_replace cannot be set on an attribute inside"):
            b_set("disk", attributes={"size": a_str(required=True, requires_replace=True)})

    def test_rejected_inside_a_single_block(self) -> None:
        with pytest.raises(ValueError, match="requires_replace cannot be set on an attribute inside"):
            b_single("disk", attributes={"size": a_str(required=True, requires_replace=True)})

    def test_rejected_inside_a_doubly_nested_block(self) -> None:
        """The inner block validates itself before the outer one is built."""
        with pytest.raises(ValueError, match="requires_replace cannot be set on an attribute inside"):
            b_list(
                "outer",
                attributes={"name": a_str(required=True)},
                block_types=[
                    b_list("inner", attributes={"size": a_str(required=True, requires_replace=True)})
                ],
            )

    def test_error_names_the_offending_path(self) -> None:
        with pytest.raises(ValueError) as excinfo:
            b_list("disk", attributes={"size": a_str(required=True, requires_replace=True)})

        message = str(excinfo.value)
        assert "disk.size" in message
        assert "ctx.require_replace('disk.size')" in message

    def test_block_without_the_flag_is_allowed(self) -> None:
        block = b_list("disk", attributes={"size": a_str(required=True)})

        assert block.type_name == "disk"

    def test_rejected_inside_an_object_attribute(self) -> None:
        with pytest.raises(ValueError, match="requires_replace cannot be set on an attribute nested inside"):
            a_obj({"size": a_str(required=True, requires_replace=True)})

    def test_object_error_reads_correctly_without_an_outer_name(self) -> None:
        """`a_obj()` is built before the builder that names it, so `name` is still empty."""
        with pytest.raises(ValueError) as excinfo:
            a_obj({"size": a_str(required=True, requires_replace=True)})

        message = str(excinfo.value)
        assert "nested attribute 'size'" in message
        assert "for '':" not in message
        assert "'.size'" not in message
        assert "ctx.require_replace('.size')" not in message
        assert "ctx.require_replace('<object>.size')" in message

    def test_object_error_uses_the_outer_name_when_it_is_known(self) -> None:
        with pytest.raises(ValueError) as excinfo:
            a_obj({"size": a_str(required=True, requires_replace=True)}, name="cfg")

        message = str(excinfo.value)
        assert "nested attribute 'cfg.size'" in message
        assert "ctx.require_replace('cfg.size')." in message

    def test_object_attribute_may_itself_require_replace(self) -> None:
        """The object is a top-level attribute, so its own path is addressable."""
        attr = a_obj({"size": a_str(required=True)}, required=True, requires_replace=True)

        assert attr.requires_replace is True

    def test_schema_with_a_clean_block_still_builds(self) -> None:
        schema = s_resource(
            {"name": a_str(required=True, requires_replace=True)},
            block_types=[b_list("disk", attributes={"size": a_str(required=True)})],
        )

        assert schema.block.attributes["name"].requires_replace is True


# 🐍🏗️🔚
