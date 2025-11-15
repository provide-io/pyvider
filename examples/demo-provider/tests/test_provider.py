#!/usr/bin/env python3
"""
Test script to verify the demo provider works with s_function.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


async def test_provider():
    """Test that the provider loads and functions work."""
    from pyvider.telemetry import pout

    pout("=" * 60)
    pout("Testing Demo Provider with s_function")
    pout("=" * 60)

    # Import the provider module to trigger registration
    pout("\n1. Importing provider module...")
    try:
        import demo  # noqa: F401

        pout("   Provider module imported successfully")
    except Exception as e:
        pout(f"   Failed to import provider: {e}")
        return False

    # Test that function classes exist
    pout("\n2. Checking function classes...")
    try:
        from demo import CalculateCostFunction, FormatTagsFunction, GenerateNameFunction, ValidateCIDRFunction

        for func_cls, name in [
            (FormatTagsFunction, "format_tags"),
            (CalculateCostFunction, "calculate_cost"),
            (ValidateCIDRFunction, "validate_cidr"),
            (GenerateNameFunction, "generate_name"),
        ]:
            if hasattr(func_cls, "get_schema"):
                pout(f"   {name} class has get_schema method")
            else:
                pout(f"   {name} class missing get_schema")
                return False
    except Exception as e:
        pout(f"   Failed to import function classes: {e}")
        return False

    # Test that functions have get_schema using s_function
    pout("\n3. Testing get_schema() with s_function...")
    try:
        from demo import CalculateCostFunction, FormatTagsFunction, GenerateNameFunction, ValidateCIDRFunction

        from pyvider.schema import PvsSchema

        for func_cls, name in [
            (FormatTagsFunction, "format_tags"),
            (CalculateCostFunction, "calculate_cost"),
            (ValidateCIDRFunction, "validate_cidr"),
            (GenerateNameFunction, "generate_name"),
        ]:
            schema = func_cls.get_schema()
            if isinstance(schema, PvsSchema):
                pout(f"   {name}: get_schema() returns PvsSchema")
                # Check for parameters
                if "param_0" in schema.block.attributes:
                    pout("      - Has parameters")
                if "return_type" in schema.block.attributes:
                    pout("      - Has return type")
            else:
                pout(f"   {name}: get_schema() returned {type(schema)}")
                return False
    except Exception as e:
        pout(f"   Failed to test get_schema: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Test function execution
    pout("\n4. Testing function execution...")
    try:
        from demo import CalculateCostFunction, FormatTagsFunction, GenerateNameFunction, ValidateCIDRFunction

        # Test format_tags function
        format_func = FormatTagsFunction(name="format_tags")
        result = await format_func.call({"env": "prod", "team": "infra"}, False)
        expected = '{"env": "prod", "team": "infra"}'
        if result == expected:
            pout(f"   format_tags() = '{result}'")
        else:
            pout(f"   format_tags() = '{result}' (expected '{expected}')")
            return False

        # Test calculate_cost function
        cost_func = CalculateCostFunction(name="calculate_cost")
        result = await cost_func.call("t2.micro", 730)
        expected = 0.0116 * 730  # 8.468
        if abs(result - expected) < 0.01:
            pout(f"   calculate_cost('t2.micro', 730) = {result:.4f}")
        else:
            pout(f"   calculate_cost returned {result} (expected {expected})")
            return False

        # Test validate_cidr function
        cidr_func = ValidateCIDRFunction(name="validate_cidr")
        result = await cidr_func.call("10.0.0.0/16")
        if result is True:
            pout("   validate_cidr('10.0.0.0/16') = True")
        else:
            pout(f"   validate_cidr('10.0.0.0/16') = {result} (expected True)")
            return False

        # Test generate_name function
        name_func = GenerateNameFunction(name="generate_name")
        result = await name_func.call("web", "prod", "us-east-1", 1)
        expected = "web-prod-use1-001"
        if result == expected:
            pout(f"   generate_name() = '{result}'")
        else:
            pout(f"   generate_name() = '{result}' (expected '{expected}')")
            return False
    except Exception as e:
        pout(f"   Failed to execute functions: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Test schema structure
    pout("\n5. Verifying schema structure...")
    try:
        from demo import ValidateCIDRFunction

        schema = ValidateCIDRFunction.get_schema()

        # Check version
        if schema.version == 1:
            pout(f"   Schema version: {schema.version}")
        else:
            pout(f"   Schema version: {schema.version} (expected 1)")
            return False

        # Check CTY types
        from pyvider.cty import CtyBool, CtyString

        param_type = schema.block.attributes["param_0"].type
        return_type = schema.block.attributes["return_type"].type

        if isinstance(param_type, CtyString):
            pout("   Parameter type: CtyString")
        else:
            pout(f"   Parameter type: {type(param_type)}")
            return False

        if isinstance(return_type, CtyBool):
            pout("   Return type: CtyBool")
        else:
            pout(f"   Return type: {type(return_type)}")
            return False
    except Exception as e:
        pout(f"   Failed to verify schema: {e}")
        import traceback

        traceback.print_exc()
        return False

    pout("\n" + "=" * 60)
    pout("ALL TESTS PASSED!")
    pout("=" * 60)
    pout("\ns_function is working perfectly with the provider!\n")
    return True


if __name__ == "__main__":
    success = asyncio.run(test_provider())
    sys.exit(0 if success else 1)
