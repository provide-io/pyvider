#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Shared lint contract for every configuration-validation RPC."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, ClassVar
from unittest.mock import patch

import attrs
import pytest

from pyvider.conversion import marshal
from pyvider.hub import hub
from pyvider.lint import LintContext, LintFinding, LintSelector
from pyvider.protocols.tfprotov6.handlers.action_handlers import ValidateActionConfigHandler
from pyvider.protocols.tfprotov6.handlers.config_handlers import ValidateListResourceConfigHandler
from pyvider.protocols.tfprotov6.handlers.state_store_handlers import ValidateStateStoreConfigHandler
from pyvider.protocols.tfprotov6.handlers.validate_data_resource_config import (
    _validate_data_resource_config_impl,
)
from pyvider.protocols.tfprotov6.handlers.validate_ephemeral_resource_config import (
    _validate_ephemeral_resource_config_impl,
)
from pyvider.protocols.tfprotov6.handlers.validate_provider_config import (
    _validate_provider_config_impl,
)
from pyvider.protocols.tfprotov6.handlers.validate_resource_config import (
    _validate_resource_config_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.schema import PvsSchema, a_str, s_data_source, s_provider, s_resource

TYPE_NAME = "lint_contract"
RULE = "provide-io/pyvider:contract-rule"
GROUP = "provide-io/pyvider:contract-group"
FINDING = LintFinding(
    rule=RULE,
    groups=(GROUP,),
    summary="Contract lint finding",
    detail="Change this test value.",
    attribute_path="url",
)


@attrs.define
class LintConfig:
    url: str


@dataclass(frozen=True)
class HandlerCase:
    name: str
    component_type: str | None
    schema: PvsSchema


PROVIDER = HandlerCase("provider", None, s_provider(attributes={"url": a_str(required=True)}))
RESOURCE = HandlerCase("resource", "resource", s_resource(attributes={"url": a_str(required=True)}))
DATA_SOURCE = HandlerCase(
    "data-source", "data_source", s_data_source(attributes={"url": a_str(required=True)})
)
EPHEMERAL_RESOURCE = HandlerCase(
    "ephemeral-resource", "ephemeral_resource", s_resource(attributes={"url": a_str(required=True)})
)
LIST_RESOURCE = HandlerCase(
    "list-resource", "list_resource", s_resource(attributes={"url": a_str(required=True)})
)
ACTION = HandlerCase("action", "action", s_resource(attributes={"url": a_str(required=True)}))
STATE_STORE = HandlerCase("state-store", "state_store", s_resource(attributes={"url": a_str(required=True)}))


def _component(case: HandlerCase, *, with_lint: bool = True) -> type[Any]:
    class ContractComponent:
        config_class = LintConfig
        schema = case.schema
        validation_errors: ClassVar[list[str]] = []
        lint_contexts: ClassVar[list[LintContext[Any]]] = []

        @classmethod
        def get_schema(cls) -> PvsSchema:
            return case.schema

        async def validate(self, config: object | None) -> list[str]:
            return list(type(self).validation_errors)

    if with_lint:

        async def lint(self: object, ctx: LintContext[Any]) -> tuple[LintFinding, ...]:
            ContractComponent.lint_contexts.append(ctx)
            return (FINDING,)

        ContractComponent.lint = lint  # type: ignore[attr-defined]

    return ContractComponent


def _config(case: HandlerCase, *, valid: bool = True) -> pb.DynamicValue:
    return marshal({"url": "http://example.test" if valid else None}, schema=case.schema.block)


def _unregister_if_present(component_type: str, name: str) -> None:
    if hub.get_component(component_type, name) is not None:
        hub.unregister(component_type, name)


@contextmanager
def _isolated_hub(case: HandlerCase, component: type[Any]) -> Iterator[None]:
    keys = [("singleton", "provider_context"), ("singleton", "lint_selector")]
    if case.component_type is None:
        keys.append(("singleton", "provider"))
    else:
        keys.append((case.component_type, TYPE_NAME))
    previous = {key: hub.get_component(*key) for key in keys}
    try:
        for component_type, name in keys:
            _unregister_if_present(component_type, name)
        if case.component_type is None:
            hub.register("singleton", "provider", component())
        else:
            hub.register(case.component_type, TYPE_NAME, component)
        yield
    finally:
        for component_type, name in keys:
            _unregister_if_present(component_type, name)
        for (component_type, name), value in previous.items():
            if value is not None:
                hub.register(component_type, name, value)


def _set_selector(selector: LintSelector) -> None:
    _unregister_if_present("singleton", "lint_selector")
    hub.register("singleton", "lint_selector", selector)


async def _invoke(
    case: HandlerCase,
    component: type[Any],
    *,
    valid_config: bool = True,
) -> Any:
    config = _config(case, valid=valid_config)
    if case.name == "provider":
        request = pb.ValidateProviderConfig.Request(config=config)
        return await _validate_provider_config_impl(request, context=None)
    if case.name == "resource":
        request = pb.ValidateResourceConfig.Request(type_name=TYPE_NAME, config=config)
        return await _validate_resource_config_impl(request, context=None)
    if case.name == "data-source":
        request = pb.ValidateDataResourceConfig.Request(type_name=TYPE_NAME, config=config)
        return await _validate_data_resource_config_impl(request, context=None)
    if case.name == "ephemeral-resource":
        request = pb.ValidateEphemeralResourceConfig.Request(type_name=TYPE_NAME, config=config)
        return await _validate_ephemeral_resource_config_impl(request, context=None)
    if case.name == "list-resource":
        request = pb.ValidateListResourceConfig.Request(type_name=TYPE_NAME, config=config)
        return await ValidateListResourceConfigHandler(request, context=None)
    if case.name == "action":
        request = pb.ValidateActionConfig.Request(type_name=TYPE_NAME, config=config)
        return await ValidateActionConfigHandler(request, context=None)
    request = pb.ValidateStateStore.Request(type_name=TYPE_NAME, config=config)
    with patch(
        "pyvider.protocols.tfprotov6.handlers.state_store_handlers._backend",
        return_value=component(),
    ):
        return await ValidateStateStoreConfigHandler(request, context=None)


def _assert_warning(response: Any) -> None:
    assert len(response.diagnostics) == 1
    diagnostic = response.diagnostics[0]
    assert diagnostic.severity == pb.Diagnostic.WARNING
    assert diagnostic.summary == f"Contract lint finding ({RULE})"
    assert diagnostic.detail == "Change this test value."
    assert len(diagnostic.attribute.steps) == 1
    assert diagnostic.attribute.steps[0].attribute_name == "url"


@pytest.mark.parametrize(
    "case",
    [
        pytest.param(PROVIDER, id="provider"),
        pytest.param(RESOURCE, id="resource"),
        pytest.param(DATA_SOURCE, id="data_source"),
        pytest.param(EPHEMERAL_RESOURCE, id="ephemeral"),
        pytest.param(LIST_RESOURCE, id="list"),
        pytest.param(ACTION, id="action"),
        pytest.param(STATE_STORE, id="state_store"),
    ],
)
async def test_handler_lint_contract(case: HandlerCase) -> None:
    component = _component(case)
    with _isolated_hub(case, component):
        assert hub.get_component("singleton", "provider_context") is None

        _set_selector(LintSelector(include={RULE}))
        response = await _invoke(case, component)
        _assert_warning(response)
        assert len(component.lint_contexts) == 1
        assert isinstance(component.lint_contexts[0].config, LintConfig)
        assert component.lint_contexts[0].config.url == "http://example.test"

        component.lint_contexts = []
        _set_selector(LintSelector())
        response = await _invoke(case, component)
        assert list(response.diagnostics) == []
        assert component.lint_contexts == []

        component.lint_contexts = []
        _set_selector(LintSelector(include={RULE}))
        if case.name == "provider":
            response = await _invoke(case, component, valid_config=False)
        else:
            component.validation_errors = ["Existing semantic error"]
            response = await _invoke(case, component)
        assert component.lint_contexts == []
        assert len(response.diagnostics) == 1
        assert response.diagnostics[0].severity == pb.Diagnostic.ERROR

        component.validation_errors = []
        _set_selector(LintSelector(include={GROUP}))
        response = await _invoke(case, component)
        _assert_warning(response)

        component.lint_contexts = []
        _set_selector(LintSelector(include={"all"}, exclude={RULE}))
        response = await _invoke(case, component)
        assert list(response.diagnostics) == []
        assert len(component.lint_contexts) == 1


@pytest.mark.parametrize(
    "case",
    [
        pytest.param(PROVIDER, id="provider"),
        pytest.param(RESOURCE, id="resource"),
        pytest.param(DATA_SOURCE, id="data_source"),
        pytest.param(EPHEMERAL_RESOURCE, id="ephemeral"),
        pytest.param(LIST_RESOURCE, id="list"),
        pytest.param(ACTION, id="action"),
        pytest.param(STATE_STORE, id="state_store"),
    ],
)
async def test_validation_handler_accepts_duck_typed_component_without_lint(case: HandlerCase) -> None:
    component = _component(case, with_lint=False)
    with _isolated_hub(case, component):
        _set_selector(LintSelector(include={"all"}))

        response = await _invoke(case, component)

    assert list(response.diagnostics) == []
