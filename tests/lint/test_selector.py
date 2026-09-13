#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for OpenTofu-compatible lint selector semantics."""

from unittest.mock import call, patch

import pytest

RULE = "provide-io/pyvider:insecure-http"
ALL = "provide-io/pyvider:all"
SECURITY = "provide-io/pyvider:security"


@pytest.mark.parametrize(
    ("selector_values", "rule", "groups", "expected"),
    [
        pytest.param(({RULE}, set()), RULE, (), True, id="exact-rule-include"),
        pytest.param(
            ({"all"}, {RULE}),
            RULE,
            (),
            False,
            id="exact-rule-exclude",
        ),
        pytest.param(({SECURITY}, set()), RULE, (ALL, SECURITY), True, id="any-included-group"),
        pytest.param(
            ({"all"}, {SECURITY}),
            RULE,
            (ALL, SECURITY),
            False,
            id="any-excluded-group",
        ),
        pytest.param(({"all"}, set()), RULE, (), True, id="global-all"),
        pytest.param(({ALL}, set()), RULE, (ALL, SECURITY), True, id="namespaced-all-group"),
        pytest.param(({ALL}, set()), RULE, (SECURITY,), False, id="namespaced-all-is-not-global"),
        pytest.param(
            ({RULE}, {SECURITY}),
            RULE,
            (SECURITY,),
            True,
            id="exact-include-before-group-exclude",
        ),
        pytest.param(
            ({SECURITY}, {RULE}),
            RULE,
            (SECURITY,),
            False,
            id="exact-exclude-before-group-include",
        ),
        pytest.param(({"unknown-valid"}, set()), RULE, (), False, id="unknown-no-op"),
    ],
)
def test_selector_enabled_precedence(
    selector_values: tuple[set[str], set[str]], rule: str, groups: tuple[str, ...], expected: bool
) -> None:
    from pyvider.lint.selector import LintSelector

    include, exclude = selector_values
    selector = LintSelector(include=include, exclude=exclude)
    assert selector.enabled(rule, *groups) is expected


def test_selector_parse_normalizes_tokens_and_include_wins_conflicts() -> None:
    from pyvider.lint.selector import LintSelector

    with patch("pyvider.lint.selector.logger.warning") as warning:
        selector = LintSelector.parse(
            [" beta ", "!zeta", "alpha", "alpha", " !beta ", "!alpha", "!gamma", "!gamma"]
        )

    assert selector.include == frozenset({"alpha", "beta"})
    assert selector.exclude == frozenset({"gamma", "zeta"})
    assert selector.as_tokens() == ("alpha", "beta", "!gamma", "!zeta")
    assert warning.call_args_list == [
        call(
            "Conflicting lint selector; inclusion wins",
            selector_address="alpha",
            reason="include_wins",
        ),
        call(
            "Conflicting lint selector; inclusion wins",
            selector_address="beta",
            reason="include_wins",
        ),
    ]


def test_selector_parse_logs_and_ignores_malformed_entries() -> None:
    from pyvider.lint.selector import LintSelector

    values: list[object] = [None, "", "  ", "Uppercase", "!", "!!rule", "bad.rule", "valid-rule"]

    with patch("pyvider.lint.selector.logger.warning") as warning:
        selector = LintSelector.parse(values)

    assert selector == LintSelector(include=frozenset({"valid-rule"}))
    assert warning.call_count == 7


def test_selector_no_tokens_is_disabled() -> None:
    from pyvider.lint.selector import LintSelector

    assert LintSelector.parse([]).is_disabled is True
    assert LintSelector(include=frozenset({"all"})).is_disabled is False
    assert LintSelector(exclude=frozenset({RULE})).is_disabled is False


# 🐍🏗️🔚
