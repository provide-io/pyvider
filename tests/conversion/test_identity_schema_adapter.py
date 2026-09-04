#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for identity schema to protobuf conversion."""

import asyncio

import pytest

from pyvider.conversion import pvs_identity_schema_to_proto
import pyvider.protocols.tfprotov6.protobuf as pb
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


def test_accepts_a_list_of_scalars() -> None:
    """Terraform allows it, and this used to be stricter than Terraform.

    Core rejects a map, a set and an object in an identity schema and accepts
    everything else (schemarepo/loadschemas/plugins.go:150-161);
    terraform-plugin-go documents the accepted set as bool, number, string and a
    list of those (tfprotov6/resource_identity_schema.go:63-72). Refusing a list
    ruled out an ordinary composite identity for no protocol reason.
    """
    schema = s_identity(attributes={"path": a_list(a_str(), required=True)})

    proto = pvs_identity_schema_to_proto(schema)

    assert [attr.name for attr in proto.identity_attributes] == ["path"]


def test_rejects_a_map_attribute_type() -> None:
    """A map is one of the three shapes Terraform genuinely refuses."""
    from pyvider.schema import a_map

    schema = s_identity(attributes={"tags": a_map(a_str(), required=True)})

    with pytest.raises(PvsSchemaDefinitionError, match="identity"):
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


def test_a_markdown_description_is_published_as_markdown() -> None:
    """`description_kind` was carried on the attribute and dropped on the wire.

    Terraform renders a description as Markdown only when told to; anything
    other than MARKDOWN is mapped to plain (plugin6/convert/schema.go:234-241).
    So a description written as Markdown was published as plain text, and the
    registry showed the raw markup.
    """
    from pyvider.conversion.schema_adapter import pvs_schema_to_proto
    from pyvider.schema import s_resource
    from pyvider.schema.types import StringKind

    schema = s_resource(
        {"name": a_str(required=True, description="**bold**", description_kind=StringKind.MARKDOWN)}
    )

    proto = asyncio.run(pvs_schema_to_proto(schema))

    attribute = next(a for a in proto.block.attributes if a.name == "name")
    assert attribute.description_kind == pb.StringKind.MARKDOWN


def test_a_plain_description_stays_plain() -> None:
    from pyvider.conversion.schema_adapter import pvs_schema_to_proto
    from pyvider.schema import s_resource

    proto = asyncio.run(pvs_schema_to_proto(s_resource({"name": a_str(required=True, description="plain")})))

    attribute = next(a for a in proto.block.attributes if a.name == "name")
    assert attribute.description_kind == pb.StringKind.PLAIN


def test_a_json_dynamic_value_is_decoded() -> None:
    """Terraform accepts either encoding in a response, so this must read both.

    Core decodes whichever of msgpack or json is present
    (internal/plugin6/grpc_provider.go:2078-2093). Terraform encodes msgpack
    itself, so this is the path a differently-built client takes and the one raw
    state arrives on; it used to raise NotImplementedError.
    """
    from pyvider.conversion import unmarshal
    from pyvider.schema import s_resource

    block = s_resource({"name": a_str(required=True)}).block
    value = unmarshal(pb.DynamicValue(json=b'{"name": "alpha"}'), schema=block)

    assert value["name"].value == "alpha"
