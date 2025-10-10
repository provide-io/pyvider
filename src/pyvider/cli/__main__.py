"""
The canonical entry point for the Pyvider CLI application.
"""

import asyncio

from provide.foundation import setup_logging, shutdown_foundation

from pyvider.cli import cli


def main() -> None:
    """Main entry point for the Pyvider CLI application."""
    # Initialize Foundation logging for CLI mode
    # (Provider mode initializes logging separately in provide_command.py)
    setup_logging()

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
