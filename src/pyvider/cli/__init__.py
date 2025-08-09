#
# pyvider/cli/__init__.py
#
"""
Pyvider CLI Package
==================
This module assembles the main CLI application.
"""

# 1. Import the foundational 'cli' group object from main.
# 2. Import the command objects (groups and commands) from their modules.
from .components_commands import components
from .config_commands import config
from .install_command import install_command
from .launch_context_command import launch_context_cmd
from .main import cli
from .prep_commands import prep
from .provide_command import provide_cmd

# 3. Explicitly attach the commands to the main cli group.
cli.add_command(components)
cli.add_command(config)
cli.add_command(install_command)
cli.add_command(launch_context_cmd)
cli.add_command(prep)
cli.add_command(provide_cmd)

# 4. Expose the fully assembled 'cli' object for the entry point.
__all__ = ["cli"]


# 🐍🏗️🚀🪄
