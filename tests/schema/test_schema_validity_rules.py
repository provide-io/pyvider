#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Schemas Terraform will reject are rejected here, where the author can see them.

Terraform runs `Block.InternalValidate()` over every managed, data, ephemeral and
list schema as it loads a provider, and a single violation takes the whole
provider down at `terraform init`:

    provider %s has invalid schema for managed resource type %q, which is a bug
    in the provider: %q

(internal/schemarepo/loadschemas/plugins.go:134-186; the rules are in
internal/configs/configschema/internal_validate.go). None of them were checked
here, so a schema could be built, unit-tested and shipped, and fail for every
practitioner at once with an error naming the provider rather than the line that
caused it.

These are the structural rules a schema can be checked against on its own. They
are enforced where the schema is written, so a mistake fails the provider
author's own test run.
"""

from __future__ import annotations

import pytest

from pyvider.schema import (
    a_dyn,
    a_str,
    b_group,
    b_list,
    b_map,
    b_set,
    b_single,
    s_data_source,
    s_resource,
)


class TestBlockNames:
    """`^[a-z0-9_]+$`, from internal_validate.go:58."""

    def test_an_uppercase_block_name_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="block name"):
            b_single("Auth", attributes={"token": a_str()})

    def test_a_block_name_with_a_dash_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="block name"):
            b_single("my-block", attributes={"token": a_str()})

    def test_an_ordinary_block_name_is_accepted(self) -> None:
        assert b_single("auth_2", attributes={"token": a_str()}) is not None


class TestNestingItemCounts:
    """Per-mode min_items/max_items rules, internal_validate.go:64-119."""

    def test_a_negative_min_items_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="min_items"):
            b_list("cred", attributes={"token": a_str()}, min_items=-1)

    def test_a_negative_max_items_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="max_items"):
            b_list("cred", attributes={"token": a_str()}, max_items=-1)

    def test_a_list_with_min_above_max_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="min_items"):
            b_list("cred", attributes={"token": a_str()}, min_items=3, max_items=2)

    def test_a_list_with_min_below_max_is_accepted(self) -> None:
        assert b_list("cred", attributes={"token": a_str()}, min_items=1, max_items=3) is not None

    def test_a_list_with_no_maximum_is_accepted(self) -> None:
        """max_items 0 means unbounded, so a minimum above it is not a conflict."""
        assert b_list("cred", attributes={"token": a_str()}, min_items=3, max_items=0) is not None

    def test_a_single_block_requiring_two_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="single"):
            b_single("auth", attributes={"token": a_str()}, min_items=2, max_items=2)

    def test_a_single_block_with_mismatched_bounds_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="single"):
            b_single("auth", attributes={"token": a_str()}, min_items=1, max_items=0)

    def test_a_required_single_block_is_accepted(self) -> None:
        assert b_single("auth", attributes={"token": a_str()}, min_items=1, max_items=1) is not None

    def test_a_group_block_with_bounds_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="group"):
            b_group("auth", attributes={"token": a_str()}, min_items=1)

    def test_a_map_block_with_bounds_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="map"):
            b_map("zone", attributes={"token": a_str()}, max_items=3)


class TestSetBlockContents:
    """A set block's elements are matched by value, internal_validate.go:92-105."""

    def test_a_set_block_containing_a_dynamic_attribute_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="dynamic"):
            b_set("tag", attributes={"anything": a_dyn()})

    def test_a_set_block_containing_a_write_only_attribute_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="write_only"):
            b_set("tag", attributes={"secret": a_str(write_only=True)})

    def test_a_list_block_may_contain_either(self) -> None:
        """The restriction is specific to set nesting."""
        assert b_list("tag", attributes={"anything": a_dyn()}) is not None
        assert b_list("tag", attributes={"secret": a_str(write_only=True)}) is not None


class TestNameCollisions:
    """An attribute and a block cannot share a name, internal_validate.go:56."""

    def test_a_shared_name_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="auth"):
            s_resource(
                attributes={"auth": a_str()},
                block_types=[b_single("auth", attributes={"token": a_str()})],
            )

    def test_distinct_names_are_accepted(self) -> None:
        assert (
            s_resource(
                attributes={"name": a_str(required=True)},
                block_types=[b_single("auth", attributes={"token": a_str()})],
            )
            is not None
        )


class TestWriteOnlyPlacement:
    """Write-only is a managed-resource concept.

    terraform-plugin-sdk rejects it on provider and data source schemas
    (helper/schema/provider.go:202,208,242); Terraform's own write-only checks
    only ever run against managed resources.
    """

    def test_a_write_only_data_source_attribute_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="write_only"):
            s_data_source({"secret": a_str(write_only=True)})

    def test_a_write_only_resource_attribute_is_accepted(self) -> None:
        assert s_resource({"secret": a_str(write_only=True)}) is not None


# 🐍🏗️🔚


class TestIdentityAttributeTypes:
    """Core rejects a map, set or object in identity and accepts the rest.

    schemarepo/loadschemas/plugins.go:150-161; terraform-plugin-go documents the
    accepted set as bool, number, string and a list of those
    (tfprotov6/resource_identity_schema.go:63-72).
    """

    def test_a_list_of_strings_is_accepted(self) -> None:
        """This was rejected, which is stricter than Terraform for no reason."""
        from pyvider.conversion.schema_adapter import pvs_identity_schema_to_proto
        from pyvider.schema import a_list, s_identity

        proto = pvs_identity_schema_to_proto(s_identity({"path": a_list(a_str(), required=True)}))

        assert [attr.name for attr in proto.identity_attributes] == ["path"]

    def test_a_scalar_is_still_accepted(self) -> None:
        from pyvider.conversion.schema_adapter import pvs_identity_schema_to_proto
        from pyvider.schema import s_identity

        proto = pvs_identity_schema_to_proto(s_identity({"id": a_str(required=True)}))

        assert [attr.name for attr in proto.identity_attributes] == ["id"]

    def test_a_map_is_still_rejected(self) -> None:
        from pyvider.conversion.schema_adapter import pvs_identity_schema_to_proto
        from pyvider.schema import a_map, s_identity
        from pyvider.schema.exceptions import PvsSchemaDefinitionError

        with pytest.raises(PvsSchemaDefinitionError, match="identity"):
            pvs_identity_schema_to_proto(s_identity({"tags": a_map(a_str(), required=True)}))
