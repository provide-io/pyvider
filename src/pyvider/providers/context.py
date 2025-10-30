#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from attrs import define, field
from provide.foundation import logger

from pyvider.common.context import BaseContext

if TYPE_CHECKING:
    from pyvider.providers.base import BaseProvider


@define
class ProviderContext(BaseContext):
    """
    Holds the configured state of the provider. Inherits diagnostic
    reporting capabilities from BaseContext.
    """

    config: Any = field()
    provider: BaseProvider | None = field(default=None, init=False)
    test_mode_enabled: bool = field(default=False, kw_only=True)

    def __attrs_post_init__(self) -> None:
        logger.info(
            "ProviderContext initialized",
            config_type=type(self.config).__name__,
            test_mode=self.test_mode_enabled,
        )
        if self.test_mode_enabled:
            logger.warning("⚠️  Test mode enabled - this should only be used for testing and development")
        else:
            logger.debug("Test mode is not enabled - running in production mode")


# 🐍🏗️🔚
