#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Pyvider CLI Package
==================
This module assembles the main CLI application."""

import os
import sys

# Ensure TCP transport is used on Windows BEFORE any pyvider imports
if sys.platform == "win32" and "PLUGIN_SERVER_TRANSPORTS" not in os.environ:
    os.environ["PLUGIN_SERVER_TRANSPORTS"] = "tcp"

# Install lazy loader for on-demand package extraction
# This must be done BEFORE importing packages that might be lazily loaded
from pyvider.lazy_import import install_lazy_loader
install_lazy_loader()

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
