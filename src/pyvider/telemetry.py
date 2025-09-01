"""
Telemetry adapter module for pyvider.

This module provides compatibility layer between pyvider's existing telemetry
usage and provide.foundation's logger system.
"""

from provide.foundation import logger as foundation_logger
from provide.foundation import get_logger, setup_logging

# Re-export the foundation logger as the default logger
logger = foundation_logger

# Re-export utility functions
__all__ = ["logger", "get_logger", "setup_telemetry"]


def setup_telemetry(**kwargs) -> None:
    """
    Setup telemetry/logging for pyvider.
    
    This is a compatibility wrapper around foundation's setup_logging.
    """
    setup_logging(**kwargs)