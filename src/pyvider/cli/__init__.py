#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
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

from pyvider.cli.components_commands import components  # noqa: E402
from pyvider.cli.config_commands import config  # noqa: E402
from pyvider.cli.install_command import install_command  # noqa: E402
from pyvider.cli.launch_context_command import launch_context_cmd  # noqa: E402
from pyvider.cli.main import cli  # noqa: E402
from pyvider.cli.provide_command import provide_cmd  # noqa: E402

# 3. Explicitly attach the commands to the main cli group.
cli.add_command(components)
cli.add_command(config)
cli.add_command(install_command)
cli.add_command(launch_context_cmd)
cli.add_command(provide_cmd)


# 4. Create a main function that can be used as an entry point
def main() -> None:
    """Main entry point for the Pyvider CLI application.

    This allows the CLI to be invoked via 'pyvider.cli:main' entry point,
    in addition to the existing 'pyvider.cli.__main__:main' entry point.
    """
    cli()


# 5. Expose the fully assembled 'cli' object and main function for entry points.
__all__ = ["cli", "main"]

# 🐍🏗️🔚
