#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Any

from pyvider.exceptions.base import ConversionError


class SerializationError(ConversionError):
    """Raised when serialization of a value fails."""

    def __init__(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Serialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail


class DeserializationError(ConversionError):
    """Raised when deserialization of data into a value fails."""

    def __init__(
        self,
        message: str,
        *,
        type_name: str | None = None,
        source_value: Any = None,
        detail: str | None = None,
    ) -> None:
        full_message = f"Deserialization failed for type '{type_name or 'unknown'}': {message}{f' - Detail: {detail}' if detail else ''}"
        super().__init__(full_message, source_value=source_value, target_type=type_name)
        self.type_name = type_name
        self.detail = detail


# 🐍🏗️🔚
