#!/usr/bin/env python3
"""
Test script to verify the demo provider works with s_function.
"""

import asyncio
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


async def _test_import_provider() -> bool:
    """Test importing the provider module."""
    from provide.foundation.console import pout

    pout("\n1. Importing provider module...")
    try:
        import demo  # noqa: F401

        pout("   Provider module imported successfully")
        return True
    except Exception as e:
        pout(f"   Failed to import provider: {e}")
        return False


async def _test_function_classes() -> bool:
    """Test that function classes exist."""
    from provide.foundation.console import pout

    pout("\n2. Checking function classes...")
    try:
        from demo import CalculateCostFunction, FormatTagsFunction, GenerateNameFunction, ValidateCIDRFunction

        for func_cls, name in [
            (FormatTagsFunction, "format_tags"),
            (CalculateCostFunction, "calculate_cost"),
            (ValidateCIDRFunction, "validate_cidr"),
            (GenerateNameFunction, "generate_name"),
        ]:
            if not hasattr(func_cls, "get_schema"):
                pout(f"   {name} class missing get_schema")
                return False
            pout(f"   {name} class has get_schema method")
        return True
    except Exception as e:
        pout(f"   Failed to import function classes: {e}")
        return False


async def _test_get_schema() -> bool:
    """Test get_schema with s_function."""
    from provide.foundation.console import pout

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
            if not isinstance(schema, PvsSchema):
                pout(f"   {name}: get_schema() returned {type(schema)}")
                return False

            pout(f"   {name}: get_schema() returns PvsSchema")
            if "param_0" in schema.block.attributes:
                pout("      - Has parameters")
            if "return_type" in schema.block.attributes:
                pout("      - Has return type")
        return True
    except Exception as e:
        pout(f"   Failed to test get_schema: {e}")
        import traceback

        traceback.print_exc()
        return False


async def _test_function_execution() -> bool:
    """Test function execution."""
    from provide.foundation.console import pout

    pout("\n4. Testing function execution...")
    try:
        from demo import CalculateCostFunction, FormatTagsFunction, GenerateNameFunction, ValidateCIDRFunction

        # Test format_tags function
        format_func = FormatTagsFunction(name="format_tags")
        result = await format_func.call({"env": "prod", "team": "infra"}, False)
        expected = '{"env": "prod", "team": "infra"}'
        if result != expected:
            pout(f"   format_tags() = '{result}' (expected '{expected}')")
            return False
        pout(f"   format_tags() = '{result}'")

        # Test calculate_cost function
        cost_func = CalculateCostFunction(name="calculate_cost")
        result = await cost_func.call("t2.micro", 730)
        expected = 0.0116 * 730  # 8.468
        if abs(result - expected) >= 0.01:
            pout(f"   calculate_cost returned {result} (expected {expected})")
            return False
        pout(f"   calculate_cost('t2.micro', 730) = {result:.4f}")

        # Test validate_cidr function
        cidr_func = ValidateCIDRFunction(name="validate_cidr")
        result = await cidr_func.call("10.0.0.0/16")
        if result is not True:
            pout(f"   validate_cidr('10.0.0.0/16') = {result} (expected True)")
            return False
        pout("   validate_cidr('10.0.0.0/16') = True")

        # Test generate_name function
        name_func = GenerateNameFunction(name="generate_name")
        result = await name_func.call("web", "prod", "us-east-1", 1)
        expected = "web-prod-use1-001"
        if result != expected:
            pout(f"   generate_name() = '{result}' (expected '{expected}')")
            return False
        pout(f"   generate_name() = '{result}'")

        return True
    except Exception as e:
        pout(f"   Failed to execute functions: {e}")
        import traceback

        traceback.print_exc()
        return False


async def _test_schema_structure() -> bool:
    """Test schema structure."""
    from provide.foundation.console import pout

    pout("\n5. Verifying schema structure...")
    try:
        from demo import ValidateCIDRFunction

        from pyvider.cty import CtyBool, CtyString

        schema = ValidateCIDRFunction.get_schema()

        # Check version
        if schema.version != 1:
            pout(f"   Schema version: {schema.version} (expected 1)")
            return False
        pout(f"   Schema version: {schema.version}")

        # Check CTY types
        param_type = schema.block.attributes["param_0"].type
        return_type = schema.block.attributes["return_type"].type

        if not isinstance(param_type, CtyString):
            pout(f"   Parameter type: {type(param_type)}")
            return False
        pout("   Parameter type: CtyString")

        if not isinstance(return_type, CtyBool):
            pout(f"   Return type: {type(return_type)}")
            return False
        pout("   Return type: CtyBool")

        return True
    except Exception as e:
        pout(f"   Failed to verify schema: {e}")
        import traceback

        traceback.print_exc()
        return False


async def test_provider() -> bool:
    """Test that the provider loads and functions work."""
    from provide.foundation.console import pout

    pout("=" * 60)
    pout("Testing Demo Provider with s_function")
    pout("=" * 60)

    # Run all test steps
    if not await _test_import_provider():
        return False

    if not await _test_function_classes():
        return False

    if not await _test_get_schema():
        return False

    if not await _test_function_execution():
        return False

    if not await _test_schema_structure():
        return False

    pout("\n" + "=" * 60)
    pout("ALL TESTS PASSED!")
    pout("=" * 60)
    pout("\ns_function is working perfectly with the provider!\n")
    return True


if __name__ == "__main__":
    success = asyncio.run(test_provider())
    sys.exit(0 if success else 1)
