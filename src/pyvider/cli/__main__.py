#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""The canonical entry point for the Pyvider CLI application."""

import asyncio

from attrs import evolve
from provide.foundation import TelemetryConfig, get_hub, logger, shutdown_foundation

from pyvider.cli import cli
from pyvider.common.config import PyviderConfig


def main() -> None:
    """Main entry point for the Pyvider CLI application."""
    # Initialize Foundation with Pyvider-specific configuration
    pyvider_config = PyviderConfig()  # Loads from environment

    # Get base telemetry config from environment
    base_telemetry = TelemetryConfig.from_env()

    # Merge with Pyvider-specific settings
    telemetry_config = evolve(
        base_telemetry,
        service_name="pyvider",
        logging=evolve(
            base_telemetry.logging,
            default_level=pyvider_config.log_level,  # Uses PYVIDER_LOG_LEVEL
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
