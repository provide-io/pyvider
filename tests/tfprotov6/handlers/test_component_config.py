#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

import attrs
import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.cty.exceptions import CtyValidationError
from pyvider.protocols.tfprotov6.handlers._component_config import (
    config_to_attrs_instance,
    decode_config,
    unmarshal_config,
)
from pyvider.schema import PvsSchema, a_str, s_resource


@attrs.define
class Config:
    value: str | None = "class-default"


class Component:
    config_class = Config

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(attributes={"value": a_str(default="schema-default")})


def test_decode_config_resolves_schema_and_class_defaults_together() -> None:
    schema = Component.get_schema()
    wire_config = marshal({"value": None}, schema=schema.block)

    config = decode_config(Component, wire_config)

    assert config == Config(value="schema-default")


def test_unmarshal_config_applies_schema_defaults() -> None:
    schema = Component.get_schema()
    wire_config = marshal({"value": None}, schema=schema.block)

    config = unmarshal_config(wire_config, schema.block)

    assert config.value["value"].value == "schema-default"


def test_config_to_attrs_instance_applies_class_defaults() -> None:
    schema = Component.get_schema()
    wire_config = marshal({"value": None}, schema=schema.block)
    unresolved_config = unmarshal(wire_config, schema=schema.block)

    config = config_to_attrs_instance(unresolved_config, Config)

    assert config == Config(value="class-default")


def test_decode_config_can_enforce_schema_validation() -> None:
    class RequiredComponent(Component):
        @classmethod
        def get_schema(cls) -> PvsSchema:
            return s_resource(attributes={"value": a_str(required=True)})

    schema = RequiredComponent.get_schema()
    wire_config = marshal({"value": None}, schema=schema.block)

    with pytest.raises(CtyValidationError, match="cannot be null"):
        decode_config(RequiredComponent, wire_config, validate=True)
