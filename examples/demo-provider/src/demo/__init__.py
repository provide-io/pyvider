"""
Demo Provider Package

A complete example provider demonstrating all major Pyvider features:
- Provider configuration
- Resource management (CRUD operations)
- Data sources (read-only queries)
- Provider functions
- State management with private state
"""

# Import all components for auto-discovery
# The @register_* decorators will automatically register them with the hub

from .data_sources import DemoInstanceTypes, DemoRegions, DemoServerInfo
from .functions import CalculateCostFunction, FormatTagsFunction, GenerateNameFunction, ValidateCIDRFunction
from .provider import DemoProvider
from .resources import DemoDatabase, DemoNetwork, DemoServer

__all__ = [
    # Provider
    "DemoProvider",
    # Resources
    "DemoServer",
    "DemoDatabase",
    "DemoNetwork",
    # Data Sources
    "DemoServerInfo",
    "DemoRegions",
    "DemoInstanceTypes",
    # Functions
    "FormatTagsFunction",
    "CalculateCostFunction",
    "ValidateCIDRFunction",
    "GenerateNameFunction",
    # Entry point
    "main",
]


def main():
    """Entry point for terraform-provider-demo command."""
    from pyvider.cli import main as pyvider_main

    pyvider_main()
