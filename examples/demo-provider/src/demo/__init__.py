"""
Demo Provider Package

A complete example provider demonstrating all major Pyvider features:
- Provider configuration
- Resource management (CRUD operations)
- Data sources (read-only queries)
- Provider functions
- Ephemeral resources (temporary credentials / sessions)
- State management with private state
"""

# Import all components for auto-discovery
# The @register_* decorators will automatically register them with the hub

from .data_sources import DemoInstanceTypes, DemoRegions, DemoServerInfo
from .ephemerals import DemoSessionToken
from .functions import CalculateCostFunction, FormatTagsFunction, GenerateNameFunction, ValidateCIDRFunction
from .provider import DemoProvider
from .resources import DemoDatabase, DemoNetwork, DemoServer

__all__ = [
    "CalculateCostFunction",
    "DemoDatabase",
    "DemoInstanceTypes",
    "DemoNetwork",
    # Provider
    "DemoProvider",
    "DemoRegions",
    # Resources
    "DemoServer",
    # Data Sources
    "DemoServerInfo",
    # Ephemerals
    "DemoSessionToken",
    # Functions
    "FormatTagsFunction",
    "GenerateNameFunction",
    "ValidateCIDRFunction",
    # Entry point
    "main",
]


def main() -> None:
    """Entry point for terraform-provider-demo command."""
    from pyvider.cli import main as pyvider_main

    pyvider_main()
