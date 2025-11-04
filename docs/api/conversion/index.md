# Conversion API

Bidirectional type conversion between Python objects and Terraform's type system (CTY).

!!! warning "Advanced API - Internal Use"
    **Most users don't need to use the conversion API directly.** Pyvider automatically handles all data conversion between Python types and Terraform's wire format. This API is documented for advanced use cases like debugging, custom type handling, or integration with other systems.

## Overview

The conversion layer handles all data transformation between:
- **Python native types** (str, int, dict, list, etc.) ↔ **CTY values** (Terraform's type system)
- **Protocol buffers** (DynamicValue) ↔ **CTY values**
- **Pyvider schemas** (PvsSchema) ↔ **Protocol buffers** (Schema)

When you write provider code, Pyvider automatically:
1. Unmarshals incoming protocol buffer messages to CTY values
2. Converts CTY values to Python native types matching your `@attrs.define` classes
3. Converts Python native types back to CTY values
4. Marshals CTY values to protocol buffer messages

## Available Functions

```python
from pyvider.conversion import (
    # CTY to Python conversion
    cty_to_native,
    infer_cty_type_from_raw,

    # Protocol buffer marshaling
    marshal,
    unmarshal,
    marshal_value,
    unmarshal_value,

    # Schema conversion
    pvs_schema_to_proto,

    # Utility functions
    unify_and_validate_list_of_objects,
)
```

## Core Functions

### `cty_to_native(cty_value) -> Any`

Converts a CTY value to its Python native equivalent.

**Parameters:**
- `cty_value` - A CTY value from the `pyvider.cty` package

**Returns:**
- Python native type (str, int, float, bool, dict, list, None)

**Example:**
```python
from pyvider.conversion import cty_to_native
from pyvider.cty import CtyString, CtyNumber, CtyObject

# This is handled automatically by Pyvider, but for reference:
string_val = cty_to_native(CtyString("hello"))  # -> "hello"
number_val = cty_to_native(CtyNumber(42))       # -> 42

# Nested structures
obj_val = cty_to_native(CtyObject({
    "name": CtyString("test"),
    "count": CtyNumber(5)
}))
# -> {"name": "test", "count": 5}
```

!!! note "CTY Type System"
    The CTY (Terraform's type system) types come from the `pyvider.cty` package, which is an internal dependency. You should not import from `pyvider.cty` or `pyvider-cty` directly unless you're doing advanced debugging or integration work.

### `infer_cty_type_from_raw(value) -> CtyType`

Infers the appropriate CTY type from a raw Python value.

**Parameters:**
- `value` - Any Python value

**Returns:**
- A CTY type that can represent the value

**Example:**
```python
from pyvider.conversion import infer_cty_type_from_raw

# Infer types from Python values
str_type = infer_cty_type_from_raw("hello")       # -> CtyString type
num_type = infer_cty_type_from_raw(42)            # -> CtyNumber type
list_type = infer_cty_type_from_raw([1, 2, 3])    # -> CtyList(CtyNumber) type
```

## Protocol Buffer Marshaling

### `marshal(cty_value, cty_type) -> DynamicValue`

Marshals a CTY value into a protocol buffer `DynamicValue` for transmission to Terraform.

**Parameters:**
- `cty_value` - CTY value to marshal
- `cty_type` - CTY type of the value

**Returns:**
- Protocol buffer `DynamicValue`

**Use case:** Internal framework function called when sending data to Terraform.

### `unmarshal(dynamic_value, cty_type) -> CtyValue`

Unmarshals a protocol buffer `DynamicValue` into a CTY value.

**Parameters:**
- `dynamic_value` - Protocol buffer `DynamicValue` from Terraform
- `cty_type` - Expected CTY type

**Returns:**
- CTY value

**Use case:** Internal framework function called when receiving data from Terraform.

### `marshal_value(cty_value, cty_type) -> DynamicValue`

Function-specific variant of marshal for function calls.

### `unmarshal_value(dynamic_value, cty_type) -> CtyValue`

Function-specific variant of unmarshal for function calls.

## Schema Conversion

### `pvs_schema_to_proto(pvs_schema) -> proto.Schema`

Converts a Pyvider schema to a protocol buffer schema for transmission to Terraform.

**Parameters:**
- `pvs_schema` - Pyvider schema (from `s_resource()`, `s_data_source()`, etc.)

**Returns:**
- Protocol buffer `Schema` message

**Example:**
```python
from pyvider.schema import s_resource, a_str, a_num
from pyvider.conversion import pvs_schema_to_proto

# Define a Pyvider schema
pvs_schema = s_resource({
    "name": a_str(required=True),
    "count": a_num(default=1)
})

# Convert to protocol buffer format (done automatically by framework)
proto_schema = pvs_schema_to_proto(pvs_schema)
```

## Utility Functions

### `unify_and_validate_list_of_objects(objects_list, object_type) -> list`

Validates and unifies a list of objects to ensure consistent structure.

**Parameters:**
- `objects_list` - List of dictionary objects
- `object_type` - Expected CTY object type

**Returns:**
- Validated and unified list of objects

**Use case:** Internal validation for list attributes with object elements.

## How Pyvider Uses Conversion

Here's what happens behind the scenes when your resource is called:

```python
@register_resource("server")
class Server(BaseResource):
    @attrs.define
    class Config:
        name: str
        count: int = 1

    @attrs.define
    class State:
        id: str
        name: str
        count: int

    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        # 1. Terraform sends protocol buffer DynamicValue
        # 2. Pyvider unmarshals it: unmarshal(dynamic_value, cty_type) -> CtyValue
        # 3. Pyvider converts: cty_to_native(cty_value) -> dict
        # 4. Pyvider creates: Config(**dict) -> ctx.config

        # Your code receives ctx.config as a properly typed Config instance
        server = await create_server(ctx.config.name, ctx.config.count)

        # 5. You return State instance
        state = State(id=server.id, name=server.name, count=server.count)

        # 6. Pyvider converts: attrs.asdict(state) -> dict
        # 7. Pyvider converts: native_to_cty(dict, cty_type) -> CtyValue (internal)
        # 8. Pyvider marshals: marshal(cty_value, cty_type) -> DynamicValue
        # 9. Pyvider sends protocol buffer to Terraform

        return state, None
```

**You write steps 4-5. Pyvider handles steps 1-3 and 6-9 automatically.**

## Advanced Use Cases

### Debugging Data Conversion

If you need to debug what's being sent/received:

```python
from pyvider.conversion import cty_to_native, marshal
import structlog

logger = structlog.get_logger()

@register_resource("server")
class Server(BaseResource):
    async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
        # Log the config as it was received
        logger.debug(
            "Received config",
            config=attrs.asdict(ctx.config),
            config_type=type(ctx.config).__name__
        )

        # ... your implementation ...

        state = State(id="srv-123", name=ctx.config.name)

        # Log the state being returned
        logger.debug(
            "Returning state",
            state=attrs.asdict(state),
            state_type=type(state).__name__
        )

        return state, None
```

### Custom Type Handling

For most cases, attrs with Python type hints is sufficient. However, if you need custom serialization:

```python
from datetime import datetime
import attrs

@attrs.define
class ServerState:
    id: str
    created_at: datetime  # datetime will be auto-converted to ISO string

    @created_at.default
    def _default_created_at(self):
        return datetime.utcnow()
```

Pyvider automatically handles common Python types like `datetime`, `Decimal`, `UUID`, etc.

## Type Mappings

| Python Type | CTY Type | Example |
|-------------|----------|---------|
| `str` | `CtyString` | `"hello"` |
| `int` | `CtyNumber` | `42` |
| `float` | `CtyNumber` | `3.14` |
| `bool` | `CtyBool` | `True` |
| `None` | `CtyNull` | `None` |
| `dict` | `CtyObject` | `{"key": "value"}` |
| `list` | `CtyList` or `CtyTuple` | `[1, 2, 3]` |
| `set` | `CtySet` | `{1, 2, 3}` |
| `datetime` | `CtyString` (ISO 8601) | `"2024-01-15T10:30:00Z"` |
| `UUID` | `CtyString` | `"550e8400-e29b-41d4-a716-446655440000"` |
| `Decimal` | `CtyNumber` | `123.45` |

## Known Limitations

1. **No circular references**: CTY values cannot contain circular references
2. **No mixed-type lists**: All list elements must be the same type
3. **Map keys must be strings**: CTY maps only support string keys
4. **No arbitrary Python objects**: Only JSON-compatible types are supported

## Related Documentation

- [Schema System](../../explanation/schema-system.md) - Define schemas without touching conversion
- [Component Model](../../explanation/component-model.md) - How components use conversion internally
- [Creating Resources](../../guides/building-components/creating-resources.md) - Practical examples without conversion code

## Module Reference
