#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Provider-native linting through data-source validation."""

from collections.abc import Iterator
from typing import ClassVar
from unittest.mock import call, patch

import pytest

from pyvider.hub import hub
from pyvider.lint import LintContext, LintFinding, LintSelector
from pyvider.protocols.tfprotov6.handlers.validate_data_resource_config import (
    _validate_data_resource_config_impl,
)
import pyvider.protocols.tfprotov6.protobuf as pb

RULE = "provide-io/pyvider:insecure-http"
GROUP = "provide-io/pyvider:security"
FINDING = LintFinding(
    rule=RULE,
    groups=(GROUP,),
    summary="Insecure HTTP endpoint",
    detail="Use HTTPS for the endpoint.",
    attribute_path="url",
)


class LintingDataSource:
    lint_calls: ClassVar[int] = 0
    lint_error: ClassVar[Exception | None] = None
    validation_errors: ClassVar[list[str]] = []

    async def validate(self, config: object) -> list[str]:
        return self.validation_errors

    async def lint(self, ctx: LintContext[object]) -> tuple[LintFinding, ...]:
        type(self).lint_calls += 1
        if self.lint_error is not None:
            raise self.lint_error
        return (FINDING,)


def _unregister_if_present(component_type: str, name: str) -> None:
    if hub.get_component(component_type, name) is not None:
        hub.unregister(component_type, name)


@pytest.fixture(autouse=True)
def isolated_lint_hub() -> Iterator[None]:
    """Keep startup singleton and fake component state local to each test."""
    _unregister_if_present("singleton", "provider_context")
    _unregister_if_present("singleton", "lint_selector")
    _unregister_if_present("data_source", "lint_test")
    hub.register("data_source", "lint_test", LintingDataSource)
    LintingDataSource.lint_calls = 0
    LintingDataSource.lint_error = None
    LintingDataSource.validation_errors = []
    yield
    _unregister_if_present("singleton", "provider_context")
    _unregister_if_present("singleton", "lint_selector")
    _unregister_if_present("data_source", "lint_test")


def _request() -> pb.ValidateDataResourceConfig.Request:
    return pb.ValidateDataResourceConfig.Request(type_name="lint_test")


async def test_data_source_lint_exact_rule_maps_warning_diagnostic() -> None:
    hub.register("singleton", "lint_selector", LintSelector(include={RULE}))
    config = {"url": "http://example.test"}

    with patch(
        "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.decode_config",
        return_value=config,
    ):
        response = await _validate_data_resource_config_impl(_request(), context=None)

    assert LintingDataSource.lint_calls == 1
    assert len(response.diagnostics) == 1
    diagnostic = response.diagnostics[0]
    assert diagnostic.severity == pb.Diagnostic.WARNING
    assert diagnostic.summary == f"Insecure HTTP endpoint ({RULE})"
    assert diagnostic.detail == "Use HTTPS for the endpoint."
    assert len(diagnostic.attribute.steps) == 1
    assert diagnostic.attribute.steps[0].attribute_name == "url"


@pytest.mark.parametrize(
    ("selector", "expected_diagnostics"),
    [
        pytest.param(LintSelector(include={GROUP}), 1, id="group-enabled"),
        pytest.param(
            LintSelector(include={"all"}, exclude={RULE}),
            0,
            id="exact-excluded",
        ),
    ],
)
async def test_data_source_lint_selection(selector: LintSelector, expected_diagnostics: int) -> None:
    hub.register("singleton", "lint_selector", selector)

    with patch(
        "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.decode_config",
        return_value={"url": "http://example.test"},
    ):
        response = await _validate_data_resource_config_impl(_request(), context=None)

    assert len(response.diagnostics) == expected_diagnostics


async def test_data_source_lint_semantic_error_is_unchanged_and_skips_hook() -> None:
    hub.register("singleton", "lint_selector", LintSelector(include={"all"}))
    LintingDataSource.validation_errors = ["Existing validation error"]

    with patch(
        "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.decode_config",
        return_value={"url": "http://example.test"},
    ):
        response = await _validate_data_resource_config_impl(_request(), context=None)

    assert LintingDataSource.lint_calls == 0
    assert len(response.diagnostics) == 1
    assert response.diagnostics[0].severity == pb.Diagnostic.ERROR
    assert response.diagnostics[0].summary == "Existing validation error"


@pytest.mark.parametrize(
    ("selector", "config"),
    [
        pytest.param(LintSelector(), {"url": "http://example.test"}, id="disabled"),
        pytest.param(LintSelector(include={"all"}), None, id="unknown-config"),
    ],
)
async def test_data_source_lint_ineligible_request_skips_hook(
    selector: LintSelector, config: object | None
) -> None:
    hub.register("singleton", "lint_selector", selector)

    with patch(
        "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.decode_config",
        return_value=config,
    ):
        response = await _validate_data_resource_config_impl(_request(), context=None)

    assert LintingDataSource.lint_calls == 0
    assert list(response.diagnostics) == []


@pytest.mark.parametrize("registered_selector", [None, object()], ids=["absent", "wrong-type"])
async def test_data_source_lint_invalid_startup_selector_disables_linting(
    registered_selector: object | None,
) -> None:
    # A configured provider context must not become an alternate selector source.
    hub.register("singleton", "provider_context", LintSelector(include={"all"}))
    if registered_selector is not None:
        hub.register("singleton", "lint_selector", registered_selector)

    with (
        patch(
            "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.decode_config",
            return_value={"password": "super-secret"},
        ),
        patch("pyvider.protocols.tfprotov6.handlers._linting.logger") as mock_logger,
        patch.object(hub, "get_component", wraps=hub.get_component) as get_component,
    ):
        response = await _validate_data_resource_config_impl(_request(), context=None)

    assert LintingDataSource.lint_calls == 0
    assert list(response.diagnostics) == []
    mock_logger.warning.assert_called_once()
    assert "super-secret" not in str(mock_logger.warning.call_args)
    assert call("singleton", "provider_context") not in get_component.call_args_list


async def test_data_source_lint_hook_failure_returns_one_safe_generic_warning() -> None:
    hub.register("singleton", "lint_selector", LintSelector(include={"all"}))
    LintingDataSource.lint_error = RuntimeError("traceback super-secret")

    with patch(
        "pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.decode_config",
        return_value={"password": "super-secret"},
    ):
        response = await _validate_data_resource_config_impl(_request(), context=None)

    assert len(response.diagnostics) == 1
    diagnostic = response.diagnostics[0]
    assert diagnostic.severity == pb.Diagnostic.WARNING
    assert diagnostic.summary == "Provider linting did not complete"
    assert "traceback" not in diagnostic.detail.lower()
    assert "super-secret" not in diagnostic.detail
