#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Immutable lint findings and invocation context."""

from __future__ import annotations

from collections.abc import Iterable
import re
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from attrs import define, field

if TYPE_CHECKING:
    from pyvider.lint.selector import LintSelector


ConfigT = TypeVar("ConfigT")


RULE_ADDRESS = re.compile(r"^([a-z0-9]+[a-z0-9_\-/]*:)?[a-z0-9]+[a-z0-9_\-]*$")


def _to_groups(values: Iterable[str]) -> tuple[str, ...]:
    """Normalize rule groups while preserving the public constructor type."""
    if isinstance(values, str):
        raise TypeError("groups must be an iterable of lint addresses, not a string")
    return tuple(values)


def _valid_utf8(attribute: Any, value: str) -> None:
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"{attribute.name} must contain valid UTF-8 text") from exc


def _valid_address(_instance: object, attribute: Any, value: str) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{attribute.name} must be a valid lint address")
    _valid_utf8(attribute, value)
    if RULE_ADDRESS.fullmatch(value) is None:
        raise ValueError(f"{attribute.name} must be a valid lint address")


def _valid_addresses(instance: object, attribute: Any, values: tuple[str, ...]) -> None:
    for value in values:
        _valid_address(instance, attribute, value)


def _not_blank(_instance: object, attribute: Any, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{attribute.name} must not be blank")
    _valid_utf8(attribute, value)


def _optional_top_level_attribute(instance: object, attribute: Any, value: str | None) -> None:
    if value is not None:
        _not_blank(instance, attribute, value)
        if not value.replace("-", "_").isidentifier():
            raise ValueError(f"{attribute.name} must be a top-level attribute name")


@define(frozen=True, slots=True)
class LintFinding:
    """One advisory issue reported by a provider component."""

    rule: str = field(validator=_valid_address)
    groups: tuple[str, ...] = field(converter=_to_groups, validator=_valid_addresses)
    summary: str = field(validator=_not_blank)
    detail: str = field(validator=_not_blank)
    attribute_path: str | None = field(default=None, validator=_optional_top_level_attribute)


@define(frozen=True, slots=True)
class LintContext(Generic[ConfigT]):
    """Configuration and selector passed to a component lint hook."""

    config: ConfigT
    selector: LintSelector

    def enabled(self, rule: str, *groups: str) -> bool:
        """Return whether the active selector enables a rule and its groups."""
        return self.selector.enabled(rule, *groups)


# 🐍🏗️🔚
