#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""OpenTofu-compatible provider lint selection."""

from collections.abc import Iterable

from attrs import define, field
from provide.foundation import logger

from pyvider.lint.model import RULE_ADDRESS


def _to_frozenset(values: Iterable[str]) -> frozenset[str]:
    return frozenset(values)


@define(frozen=True, slots=True)
class LintSelector:
    """The rule and group addresses selected for one provider process."""

    include: frozenset[str] = field(factory=frozenset, converter=_to_frozenset)
    exclude: frozenset[str] = field(factory=frozenset, converter=_to_frozenset)

    @classmethod
    def parse(cls, values: Iterable[object]) -> "LintSelector":
        """Build a selector from include tokens and ``!``-prefixed exclusions."""
        include: set[str] = set()
        exclude: set[str] = set()
        for value in values:
            if not isinstance(value, str):
                logger.warning(
                    "Ignoring malformed lint selector",
                    operation="lint_selector_parse",
                    reason="not_string",
                    value_type=type(value).__name__,
                )
                continue

            token = value.strip()
            excluded = token.startswith("!")
            address = token[1:] if excluded else token
            if RULE_ADDRESS.fullmatch(address) is None:
                logger.warning(
                    "Ignoring malformed lint selector",
                    operation="lint_selector_parse",
                    reason="invalid_address",
                )
                continue

            (exclude if excluded else include).add(address)
        return cls(include=include, exclude=exclude - include)

    def as_tokens(self) -> tuple[str, ...]:
        """Return a stable, canonical representation for configuration storage."""
        return (*sorted(self.include), *(f"!{value}" for value in sorted(self.exclude)))

    @property
    def is_disabled(self) -> bool:
        """Return whether no include or exclude tokens were configured."""
        return not self.include and not self.exclude

    def enabled(self, rule: str, *groups: str) -> bool:
        """Apply OpenTofu's rule-before-group selection precedence."""
        if rule in self.include:
            return True
        if rule in self.exclude:
            return False
        if any(group in self.include for group in groups):
            return True
        if any(group in self.exclude for group in groups):
            return False
        return "all" in self.include


# 🐍🏗️🔚
