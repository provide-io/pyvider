#
# pyvider/hub/validators.py
#
from collections.abc import Callable
from typing import Any, ClassVar

from pyvider.telemetry import logger


class Validators:
    """Manages global registration and application of validators."""

    _registry: ClassVar[dict[str, Callable]] = {}  # Class variable initialized once

    @classmethod
    def register(cls, name: str) -> Callable:
        """Decorator to register a validator with a specific name."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            cls._registry[name] = func
            logger.debug(f"Validator '{name}' registered.")
            return func

        return decorator

    @classmethod
    def attach(cls, metadata: Any, *validator_names: str) -> None:
        """Attach validators to AttributeMetadata by name."""
        for name in validator_names:
            if name not in cls._registry:
                raise ValueError(f"Validator '{name}' not registered.")

            validator = cls._registry[name]

            if not hasattr(metadata, "validators") or not isinstance(
                metadata.validators, list
            ):
                logger.error(
                    f"Cannot attach validator: 'metadata' object for '{getattr(metadata, 'description', 'unknown')}' lacks a list 'validators' attribute."
                )
                continue

            metadata.validators.append(validator)
            logger.debug(
                f"Validator '{name}' attached to '{getattr(metadata, 'description', 'unknown attribute')}'."
            )

    @classmethod
    def validate(cls, validator_name: str, value: Any, metadata: Any) -> None:
        """Apply a specific validator at runtime."""
        if validator_name not in cls._registry:
            raise ValueError(f"Validator '{validator_name}' not registered.")

        cls._registry[validator_name](value, metadata)


# 🐍🏗️


# 🐍🏗️📄🪄
