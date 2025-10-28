#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from collections.abc import Callable
from typing import Any, ClassVar

from provide.foundation import logger
from provide.foundation.config import ConfigValidationError
from provide.foundation.errors import resilient


class Validators:
    """Manages global registration and application of validators."""

    _registry: ClassVar[dict[str, Callable[..., Any]]] = {}  # Class variable initialized once

    @classmethod
    def register(cls, name: str) -> Callable[..., Any]:
        """Decorator to register a validator with a specific name."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            cls._registry[name] = func
            logger.debug(f"Validator '{name}' registered.")
            return func

        return decorator

    @classmethod
    @resilient()
    def attach(cls, metadata: Any, *validator_names: str) -> None:
        """Attach validators to AttributeMetadata by name."""
        for name in validator_names:
            if name not in cls._registry:
                raise ConfigValidationError(f"Validator '{name}' not registered.")

            validator = cls._registry[name]

            if not hasattr(metadata, "validators") or not isinstance(metadata.validators, list):
                logger.error(
                    f"Cannot attach validator: 'metadata' object for '{getattr(metadata, 'description', 'unknown')}' lacks a list 'validators' attribute."
                )
                continue

            metadata.validators.append(validator)
            logger.debug(
                f"Validator '{name}' attached to '{getattr(metadata, 'description', 'unknown attribute')}'."
            )

    @classmethod
    @resilient()
    def validate(cls, validator_name: str, value: Any, metadata: Any) -> None:
        """Apply a specific validator at runtime."""
        if validator_name not in cls._registry:
            raise ConfigValidationError(f"Validator '{validator_name}' not registered.")

        try:
            cls._registry[validator_name](value, metadata)
        except Exception as e:
            raise ConfigValidationError(f"Validation failed for '{validator_name}': {e!s}") from e


# 🐍🏗️🔚
