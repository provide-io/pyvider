#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The canonical entry point for the Pyvider CLI application."""

import asyncio
import os
import sys
from typing import Literal, cast

from attrs import evolve
from provide.foundation import TelemetryConfig, get_hub, logger, shutdown_foundation

from pyvider.cli import cli
from pyvider.common.config import PyviderConfig

LogLevel = Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "TRACE", "NOTSET"]


def _log_level_from_argv(argv: list[str]) -> str | None:
    """The `--log-level` a user asked for, read straight from the command line.

    Foundation is configured once, below, before Click parses anything, so a
    flag declared on a subcommand cannot reach it through the ordinary route --
    `provide --log-level DEBUG` was accepted and did nothing at all. Reading it
    here is what makes the flag mean something, and an explicit flag is the most
    specific thing a user can say, so it wins over the environment.
    """
    for index, token in enumerate(argv):
        if token == "--log-level":
            if index + 1 < len(argv):
                return argv[index + 1].upper()
            return None
        if token.startswith("--log-level="):
            return token.split("=", 1)[1].upper()
    return None


def main() -> None:
    """Main entry point for the Pyvider CLI application."""
    # Initialize Foundation with Pyvider-specific configuration
    requested_level = _log_level_from_argv(sys.argv)
    if requested_level:
        os.environ["PYVIDER_LOG_LEVEL"] = requested_level

    pyvider_config = PyviderConfig()  # Loads from environment

    # Get base telemetry config from environment
    base_telemetry = TelemetryConfig.from_env()

    # Merge with Pyvider-specific settings
    telemetry_config = evolve(
        base_telemetry,
        service_name="pyvider",
        logging=evolve(
            base_telemetry.logging,
            default_level=cast(LogLevel, pyvider_config.log_level),  # Uses PYVIDER_LOG_LEVEL
        ),
    )

    # Initialize Foundation with merged config
    hub = get_hub()
    hub.initialize_foundation(telemetry_config)

    logger.debug("Pyvider CLI starting")

    try:
        # The `cli` object is the fully assembled click group.
        # This call hands over control to click to parse args and run the
        # appropriate subcommand.
        cli()
    finally:
        # Ensure proper cleanup of telemetry resources
        asyncio.run(shutdown_foundation())


if __name__ == "__main__":
    main()

# 🐍🏗️🔚
