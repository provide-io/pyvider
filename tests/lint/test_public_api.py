#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Public API and author-documentation contract for provider linting."""

from pathlib import Path

import pytest
import yaml

DOC_PATH = Path(__file__).parents[2] / "docs" / "core-concepts" / "provider-linting.md"
MKDOCS_PATH = Path(__file__).parents[2] / "mkdocs.yml"
AUTHOR_EXAMPLE = """async def lint(self, ctx: LintContext[HTTPAPIConfig]) -> Sequence[LintFinding]:
    rule = "example/acme:insecure-http"
    groups = ("example/acme:all", "example/acme:security")
    if not ctx.enabled(rule, *groups) or not ctx.config.url.startswith("http://"):
        return ()
    return (LintFinding(rule, groups, "Insecure HTTP endpoint",
            "Use HTTPS or suppress this rule when plaintext is intentional.", "url"),)"""


def test_lint_public_api_exports_are_explicit() -> None:
    from pyvider import lint
    from pyvider.lint import LintContext, LintFinding, LintSelector

    assert lint.__all__ == ["LintContext", "LintFinding", "LintSelector"]
    assert lint.LintContext is LintContext
    assert lint.LintFinding is LintFinding
    assert lint.LintSelector is LintSelector


def test_provider_linting_documentation_exists() -> None:
    assert DOC_PATH.is_file()


def test_provider_linting_documentation_has_exact_author_example() -> None:
    assert AUTHOR_EXAMPLE in DOC_PATH.read_text(encoding="utf-8")


def test_provider_linting_documentation_describes_supported_author_api() -> None:
    expected = "`LintFinding`, `LintSelector`, and `LintContext` are supported public APIs"
    assert expected in DOC_PATH.read_text(encoding="utf-8")


def test_provider_linting_documentation_covers_configuration_precedence() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")
    expected = (
        "[lint]",
        'rules = ["example/acme:all", "!example/acme:insecure-http"]',
        "PYVIDER_LINT='example/acme:security,!example/acme:insecure-http'",
        "PYVIDER_LINT=''",
        "PYVIDER_LINT > [lint].rules > disabled",
    )
    assert all(value in content for value in expected)


def test_provider_linting_documentation_covers_selector_grammar_and_precedence() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")
    expected = (
        "^([a-z0-9]+[a-z0-9_\\-/]*:)?[a-z0-9]+[a-z0-9_\\-]*$",
        "Exact rule inclusion",
        "Exact rule exclusion",
        "Any included group",
        "Any excluded group",
        "Global `all`",
        "inclusion wins",
    )
    assert all(value in content for value in expected)


def test_provider_linting_documentation_distinguishes_diagnostic_kinds() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")
    expected = ("Validation error", "Deprecation", "Ordinary warning", "Lint finding")
    assert all(value in content for value in expected)


def test_provider_linting_documentation_gives_unknown_safe_guidance() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")
    expected = ("unknown-safe", "emit no finding", "side-effect free", "ctx.enabled")
    assert all(value in content for value in expected)


def test_provider_linting_documentation_describes_fail_open_behavior() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")
    expected = ("fail-open", "Provider linting did not complete", "remains valid")
    assert all(value in content for value in expected)


def test_provider_linting_documentation_describes_compatibility_boundary() -> None:
    content = " ".join(DOC_PATH.read_text(encoding="utf-8").split())
    expected = (
        "built-in linter remains experimental",
        "temporary compatibility bridge",
        "tfprotov6 has no provider-lint wire message",
        "cannot carry provider selection hints",
    )
    assert all(value in content for value in expected)


def test_provider_linting_documentation_promises_transport_only_migration() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")
    expected = ("native transport", "`lint()` hooks", "rule IDs", "groups", "never both")
    assert all(value in content for value in expected)


def test_provider_linting_documentation_diagrams_lifecycle_and_transport() -> None:
    content = " ".join(DOC_PATH.read_text(encoding="utf-8").split())
    expected = (
        "```mermaid",
        "Existing tfprotov6 validation RPC",
        "Decoded semantically valid configuration",
        "Provider component lint()",
        "LintFinding values",
        "LintSelector",
        "Fail-open runner",
        "Defensive finding filter",
        "tfprotov6 compatibility adapter",
        "TofuSoup direct lane: 7 paths",
        "OpenTofu beta validation lane: 4 paths",
        "Validation RPC response",
        "Warning diagnostics",
        "Future native adapter",
        "tofusoup --> validation_rpc",
        "opentofu --> validation_rpc",
        "validation_rpc --> config",
        "config --> runner",
        "selector --> runner",
        "runner --> hook --> findings --> finding_filter",
        "finding_filter --> compatibility_adapter --> warnings --> response",
        "finding_filter -.-> native_adapter",
        "provider, resource, data source, ephemeral, list, action, and state store",
        "provider, resource, data source, and ephemeral",
        "Neither client supplies provider selector hints over tfprotov6 today",
    )
    assert all(value in content for value in expected)


@pytest.mark.parametrize(
    "url",
    [
        pytest.param(
            "https://github.com/opentofu/opentofu/blob/main/rfc/20260406-linting.md",
            id="rfc",
        ),
        pytest.param(
            "https://github.com/opentofu/opentofu/issues/4310",
            id="tracker",
        ),
        pytest.param(
            "https://github.com/opentofu/opentofu/pull/4337",
            id="implementation",
        ),
        pytest.param(
            "https://github.com/opentofu/opentofu/releases/tag/v1.13.0-beta1",
            id="beta-release",
        ),
    ],
)
def test_provider_linting_documentation_links_upstream_sources(url: str) -> None:
    assert url in DOC_PATH.read_text(encoding="utf-8")


def test_provider_linting_documentation_is_in_navigation() -> None:
    expected = {"Provider Linting": "core-concepts/provider-linting.md"}
    formatting_variant = """nav:
  - Concepts:
      - Provider Linting: core-concepts/provider-linting.md
"""

    for source in (MKDOCS_PATH.read_text(encoding="utf-8"), formatting_variant):
        config = yaml.safe_load(source)
        concepts = next(section["Concepts"] for section in config["nav"] if "Concepts" in section)
        assert expected in concepts


# 🐍🏗️🔚
