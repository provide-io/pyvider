#!/usr/bin/env python3.11
"""Test that all Pyvider functionality works on Python 3.11"""

import sys
import subprocess

def test_python_version():
    """Verify we're running on Python 3.11"""
    print(f"Python version: {sys.version}")
    assert sys.version_info[:2] == (3, 11), f"Expected Python 3.11, got {sys.version_info[:2]}"
    print("✓ Running on Python 3.11")

def test_imports():
    """Test that all Pyvider modules can be imported"""
    modules = [
        "pyvider",
        "pyvider.cty",
        "pyvider.hcl", 
        "pyvider.telemetry",
        "pyvider.rpcplugin",
        "pyvider.components",
        "pyvider.resources",
        "pyvider.capabilities",
        "pyvider.schemas",
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"✓ Successfully imported {module}")
        except ImportError as e:
            print(f"✗ Failed to import {module}: {e}")
            raise

def test_basic_functionality():
    """Test basic Pyvider functionality"""
    from pyvider.cty import CtyString, CtyNumber, CtyList, CtyObject
    from pyvider.resources import ResourceContext
    from pyvider.hcl import parse_hcl_to_cty
    
    # Test CtyValue creation
    string_val = CtyString().validate("hello")
    print(f"✓ Created CtyString: {string_val}")
    
    number_val = CtyNumber().validate(42)
    print(f"✓ Created CtyNumber: {number_val}")
    
    list_val = CtyList(element_type=CtyString()).validate(["a", "b", "c"])
    print(f"✓ Created CtyList: {list_val}")
    
    # Test HCL parsing
    hcl_content = '''
    resource "example" "test" {
        name = "test-resource"
        count = 5
    }
    '''
    parsed = parse_hcl_to_cty(hcl_content)
    print(f"✓ Parsed HCL content: {type(parsed)}")
    
    # Test ResourceContext
    ctx = ResourceContext()
    print(f"✓ Created ResourceContext: {type(ctx)}")

def run_pytest():
    """Run pytest on cty tests to ensure they still pass"""
    print("\nRunning pytest on pyvider-cty tests...")
    result = subprocess.run(
        ["python3.11", "-m", "pytest", "../pyvider-cty/tests/", "-v", "--tb=short"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ All pyvider-cty tests passed!")
        # Extract test summary
        lines = result.stdout.split('\n')
        for line in lines:
            if 'passed' in line and 'failed' not in line:
                print(f"  {line.strip()}")
    else:
        print("✗ Some tests failed:")
        print(result.stdout[-1000:])  # Last 1000 chars
        raise RuntimeError("Tests failed")

def main():
    print("=== Testing Pyvider Python 3.11 Support ===\n")
    
    try:
        test_python_version()
        print()
        
        test_imports()
        print()
        
        test_basic_functionality()
        print()
        
        run_pytest()
        
        print("\n=== All tests passed! Pyvider works on Python 3.11 ===")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()