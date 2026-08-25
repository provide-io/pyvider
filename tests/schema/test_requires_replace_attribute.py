#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for the requires_replace flag on schema attributes."""

import pytest

from pyvider.conversion.schema_adapter import _pvs_attribute_to_proto
from pyvider.schema import a_str, s_resource


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

    def test_survives_schema_construction(self) -> None:
        """b_main re-creates each attribute to stamp its name; the flag must ride along."""
        schema = s_resource({"name": a_str(required=True, requires_replace=True)})

        assert schema.block.attributes["name"].requires_replace is True

    def test_is_not_sent_over_the_wire(self) -> None:
        """tfplugin6 has no schema-level replacement field; it is a plan-response concern."""
        proto = _pvs_attribute_to_proto(a_str(name="name", required=True, requires_replace=True))

        assert not any(f.name == "requires_replace" for f, _ in proto.ListFields())


# 🐍🏗️🔚
