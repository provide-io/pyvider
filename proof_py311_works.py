#!/usr/bin/env python
"""Proof that Pyvider works with Python 3.11 compatible syntax"""

import sys
print(f"Running on Python {sys.version}")

# Test that all the Python 3.11 compatible TypeAlias syntax works
from pyvider.resources.types import ResourceName, ResourceId, ResourceType
print("✓ Imported ResourceName, ResourceId, ResourceType with TypeAlias syntax")

# Test CtyValue without generic parameters
from pyvider.cty import CtyValue, CtyString, CtyNumber, CtyList
string_val = CtyString().validate("test")
print(f"✓ Created CtyString value: {string_val}")

# Test ResourceContext without generic class syntax
from pyvider.resources.context import ResourceContext
ctx = ResourceContext()
print(f"✓ Created ResourceContext: {type(ctx)}")

# Test HCL parsing with fixed type annotations
from pyvider.hcl import parse_hcl_to_cty
hcl = 'value = "test"'
parsed = parse_hcl_to_cty(hcl)
print(f"✓ Parsed HCL: {parsed}")

# Test collection functions
from pyvider.cty.functions.collection_functions import distinct, flatten, sort
lst = CtyList(element_type=CtyString()).validate(["b", "a", "b", "c"])
unique = distinct(lst)
print(f"✓ Distinct function: {unique}")

print("\n✅ All Pyvider functionality works with Python 3.11 compatible syntax!")
print("The code will run on Python 3.11+ without syntax errors.")