#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for the public, protocol-neutral lint model."""

from collections.abc import Iterable
from typing import get_type_hints
from unittest.mock import Mock

from attrs.exceptions import FrozenInstanceError
import pytest


def test_lint_finding_is_immutable_and_normalizes_groups() -> None:
    from pyvider.lint.model import LintFinding

    finding = LintFinding(
        rule="provide-io/pyvider:insecure-http",
        groups=["provide-io/pyvider:all", "provide-io/pyvider:security"],
        summary="Insecure HTTP endpoint",
        detail="Use HTTPS.",
        attribute_path="url",
    )

    assert finding.groups == ("provide-io/pyvider:all", "provide-io/pyvider:security")
    with pytest.raises(FrozenInstanceError):
        finding.summary = "Changed"  # type: ignore[misc]


def test_lint_finding_constructor_accepts_any_string_iterable() -> None:
    from pyvider.lint.model import LintFinding

    assert get_type_hints(LintFinding.__init__)["groups"] == Iterable[str]


def test_lint_finding_rejects_a_bare_string_for_groups() -> None:
    from pyvider.lint.model import LintFinding

    with pytest.raises(TypeError, match="groups must be an iterable of lint addresses, not a string"):
        LintFinding(
            rule="provide-io/pyvider:insecure-http",
            groups="provide-io/pyvider:security",
            summary="Insecure HTTP endpoint",
            detail="Use HTTPS.",
        )


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        pytest.param("rule", "Uppercase", id="uppercase-rule"),
        pytest.param("rule", "provide-io/pyvider:", id="missing-rule-name"),
        pytest.param("rule", "provide.io/pyvider:rule", id="invalid-namespace-character"),
        pytest.param("groups", ("provide-io/pyvider:security", "bad.group"), id="invalid-group"),
    ],
)
def test_lint_finding_rejects_invalid_addresses(field_name: str, invalid_value: object) -> None:
    from pyvider.lint.model import LintFinding

    values: dict[str, object] = {
        "rule": "provide-io/pyvider:insecure-http",
        "groups": ("provide-io/pyvider:all",),
        "summary": "Insecure HTTP endpoint",
        "detail": "Use HTTPS.",
    }
    values[field_name] = invalid_value

    with pytest.raises(ValueError, match="valid lint address"):
        LintFinding(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("field_name", "blank_value"),
    [
        pytest.param("summary", "", id="empty-summary"),
        pytest.param("summary", "   ", id="whitespace-summary"),
        pytest.param("detail", "", id="empty-detail"),
        pytest.param("detail", "\t", id="whitespace-detail"),
        pytest.param("attribute_path", "", id="empty-attribute-path"),
        pytest.param("attribute_path", "  ", id="whitespace-attribute-path"),
    ],
)
def test_lint_finding_rejects_blank_text(field_name: str, blank_value: str) -> None:
    from pyvider.lint.model import LintFinding

    values: dict[str, object] = {
        "rule": "provide-io/pyvider:insecure-http",
        "groups": ("provide-io/pyvider:all",),
        "summary": "Insecure HTTP endpoint",
        "detail": "Use HTTPS.",
        "attribute_path": None,
    }
    values[field_name] = blank_value

    with pytest.raises(ValueError, match="must not be blank"):
        LintFinding(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    ["rule", "groups", "summary", "detail", "attribute_path"],
)
def test_lint_finding_rejects_non_utf8_text(field_name: str) -> None:
    from pyvider.lint.model import LintFinding

    values: dict[str, object] = {
        "rule": "provide-io/pyvider:insecure-http",
        "groups": ("provide-io/pyvider:all",),
        "summary": "Insecure HTTP endpoint",
        "detail": "Use HTTPS.",
        "attribute_path": "url",
    }
    values[field_name] = ("provide-io/pyvider:\ud800",) if field_name == "groups" else "\ud800"

    with pytest.raises(ValueError, match="valid UTF-8"):
        LintFinding(**values)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "attribute_path",
    ["nested.url", "items[0]", "url/name", "two words", "0url"],
)
def test_lint_finding_rejects_non_top_level_attribute_path(attribute_path: str) -> None:
    from pyvider.lint.model import LintFinding

    with pytest.raises(ValueError, match="top-level attribute name"):
        LintFinding(
            rule="provide-io/pyvider:insecure-http",
            groups=("provide-io/pyvider:all",),
            summary="Insecure HTTP endpoint",
            detail="Use HTTPS.",
            attribute_path=attribute_path,
        )


def test_lint_context_is_immutable() -> None:
    from pyvider.lint.model import LintContext

    context = LintContext(config={"url": "http://example.test"}, selector=Mock())

    with pytest.raises(FrozenInstanceError):
        context.config = {}  # type: ignore[misc]


def test_lint_context_enabled_delegates_to_selector() -> None:
    from pyvider.lint.model import LintContext

    selector = Mock()
    selector.enabled.return_value = True
    context = LintContext(config=object(), selector=selector)

    assert context.enabled("provide-io/pyvider:insecure-http", "provide-io/pyvider:security") is True
    selector.enabled.assert_called_once_with("provide-io/pyvider:insecure-http", "provide-io/pyvider:security")


def test_lint_model_public_exports() -> None:
    from pyvider import lint
    from pyvider.lint.model import LintContext, LintFinding
    from pyvider.lint.selector import LintSelector

    assert lint.LintContext is LintContext
    assert lint.LintFinding is LintFinding
    assert lint.LintSelector is LintSelector


# 🐍🏗️🔚
