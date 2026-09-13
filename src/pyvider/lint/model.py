#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Immutable lint findings and invocation context."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from attrs import define, field

if TYPE_CHECKING:
    from pyvider.lint.selector import LintSelector


ConfigT = TypeVar("ConfigT")


RULE_ADDRESS = re.compile(r"^([a-z0-9]+[a-z0-9_\-/]*:)?[a-z0-9]+[a-z0-9_\-]*$")


def _valid_address(_instance: object, attribute: Any, value: str) -> None:
    if not isinstance(value, str) or RULE_ADDRESS.fullmatch(value) is None:
        raise ValueError(f"{attribute.name} must be a valid lint address")


def _valid_addresses(instance: object, attribute: Any, values: tuple[str, ...]) -> None:
    for value in values:
        _valid_address(instance, attribute, value)


def _not_blank(_instance: object, attribute: Any, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{attribute.name} must not be blank")


def _optional_not_blank(instance: object, attribute: Any, value: str | None) -> None:
    if value is not None:
        _not_blank(instance, attribute, value)


@define(frozen=True, slots=True)
class LintFinding:
    """One advisory issue reported by a provider component."""

    rule: str = field(validator=_valid_address)
    groups: tuple[str, ...] = field(converter=tuple, validator=_valid_addresses)
    summary: str = field(validator=_not_blank)
    detail: str = field(validator=_not_blank)
    attribute_path: str | None = field(default=None, validator=_optional_not_blank)


@define(frozen=True, slots=True)
class LintContext(Generic[ConfigT]):
    """Configuration and selector passed to a component lint hook."""

    config: ConfigT
    selector: LintSelector

    def enabled(self, rule: str, *groups: str) -> bool:
        """Return whether the active selector enables a rule and its groups."""
        return self.selector.enabled(rule, *groups)


# 🐍🏗️🔚
