#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""tfprotov6 compatibility adapter for protocol-neutral lint findings."""

from provide.foundation import logger

from pyvider.hub import hub
from pyvider.lint import LintSelector
from pyvider.lint._runner import run_lints
import pyvider.protocols.tfprotov6.protobuf as pb


async def lint_diagnostics(
    component: object,
    config: object | None,
    *,
    kind: str,
    name: str,
    operation: str,
) -> list[pb.Diagnostic]:
    """Run component lints and encode their findings as warning diagnostics."""
    registered_selector = hub.get_component("singleton", "lint_selector")
    if not isinstance(registered_selector, LintSelector):
        logger.warning(
            "Provider lint selector is unavailable; linting is disabled",
            component_kind=kind,
            component_name=name,
            operation=operation,
            selector_type=type(registered_selector).__name__,
        )
        selector = LintSelector()
    else:
        selector = registered_selector

    result = await run_lints(
        component,
        config,
        selector,
        kind=kind,
        name=name,
        operation=operation,
    )
    if result.failed:
        return [
            pb.Diagnostic(
                severity=pb.Diagnostic.WARNING,
                summary="Provider linting did not complete",
                detail="The provider could not complete the requested lint checks. Review provider logs for details.",
            )
        ]

    diagnostics: list[pb.Diagnostic] = []
    for finding in result.findings:
        attribute = None
        if finding.attribute_path is not None:
            attribute = pb.AttributePath(steps=[pb.AttributePath.Step(attribute_name=finding.attribute_path)])
        diagnostics.append(
            pb.Diagnostic(
                severity=pb.Diagnostic.WARNING,
                summary=f"{finding.summary} ({finding.rule})",
                detail=finding.detail,
                attribute=attribute,
            )
        )
    return diagnostics


# 🐍🏗️🔚
