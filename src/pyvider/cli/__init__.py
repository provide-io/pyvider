#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Pyvider CLI Package
==================
This module assembles the main CLI application."""

from pyvider.cli.components_commands import components
from pyvider.cli.config_commands import config
from pyvider.cli.install_command import install_command
from pyvider.cli.launch_context_command import launch_context_cmd
from pyvider.cli.main import cli
from pyvider.cli.provide_command import provide_cmd

# Explicitly attach the commands to the main cli group.
cli.add_command(components)
cli.add_command(config)
cli.add_command(install_command)
cli.add_command(launch_context_cmd)
cli.add_command(provide_cmd)


def main() -> None:
    """Main entry point for the Pyvider CLI application."""
    cli()


__all__ = ["cli", "main"]

# 🐍🏗️🔚
