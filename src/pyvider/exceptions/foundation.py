#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""


class PyviderError(Exception):
    """Base class for all Pyvider errors."""

    pass


class CapabilityError(PyviderError):
    pass


class ValueError(PyviderError):
    pass


class ConfigurationError(PyviderError):
    pass


class DataSourceError(PyviderError):
    pass


class FunctionError(PyviderError):
    pass


class InvalidTypeError(PyviderError):
    """Raised when a value does not match the expected type."""

    def __init__(self, expected_type: str = "unknown", actual_type: str = "unknown") -> None:
        super().__init__(f"Invalid type: expected '{expected_type}', got '{actual_type}'.")


class UnsupportedTypeError(PyviderError):
    """Raised when an unsupported type is encountered."""

    def __init__(self, type_name: str = "unknown") -> None:
        super().__init__(f"Unsupported type encountered: '{type_name}'.")


# 🐍🏗️🔚
