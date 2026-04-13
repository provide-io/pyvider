#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from pyvider.cty.errors import ValidationError


class MockType(type[str]):
    """Mock Terraform type for testing."""

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValidationError("MockType", f"Value must be a string, got {type(value).__name__}.")

    def serialize(self, value: str) -> str:
        return f'"{value}"'

    def equal(self, other: "type") -> bool:
        return isinstance(other, MockType)

    def usable_as(self, other: "type") -> bool:
        return isinstance(other, MockType)

    def __str__(self) -> str:
        return "MockType"


# 🐍🏗️🔚
