# Creating Functions

This guide shows you how to create provider functions in Pyvider. Functions are callable operations that transform or validate data in Terraform configurations.

## What is a Provider Function?

Provider functions in Terraform:
- **Transform data** (string manipulation, JSON parsing, encoding)
- **Validate inputs** (check formats, constraints)
- **Perform calculations** (hashing, math operations)
- **Are pure functions** (no side effects, same input = same output)

## Basic Function Example

Here's a simple function that converts strings to uppercase:

```python
from pyvider.functions import register_function, BaseFunction
from pyvider.schema import s_function, a_str, PvsSchema

@register_function("upper")
class UpperFunction(BaseFunction):
    """Converts a string to uppercase."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define function signature."""
        return s_function(
            parameters=[
                a_str(description="Input string to convert"),
            ],
            return_type=a_str(description="Uppercase string"),
        )

    async def call(self, input: str) -> str:
        """Execute the function."""
        return input.upper()
```

## Function Components

### 1. Schema Definition

Define parameters and return type:

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_function(
        parameters=[
            a_str(description="First parameter"),
            a_num(description="Second parameter"),
        ],
        return_type=a_bool(description="Result"),
    )
```

### 2. Implementation

Implement the `call()` method:

```python
async def call(self, param1: str, param2: int) -> bool:
    """Execute function logic."""
    # Your logic here
    return True
```

## Complete Examples

### String Manipulation Function

```python
from pyvider.functions import register_function, BaseFunction
from pyvider.schema import s_function, a_str, PvsSchema

@register_function("join")
class JoinFunction(BaseFunction):
    """Joins strings with a separator."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            parameters=[
                a_list(a_str(), description="Strings to join"),
                a_str(description="Separator"),
            ],
            return_type=a_str(description="Joined string"),
        )

    async def call(self, strings: list[str], separator: str) -> str:
        """Join strings."""
        return separator.join(strings)
```

### Hash Function

```python
from pyvider.functions import register_function, BaseFunction
from pyvider.schema import s_function, a_str, PvsSchema
import hashlib

@register_function("sha256")
class SHA256Function(BaseFunction):
    """Computes SHA256 hash of a string."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            parameters=[
                a_str(description="Input string to hash"),
            ],
            return_type=a_str(description="SHA256 hex digest"),
        )

    async def call(self, input: str) -> str:
        """Compute SHA256 hash."""
        return hashlib.sha256(input.encode()).hexdigest()
```

### JSON Parsing Function

```python
from pyvider.functions import register_function, BaseFunction
from pyvider.schema import s_function, a_str, a_dyn, PvsSchema
import json

