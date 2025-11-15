#!/usr/bin/env python3
"""
Test script to verify the demo provider works with s_function.
"""

import asyncio
import sys


async def test_provider():
    """Test that the provider loads and functions work."""
    print("=" * 60)
    print("Testing Demo Provider with s_function")
    print("=" * 60)

    # Import the provider module to trigger registration
    print("\n1. Importing provider module...")
    try:
        import provider  # noqa: F401

        print("   ✅ Provider module imported successfully")
    except Exception as e:
        print(f"   ❌ Failed to import provider: {e}")
        return False

    # Test that function classes exist
    print("\n2. Checking function classes...")
    try:
        from provider import AddFunction, JoinFunction, UpperFunction

        for func_cls, name in [
            (UpperFunction, "upper"),
            (JoinFunction, "join_strings"),
            (AddFunction, "add"),
        ]:
            if hasattr(func_cls, "get_schema"):
                print(f"   ✅ {name} class has get_schema method")
            else:
                print(f"   ❌ {name} class missing get_schema")
                return False
    except Exception as e:
        print(f"   ❌ Failed to import function classes: {e}")
        return False

    # Test that functions have get_schema using s_function
    print("\n3. Testing get_schema() with s_function...")
    try:
        from provider import AddFunction, JoinFunction, UpperFunction

        from pyvider.schema import PvsSchema

        for func_cls, name in [
            (UpperFunction, "upper"),
            (JoinFunction, "join_strings"),
            (AddFunction, "add"),
        ]:
            schema = func_cls.get_schema()
            if isinstance(schema, PvsSchema):
                print(f"   ✅ {name}: get_schema() returns PvsSchema")
                # Check for parameters
                if "param_0" in schema.block.attributes:
                    print("      - Has parameters ✓")
                if "return_type" in schema.block.attributes:
                    print("      - Has return type ✓")
            else:
                print(f"   ❌ {name}: get_schema() returned {type(schema)}")
                return False
    except Exception as e:
        print(f"   ❌ Failed to test get_schema: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Test function execution
    print("\n4. Testing function execution...")
    try:
        from provider import AddFunction, JoinFunction, UpperFunction

        # Test upper function
        upper_func = UpperFunction(name="upper")
        result = await upper_func.call("hello world")
        if result == "HELLO WORLD":
            print(f"   ✅ upper('hello world') = '{result}'")
        else:
            print(f"   ❌ upper('hello world') = '{result}' (expected 'HELLO WORLD')")
            return False

        # Test join function
        join_func = JoinFunction(name="join_strings")
        result = await join_func.call(["one", "two", "three"], "-")
        if result == "one-two-three":
            print(f"   ✅ join_strings(['one', 'two', 'three'], '-') = '{result}'")
        else:
            print(f"   ❌ join_strings returned '{result}'")
            return False

        # Test add function
        add_func = AddFunction(name="add")
        result = await add_func.call(5.5, 3.3)
        expected = 8.8
        if abs(result - expected) < 0.01:
            print(f"   ✅ add(5.5, 3.3) = {result}")
        else:
            print(f"   ❌ add(5.5, 3.3) = {result} (expected {expected})")
            return False
    except Exception as e:
        print(f"   ❌ Failed to execute functions: {e}")
        import traceback

        traceback.print_exc()
        return False

    # Test schema structure
    print("\n5. Verifying schema structure...")
    try:
        from provider import UpperFunction

        schema = UpperFunction.get_schema()

        # Check version
        if schema.version == 1:
            print(f"   ✅ Schema version: {schema.version}")
        else:
            print(f"   ❌ Schema version: {schema.version} (expected 1)")
            return False

        # Check CTY types
        from pyvider.cty import CtyString

        param_type = schema.block.attributes["param_0"].type
        return_type = schema.block.attributes["return_type"].type

        if isinstance(param_type, CtyString):
            print("   ✅ Parameter type: CtyString")
        else:
            print(f"   ❌ Parameter type: {type(param_type)}")
            return False

        if isinstance(return_type, CtyString):
            print("   ✅ Return type: CtyString")
        else:
            print(f"   ❌ Return type: {type(return_type)}")
            return False
    except Exception as e:
        print(f"   ❌ Failed to verify schema: {e}")
        import traceback

        traceback.print_exc()
        return False

    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\ns_function is working perfectly with the provider! 🎉\n")
    return True


if __name__ == "__main__":
    success = asyncio.run(test_provider())
    sys.exit(0 if success else 1)


# 🐍🏗️🔚
