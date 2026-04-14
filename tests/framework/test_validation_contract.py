#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any

import attrs
import pytest
from pytest_mock import MockerFixture

from pyvider.common.types import StateType
from pyvider.conversion import marshal
from pyvider.data_sources.base import BaseDataSource
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers import (
    ValidateResourceConfigHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_str, s_data_source, s_resource


@attrs.define(frozen=True)
class ValidationConfig:
    name: str


class IncompleteResource(BaseResource):
    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({})


@attrs.define
class ValidatableResource(BaseResource[Any, Any, ValidationConfig]):
    config_class = ValidationConfig
    state_class = ValidationConfig

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({"name": a_str()})

    async def _validate_config(self, config: ValidationConfig) -> list[str]:
        if config.name == "invalid":
            return ["Name cannot be 'invalid'."]
        return []

    async def read(self, ctx: ResourceContext) -> StateType | None:
        return None

    async def _create(
        self, ctx: ResourceContext, base_plan: dict[str, Any]
    ) -> tuple[dict[str, Any] | None, None]:
        return None, None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        pass


@attrs.define
class ValidatableDataSource(BaseDataSource[Any, Any, ValidationConfig]):
    config_class = ValidationConfig
    state_class = ValidationConfig

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source({"name": a_str()})

    async def _validate_config(self, config: ValidationConfig) -> list[str]:
        if config.name == "invalid-ds":
            return ["Data source name cannot be 'invalid-ds'."]
        return []

    async def read(self, ctx: ResourceContext) -> StateType | None:
        return None


class TestValidationContract:
    def test_subclass_must_implement_all_abstract_methods(self) -> None:
        with pytest.raises(TypeError, match="Can't instantiate abstract class IncompleteResource"):
            IncompleteResource()

    @pytest.mark.asyncio
    async def test_validate_calls_and_returns_from_validate_config(self, mocker: MockerFixture) -> None:
        resource = ValidatableResource()
        spy = mocker.spy(resource, "_validate_config")
        valid_config = ValidationConfig(name="valid")
        errors = await resource.validate(valid_config)
        assert errors == []
        spy.assert_called_once_with(valid_config)
        spy.reset_mock()
        invalid_config = ValidationConfig(name="invalid")
        errors = await resource.validate(invalid_config)
        assert errors == ["Name cannot be 'invalid'."]
        spy.assert_called_once_with(invalid_config)

    @pytest.mark.asyncio
    async def test_validate_handles_none_config_gracefully(self, mocker: MockerFixture) -> None:
        resource = ValidatableResource()
        spy = mocker.spy(resource, "_validate_config")
        errors = await resource.validate(None)
        assert errors == []
        spy.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("discovered_components_session")
    async def test_resource_handler_uses_validation_contract(self) -> None:
        resource_name = "validatable_resource_for_handler"
        hub.register("resource", resource_name, ValidatableResource)
        try:
            schema = ValidatableResource.get_schema()
            raw_config = {"name": "invalid"}
            config_dv = marshal(raw_config, schema=schema.block)
            request = pb.ValidateResourceConfig.Request(type_name=resource_name, config=config_dv)
            response = await ValidateResourceConfigHandler(request, context=None)
            assert len(response.diagnostics) == 1
            diag = response.diagnostics[0]
            assert diag.severity == pb.Diagnostic.ERROR
            assert diag.summary == "Name cannot be 'invalid'."
        finally:
            hub.unregister("resource", resource_name)


# 🐍🏗️🔚
