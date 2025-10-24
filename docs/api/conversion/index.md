# Conversion API

Bidirectional type conversion between Python objects and Terraform's type system (CTY).

## Overview

The conversion layer handles all data transformation between:
- **Python types** ↔ **CTY values** (Terraform's type system)
- **Protocol buffers** ↔ **Python objects**
- **Schema definitions** ↔ **Protocol schema**

Most users won't need to interact with the conversion layer directly, as Pyvider handles conversions automatically. However, this module is useful for advanced use cases and custom type implementations.

## Core Functions

### `cty_to_native(cty_value) -> Any`

Converts a CTY value to its Python native equivalent:

```python
from pyvider.conversion import cty_to_native
from pyvider_cty import CtyString, CtyNumber, CtyList

# Simple conversions
string_val = cty_to_native(CtyString("hello"))  # -> "hello"
number_val = cty_to_native(CtyNumber(42))       # -> 42
bool_val = cty_to_native(CtyBool(True))        # -> True

# Collection conversions
list_val = cty_to_native(CtyList([CtyString("a"), CtyString("b")]))
# -> ["a", "b"]

map_val = cty_to_native(CtyMap({
    "key1": CtyString("value1"),
    "key2": CtyNumber(123)
}))
# -> {"key1": "value1", "key2": 123}
```

### `native_to_cty(value, cty_type) -> CtyValue`

Converts Python native values to CTY:

```python
from pyvider.conversion import native_to_cty
from pyvider_cty import CtyString, CtyList, CtyObject

# Simple conversion
cty_str = native_to_cty("hello", CtyString())  # -> CtyString("hello")

# List conversion
cty_list = native_to_cty(
    [1, 2, 3],
    CtyList(CtyNumber())
)  # -> CtyList([CtyNumber(1), CtyNumber(2), CtyNumber(3)])

# Object conversion
cty_obj = native_to_cty(
    {"name": "test", "count": 5},
    CtyObject({
        "name": CtyString(),
        "count": CtyNumber()
    })
)
```

## Complex Nested Structures

### Converting Nested Objects

```python
from pyvider.conversion import cty_to_native, native_to_cty
from pyvider_cty import CtyObject, CtyList, CtyString, CtyNumber

# Define a complex nested structure type
server_type = CtyObject({
    "name": CtyString(),
    "config": CtyObject({
        "cpu": CtyNumber(),
        "memory": CtyNumber(),
        "disks": CtyList(CtyObject({
            "device": CtyString(),
            "size_gb": CtyNumber()
        }))
    }),
    "tags": CtyMap(CtyString())
})

# Python data
server_data = {
    "name": "web-server",
    "config": {
        "cpu": 4,
        "memory": 16,
        "disks": [
            {"device": "/dev/sda", "size_gb": 100},
            {"device": "/dev/sdb", "size_gb": 500}
        ]
    },
    "tags": {
        "environment": "production",
        "team": "platform"
    }
}

# Convert to CTY
cty_server = native_to_cty(server_data, server_type)

# Convert back to native
native_server = cty_to_native(cty_server)
assert native_server == server_data
```

## Handling Special Values

### Unknown Values

During Terraform planning, some values may be unknown:

```python
from pyvider.conversion import cty_to_native, is_unknown
from pyvider_cty import CtyUnknown, CtyString

# Check if a value is unknown
unknown_val = CtyUnknown(CtyString())
if is_unknown(unknown_val):
    # Handle unknown value
    # Usually, defer computation until apply phase
    pass

# Convert unknown (returns None by default)
native_val = cty_to_native(unknown_val)  # -> None
```

### Null Values

```python
from pyvider.conversion import cty_to_native, is_null
from pyvider_cty import CtyNull

# Check if a value is null
null_val = CtyNull()
if is_null(null_val):
    # Handle null value
    pass

# Convert null
native_val = cty_to_native(null_val)  # -> None
```

## Custom Type Converters

For custom types not covered by default conversions:

```python
from pyvider.conversion import register_converter
from datetime import datetime
from pyvider_cty import CtyString

class DateTimeConverter:
    """Custom converter for datetime objects."""

    @staticmethod
    def to_cty(value: datetime) -> CtyString:
        """Convert datetime to CTY string."""
        return CtyString(value.isoformat())

    @staticmethod
    def from_cty(cty_value: CtyString) -> datetime:
        """Convert CTY string to datetime."""
        return datetime.fromisoformat(cty_to_native(cty_value))

# Register the converter
register_converter(datetime, DateTimeConverter)

# Now datetime objects can be converted
now = datetime.now()
cty_time = native_to_cty(now, CtyString())
native_time = cty_to_native(cty_time)
```

## Schema Conversion

Converting between Pyvider schemas and protocol schemas:

```python
from pyvider.conversion import SchemaAdapter
from pyvider.schema import s_resource, a_str, a_num

# Create a Pyvider schema
pvs_schema = s_resource({
    "name": a_str(required=True),
    "count": a_num(default=1)
})

# Convert to protocol schema
adapter = SchemaAdapter()
proto_schema = adapter.to_proto(pvs_schema)

# Convert back to Pyvider schema
pvs_schema_back = adapter.from_proto(proto_schema)
```

## Protocol Buffer Marshaling

For direct protocol buffer handling:

```python
from pyvider.conversion import Marshaler
from pyvider.protocols.tfprotov6.protobuf import tfplugin6_pb2

# Create a marshaler
marshaler = Marshaler()

# Marshal Python data to protocol buffer
data = {"name": "test", "enabled": True}
proto_value = marshaler.marshal(data)

# Unmarshal protocol buffer to Python
native_data = marshaler.unmarshal(proto_value)
```

## Error Handling

```python
from pyvider.conversion import ConversionError

try:
    # Attempt conversion
    result = native_to_cty("not a number", CtyNumber())
except ConversionError as e:
    print(f"Conversion failed: {e.message}")
    print(f"Details: {e.details}")
```

## Performance Considerations

### Caching Converted Schemas

```python
from functools import lru_cache
from pyvider.conversion import SchemaAdapter

@lru_cache(maxsize=128)
def get_converted_schema(schema_hash):
    """Cache converted schemas for performance."""
    adapter = SchemaAdapter()
    return adapter.to_proto(build_schema())
```

### Batch Conversions

```python
from pyvider.conversion import batch_convert

# Convert multiple values efficiently
values = [1, 2, 3, 4, 5]
cty_values = batch_convert(values, CtyNumber())
```

## Common Patterns

### Resource State Conversion

```python
class MyResource(BaseResource):
    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        # Automatic conversion happens here
        # ctx.config is already converted from CTY to Python

        # Do work...
        result = await self.api.create(...)

        # Return state - will be converted to CTY automatically
        return State(
            id=result.id,
            name=ctx.config.name
        ), None
```

### Data Source Output

```python
class MyDataSource(BaseDataSource):
    async def read(self, config: Config) -> State:
        # Fetch data
        data = await self.api.list_items()

        # Complex conversion handled automatically
        return State(
            items=[
                {"id": item.id, "name": item.name}
                for item in data
            ]
        )
```

## Testing Conversions

```python
import pytest
from pyvider.conversion import cty_to_native, native_to_cty
from pyvider_cty import CtyString, CtyList

def test_round_trip_conversion():
    """Test that conversions are reversible."""
    original = ["a", "b", "c"]
    cty_type = CtyList(CtyString())

    # Convert to CTY and back
    cty_val = native_to_cty(original, cty_type)
    result = cty_to_native(cty_val)

    assert result == original

def test_nested_conversion():
    """Test nested structure conversion."""
    data = {
        "users": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]
    }

    cty_type = CtyObject({
        "users": CtyList(CtyObject({
            "name": CtyString(),
            "age": CtyNumber()
        }))
    })

    cty_val = native_to_cty(data, cty_type)
    result = cty_to_native(cty_val)

    assert result == data
```

## Related Documentation

- [Schema System](../../core-concepts/schema-system.md) - Schema definition and types
- [Component Model](../../core-concepts/component-model.md) - How components use conversion
- [Creating Resources](../../guides/creating-resources.md) - Practical conversion examples

## Module Reference

::: pyvider.conversion
    options:
      show_source: true
      show_root_heading: true
      members_order: source
      show_if_no_docstring: false
      filters:
        - "!^_"
        - "^__init__$"
