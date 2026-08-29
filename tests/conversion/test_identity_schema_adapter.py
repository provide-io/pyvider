#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for identity schema to protobuf conversion."""

import pytest

from pyvider.conversion import pvs_identity_schema_to_proto
from pyvider.schema import PvsSchema, a_list, a_str, b_list, s_identity
from pyvider.schema.exceptions import PvsSchemaDefinitionError
from pyvider.schema.types import PvsObjectType


def test_maps_required_to_required_for_import() -> None:
    proto = pvs_identity_schema_to_proto(s_identity(attributes={"path": a_str(required=True)}))

    assert len(proto.identity_attributes) == 1
    attr = proto.identity_attributes[0]
    assert attr.name == "path"
    assert attr.required_for_import is True
    assert attr.optional_for_import is False


def test_maps_optional_to_optional_for_import() -> None:
    proto = pvs_identity_schema_to_proto(s_identity(attributes={"region": a_str(optional=True)}))

    attr = proto.identity_attributes[0]
    assert attr.required_for_import is False
    assert attr.optional_for_import is True


def test_carries_version_and_description() -> None:
    schema = s_identity(
        attributes={"path": a_str("The absolute path.", required=True)},
        version=2,
    )
    proto = pvs_identity_schema_to_proto(schema)

    assert proto.version == 2
    assert proto.identity_attributes[0].description == "The absolute path."


def test_encodes_attribute_type_as_wire_json() -> None:
    proto = pvs_identity_schema_to_proto(s_identity(attributes={"path": a_str(required=True)}))

    assert proto.identity_attributes[0].type == b'"string"'


def test_rejects_nested_blocks() -> None:
    schema = PvsSchema(
        version=1,
        block=PvsObjectType(
            attributes={"path": a_str(required=True)},
            block_types=(b_list("nested"),),
        ),
    )

    with pytest.raises(PvsSchemaDefinitionError, match="nested blocks"):
        pvs_identity_schema_to_proto(schema)


def test_rejects_non_scalar_attribute_type() -> None:
    schema = s_identity(attributes={"tags": a_list(a_str(), required=True)})

    with pytest.raises(PvsSchemaDefinitionError, match="scalar"):
        pvs_identity_schema_to_proto(schema)


def test_rejects_computed_attribute() -> None:
    """computed would be folded into to_cty_type()'s optional set."""
    schema = s_identity(attributes={"path": a_str(computed=True)})

    with pytest.raises(PvsSchemaDefinitionError, match="computed"):
        pvs_identity_schema_to_proto(schema)


def test_rejects_sensitive_attribute() -> None:
    schema = s_identity(attributes={"path": a_str(required=True, sensitive=True)})

    with pytest.raises(PvsSchemaDefinitionError, match="sensitive"):
        pvs_identity_schema_to_proto(schema)


def test_rejects_defaulted_attribute_by_name() -> None:
    """A default implies computed, so the refusal must name what was written.

    `PvsAttribute` marks any defaulted attribute Computed, which the computed
    refusal above would otherwise report -- naming a flag that never appears in
    the practitioner's source.
    """
    schema = s_identity(attributes={"region": a_str(default="us-east-1")})

    with pytest.raises(PvsSchemaDefinitionError, match="default") as excinfo:
        pvs_identity_schema_to_proto(schema)

    assert "computed" not in str(excinfo.value)


def test_preserves_attribute_order() -> None:
    schema = s_identity(
        attributes={
            "region": a_str(required=True),
            "name": a_str(required=True),
        }
    )
    proto = pvs_identity_schema_to_proto(schema)

    assert [a.name for a in proto.identity_attributes] == ["region", "name"]


# 🐍🏗️🔚