@register_function("parse_json")
class ParseJSONFunction(BaseFunction):
    """Parses a JSON string."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            parameters=[
                a_str(description="JSON string to parse"),
            ],
            return_type=a_dyn(description="Parsed JSON data"),
        )

    async def call(self, json_str: str) -> dict | list:
        """Parse JSON string."""
        return json.loads(json_str)
```

### Validation Function

```python
from pyvider.functions import register_function, BaseFunction
from pyvider.schema import s_function, a_str, a_bool, PvsSchema
import re

@register_function("is_valid_email")
class ValidateEmailFunction(BaseFunction):
    """Validates an email address."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            parameters=[
                a_str(description="Email address to validate"),
            ],
            return_type=a_bool(description="Whether email is valid"),
        )

    async def call(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
```

### Math Function

```python
from pyvider.functions import register_function, BaseFunction
from pyvider.schema import s_function, a_num, PvsSchema

@register_function("clamp")
class ClampFunction(BaseFunction):
    """Clamps a number between min and max values."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            parameters=[
                a_num(description="Input value"),
                a_num(description="Minimum value"),
                a_num(description="Maximum value"),
            ],
            return_type=a_num(description="Clamped value"),
        )

    async def call(self, value: float, min_val: float, max_val: float) -> float:
        """Clamp value between min and max."""
        return max(min_val, min(max_val, value))
```

## Using Functions in Terraform

After creating functions, users can call them in Terraform:

```hcl
# Use the uppercase function
locals {
  name = provider::local::upper("hello world")
  # Result: "HELLO WORLD"
}

# Use the join function
locals {
  tags = provider::mycloud::join(["prod", "web", "api"], "-")
  # Result: "prod-web-api"
}

# Use the hash function
resource "mycloud_secret" "api_key" {
  name  = "api-key"
  hash  = provider::mycloud::sha256(var.api_key)
}

# Use validation function
variable "admin_email" {
  type = string
  validation {
    condition     = provider::mycloud::is_valid_email(var.admin_email)
    error_message = "Must be a valid email address"
  }
}
```

## Function Best Practices

1. **Keep functions pure** - No side effects, same input always returns same output
2. **Handle errors gracefully** - Validate inputs and return meaningful errors
3. **Document thoroughly** - Clear parameter and return descriptions
4. **Make functions fast** - Users may call functions many times
5. **Use appropriate types** - Match Terraform's type system

## Error Handling

Functions should validate inputs and raise clear errors:

```python
from pyvider.functions import register_function, BaseFunction
from pyvider.exceptions import FunctionError
from pyvider.schema import s_function, a_num, PvsSchema

@register_function("divide")
class DivideFunction(BaseFunction):
    """Divides two numbers."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            parameters=[
                a_num(description="Numerator"),
                a_num(description="Denominator"),
            ],
            return_type=a_num(description="Result"),
        )

    async def call(self, numerator: float, denominator: float) -> float:
        """Divide two numbers."""
        if denominator == 0:
            raise FunctionError("Cannot divide by zero")
        return numerator / denominator
```

## Complex Return Types

Functions can return complex data structures:

```python
from pyvider.functions import register_function, BaseFunction
from pyvider.schema import s_function, a_str, a_obj, a_num, a_bool, PvsSchema

@register_function("parse_url")
class ParseURLFunction(BaseFunction):
    """Parses a URL into components."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            parameters=[
                a_str(description="URL to parse"),
            ],
            return_type=a_obj({
                "scheme": a_str(description="URL scheme"),
                "host": a_str(description="Hostname"),
                "port": a_num(description="Port number"),
                "path": a_str(description="URL path"),
                "secure": a_bool(description="Whether HTTPS"),
            }, description="Parsed URL components"),
        )

    async def call(self, url: str) -> dict:
        """Parse URL."""
        from urllib.parse import urlparse
        parsed = urlparse(url)

        return {
            "scheme": parsed.scheme,
            "host": parsed.hostname or "",
            "port": parsed.port or (443 if parsed.scheme == "https" else 80),
            "path": parsed.path or "/",
            "secure": parsed.scheme == "https",
        }
```

## Variadic Functions

Functions with variable number of arguments:

```python
from pyvider.functions import register_function, BaseFunction
from pyvider.schema import s_function, a_str, PvsSchema

@register_function("concat")
class ConcatFunction(BaseFunction):
    """Concatenates any number of strings."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            parameters=[
                a_str(description="String to concatenate"),
            ],
            variadic_parameter=a_str(description="Additional strings"),
            return_type=a_str(description="Concatenated result"),
        )

    async def call(self, first: str, *rest: str) -> str:
        """Concatenate all strings."""
        return first + "".join(rest)
```

## Testing Functions

Test functions independently:

```python
import pytest
from my_provider.functions import UpperFunction

@pytest.mark.asyncio
async def test_upper_function():
    """Test uppercase function."""
    func = UpperFunction()

    result = await func.call("hello")
    assert result == "HELLO"

    result = await func.call("Mixed Case")
    assert result == "MIXED CASE"

@pytest.mark.asyncio
async def test_divide_function():
    """Test division function."""
    func = DivideFunction()

    result = await func.call(10, 2)
    assert result == 5.0

    with pytest.raises(FunctionError, match="divide by zero"):
        await func.call(10, 0)
```

## See Also

- [Schema System](../../explanation/schema-system.md) - Understanding schemas
- [Function API](../../api/functions.md) - BaseFunction reference
- [Best Practices](../production/best-practices.md) - Production patterns
- [Testing Functions](../development/testing-providers.md) - Testing strategies
