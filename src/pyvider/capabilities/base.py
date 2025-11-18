#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from abc import ABC, abstractmethod
from typing import Any

from pyvider.schema import PvsAttribute


class BaseCapability(ABC):
    """Abstract base class for all Pyvider capabilities."""

    @abstractmethod
    def __init__(self, config: Any | None = None) -> None:
        """
        Initializes the capability, optionally with provider-level configuration.
        Subclasses can override this to perform their own setup.
        """
        # No-op by default, subclasses can override
        pass

    @staticmethod
    @abstractmethod
    def get_schema_contribution() -> dict[str, PvsAttribute]:
        """
        Returns a dictionary of attributes to be merged into the
        provider's configuration schema.
        """
        raise NotImplementedError


# 🐍🏗️🔚
