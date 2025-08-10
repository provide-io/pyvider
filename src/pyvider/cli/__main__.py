"""
The canonical entry point for the Pyvider CLI application.
"""

from . import cli


def main() -> None:
    """Main entry point for the Pyvider CLI application."""
    # The `cli` object is the fully assembled click group.
    # This call hands over control to click to parse args and run the
    # appropriate subcommand.
    cli()


if __name__ == "__main__":
    main()
