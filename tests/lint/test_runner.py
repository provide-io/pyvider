#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for the protocol-neutral provider lint runner."""

from unittest.mock import patch

import pytest

from pyvider.lint import LintFinding, LintSelector
from pyvider.lint._runner import LintRunResult, run_lints


class RecordingComponent:
    """Minimal component that records lint invocations."""

    def __init__(self) -> None:
        self.calls = 0

    async def lint(self, ctx: object) -> tuple[()]:
        self.calls += 1
        return ()


INSECURE_HTTP = LintFinding(
    rule="provide-io/pyvider:insecure-http",
    groups=("provide-io/pyvider:security",),
    summary="Insecure HTTP endpoint",
    detail="Use HTTPS for the endpoint.",
    attribute_path="url",
)
LONG_TIMEOUT = LintFinding(
    rule="provide-io/pyvider:long-timeout",
    groups=("provide-io/pyvider:reliability",),
    summary="Long timeout",
    detail="Use a shorter timeout.",
)


class FindingComponent:
    async def lint(self, ctx: object) -> tuple[LintFinding, ...]:
        return (INSECURE_HTTP,)


class UnfilteredComponent:
    async def lint(self, ctx: object) -> tuple[LintFinding, ...]:
        return (INSECURE_HTTP, LONG_TIMEOUT)


class InvalidFindingComponent:
    async def lint(self, ctx: object) -> tuple[object, ...]:
        return (INSECURE_HTTP, "not a finding")


class RaisingComponent:
    async def lint(self, ctx: object) -> tuple[LintFinding, ...]:
        raise RuntimeError("lint hook crashed")


class SecretRaisingComponent:
    async def lint(self, ctx: object) -> tuple[LintFinding, ...]:
        raise RuntimeError("exception-secret")


class ExplodingDescriptorComponent:
    @property
    def lint(self) -> object:
        raise RuntimeError("descriptor lookup failed")


async def test_run_lints_disabled_selector_never_calls_hook() -> None:
    component = RecordingComponent()

    result = await run_lints(
        component,
        {"url": "https://example.test"},
        LintSelector(),
        kind="data source",
        name="example",
        operation="validate",
    )

    assert result == LintRunResult()
    assert component.calls == 0


async def test_run_lints_absent_config_never_calls_hook() -> None:
    component = RecordingComponent()

    result = await run_lints(
        component,
        None,
        LintSelector(include={"all"}),
        kind="data source",
        name="example",
        operation="validate",
    )

    assert result == LintRunResult()
    assert component.calls == 0


async def test_run_lints_selected_findings_survive() -> None:
    result = await run_lints(
        FindingComponent(),
        {"url": "http://example.test"},
        LintSelector(include={"provide-io/pyvider:security"}),
        kind="data source",
        name="example",
        operation="validate",
    )

    assert result == LintRunResult(findings=(INSECURE_HTTP,))


async def test_run_lints_defensively_refilters_returned_findings() -> None:
    result = await run_lints(
        UnfilteredComponent(),
        {"url": "http://example.test"},
        LintSelector(include={"all"}, exclude={LONG_TIMEOUT.rule}),
        kind="data source",
        name="example",
        operation="validate",
    )

    assert result == LintRunResult(findings=(INSECURE_HTTP,))


async def test_run_lints_non_finding_result_becomes_failure() -> None:
    result = await run_lints(
        InvalidFindingComponent(),
        {"url": "http://example.test"},
        LintSelector(include={"all"}),
        kind="data source",
        name="example",
        operation="validate",
    )

    assert result == LintRunResult(failed=True)


async def test_run_lints_raised_hook_becomes_failure_with_safe_context_log() -> None:
    with patch("pyvider.lint._runner.logger") as mock_logger:
        result = await run_lints(
            RaisingComponent(),
            {"password": "super-secret"},
            LintSelector(include={"all"}),
            kind="data source",
            name="example",
            operation="validate",
        )

    assert result == LintRunResult(failed=True)
    mock_logger.error.assert_called_once()
    log_call = mock_logger.error.call_args
    assert log_call.kwargs["component_kind"] == "data source"
    assert log_call.kwargs["component_name"] == "example"
    assert log_call.kwargs["operation"] == "validate"
    assert "super-secret" not in str(log_call)


async def test_run_lints_real_failure_log_does_not_leak_secrets_or_traceback(
    capfd: pytest.CaptureFixture[str],
) -> None:
    result = await run_lints(
        SecretRaisingComponent(),
        {"password": "configuration-secret"},
        LintSelector(include={"all"}),
        kind="data source",
        name="safe-name",
        operation="safe-operation",
    )

    captured = capfd.readouterr()
    rendered_log = captured.out + captured.err
    assert result == LintRunResult(failed=True)
    assert "data source" in rendered_log
    assert "safe-name" in rendered_log
    assert "safe-operation" in rendered_log
    assert "RuntimeError" in rendered_log
    assert "configuration-secret" not in rendered_log
    assert "exception-secret" not in rendered_log
    assert "Traceback" not in rendered_log


async def test_run_lints_exploding_hook_descriptor_becomes_failure() -> None:
    result = await run_lints(
        ExplodingDescriptorComponent(),
        {"url": "http://example.test"},
        LintSelector(include={"all"}),
        kind="data source",
        name="example",
        operation="validate",
    )

    assert result == LintRunResult(failed=True)


async def test_run_lints_missing_duck_typed_hook_is_noop() -> None:
    result = await run_lints(
        object(),
        {"url": "http://example.test"},
        LintSelector(include={"all"}),
        kind="data source",
        name="example",
        operation="validate",
    )

    assert result == LintRunResult()
