"""
The canonical entry point for the Pyvider CLI application.
"""

import asyncio
from provide.foundation import setup_telemetry, shutdown_foundation_telemetry
from pyvider.cli import cli


def main() -> None:
    """Main entry point for the Pyvider CLI application."""
    # Initialize foundation telemetry
    setup_telemetry()
    
    try:
        # The `cli` object is the fully assembled click group.
        # This call hands over control to click to parse args and run the
        # appropriate subcommand.
        cli()
    finally:
        # Ensure proper cleanup of telemetry resources
        asyncio.run(shutdown_foundation_telemetry())


if __name__ == "__main__":
    main()
