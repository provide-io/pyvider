"""
Demo Provider - Function Definitions

Contains:
- FormatTagsFunction: Format tags to JSON
- CalculateCostFunction: Calculate monthly costs
- ValidateCIDRFunction: Validate CIDR notation
- GenerateNameFunction: Generate standardized names
"""

import json

from pyvider.cty import CtyBool, CtyMap, CtyNumber, CtyString
from pyvider.functions import BaseFunction, FunctionParameter, FunctionReturnType, register_function
from pyvider.schema import PvsSchema, a_bool, a_map, a_num, a_str, s_function


@register_function("format_tags")
class FormatTagsFunction(BaseFunction):
    """
    Format a map of tags into a JSON string.

    This function demonstrates:
    - Custom Terraform functions
    - Type-safe parameters
    - String manipulation
    """

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define function schema"""
        return s_function(
            parameters=[
                a_map(a_str(), description="Tag map to format"),
                a_bool(description="Pretty print the JSON"),
            ],
            return_type=a_str(description="Formatted JSON string"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        return [
            FunctionParameter(name="tags", type=CtyMap(CtyString()), description="Tag map to format"),
            FunctionParameter(name="pretty", type=CtyBool(), description="Pretty print the JSON"),
        ]

    def get_return_type(self) -> FunctionReturnType:
        return FunctionReturnType(type=CtyString())

    async def call(self, tags: dict[str, str], pretty: bool = False) -> str:
        """Execute the function"""
        if pretty:
            return json.dumps(tags, indent=2, sort_keys=True)
        return json.dumps(tags, sort_keys=True)


@register_function("calculate_cost")
class CalculateCostFunction(BaseFunction):
    """
    Calculate estimated monthly cost for a server.

    Demonstrates numeric calculations and multiple parameters.
    """

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define function schema"""
        return s_function(
            parameters=[
                a_str(description="Instance type"),
                a_num(description="Expected hours per month"),
            ],
            return_type=a_num(description="Estimated monthly cost"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        return [
            FunctionParameter(name="instance_type", type=CtyString(), description="Instance type"),
            FunctionParameter(
                name="hours_per_month", type=CtyNumber(), description="Expected hours per month"
            ),
        ]

    def get_return_type(self) -> FunctionReturnType:
        return FunctionReturnType(type=CtyNumber())

    async def call(self, instance_type: str, hours_per_month: float) -> float:
        """Calculate cost"""
        # Simplified pricing ($/hour)
        pricing = {
            "t2.micro": 0.0116,
            "t2.small": 0.023,
            "t2.medium": 0.0464,
        }

        hourly_rate = pricing.get(instance_type, 0.05)
        return hourly_rate * hours_per_month


@register_function("validate_cidr")
class ValidateCIDRFunction(BaseFunction):
    """
    Validate CIDR block notation.

    This function demonstrates:
    - Input validation
    - Boolean return type
    - Network calculations
    """

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define function schema"""
        return s_function(
            parameters=[
                a_str(description="CIDR block to validate (e.g., 10.0.0.0/16)"),
            ],
            return_type=a_bool(description="Whether CIDR is valid"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        return [
            FunctionParameter(name="cidr", type=CtyString(), description="CIDR block to validate"),
        ]

    def get_return_type(self) -> FunctionReturnType:
        return FunctionReturnType(type=CtyBool())

    async def call(self, cidr: str) -> bool:
        """Validate CIDR block"""
        try:
            # Split into IP and prefix
            if "/" not in cidr:
                return False

            ip_part, prefix_part = cidr.split("/")

            # Validate IP address parts
            octets = ip_part.split(".")
            if len(octets) != 4:
                return False

            for octet in octets:
                num = int(octet)
                if num < 0 or num > 255:
                    return False

            # Validate prefix length
            prefix = int(prefix_part)
            return not (prefix < 0 or prefix > 32)
        except (ValueError, AttributeError):
            return False


@register_function("generate_name")
class GenerateNameFunction(BaseFunction):
    """
    Generate a standardized resource name.

    This function demonstrates:
    - String formatting
    - Multiple parameters
    - Naming conventions
    """

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define function schema"""
        return s_function(
            parameters=[
                a_str(description="Name prefix (e.g., 'web', 'db', 'app')"),
                a_str(description="Environment (e.g., 'prod', 'staging', 'dev')"),
                a_str(description="Region code (e.g., 'us-east-1')"),
                a_num(description="Sequence number"),
            ],
            return_type=a_str(description="Standardized resource name"),
        )

    def get_parameters(self) -> list[FunctionParameter]:
        return [
            FunctionParameter(name="prefix", type=CtyString(), description="Name prefix"),
            FunctionParameter(name="environment", type=CtyString(), description="Environment"),
            FunctionParameter(name="region", type=CtyString(), description="Region code"),
            FunctionParameter(name="sequence", type=CtyNumber(), description="Sequence number"),
        ]

    def get_return_type(self) -> FunctionReturnType:
        return FunctionReturnType(type=CtyString())

    async def call(self, prefix: str, environment: str, region: str, sequence: float) -> str:
        """Generate standardized name"""
        # Extract region abbreviation (first letters of each part)
        region_parts = region.split("-")
        region_abbr = "".join([p[0] for p in region_parts])

        # Format: prefix-environment-region-sequence
        # Example: web-prod-use1-001
        return f"{prefix}-{environment}-{region_abbr}{region_parts[-1]}-{int(sequence):03d}"
