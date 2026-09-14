#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Protocol-neutral execution of provider component lint hooks."""

from attrs import define
from provide.foundation import logger

from pyvider.lint import LintContext, LintFinding, LintSelector


@define(frozen=True, slots=True)
class LintRunResult:
    """Findings and failure state from one lint-hook invocation."""

    findings: tuple[LintFinding, ...] = ()
    failed: bool = False


async def run_lints(
    component: object,
    config: object | None,
    selector: LintSelector,
    *,
    kind: str,
    name: str,
    operation: str,
) -> LintRunResult:
    """Run enabled component lints without exposing protocol concerns."""
    if config is None or selector.is_disabled:
        return LintRunResult()
    lint = getattr(component, "lint", None)
    if lint is None:
        return LintRunResult()
    try:
        findings = tuple(await lint(LintContext(config, selector)))
        if not all(isinstance(finding, LintFinding) for finding in findings):
            raise TypeError("lint() must return only LintFinding values")
        return LintRunResult(
            findings=tuple(finding for finding in findings if selector.enabled(finding.rule, *finding.groups))
        )
    except Exception as exc:
        logger.error(
            "Provider linting failed",
            component_kind=kind,
            component_name=name,
            operation=operation,
            error_type=type(exc).__name__,
            exc_info=True,
        )
        return LintRunResult(failed=True)


# 🐍🏗️🔚
