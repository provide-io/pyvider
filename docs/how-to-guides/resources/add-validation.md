# How to Add Validation

Add configuration validation to your resources to catch errors early and provide helpful feedback to users.

---

## Quick Example

```python
async def _validate_config(self, config: ServerConfig) -> list[str]:
    """Validate configuration before applying."""
    errors = []

    if len(config.name) < 3:
        errors.append("Name must be at least 3 characters")

    if config.port < 1 or config.port > 65535:
        errors.append("Port must be between 1 and 65535")

    return errors
```

---

## Validation Patterns

### String Length

```python
async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    # Minimum length
    if len(config.name) < 3:
        errors.append("Name must be at least 3 characters")

    # Maximum length
    if len(config.description) > 256:
        errors.append("Description cannot exceed 256 characters")

    # Exact length
    if len(config.code) != 8:
        errors.append("Code must be exactly 8 characters")

    return errors
```

### Format Validation

```python
import re

async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    # Email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, config.email):
        errors.append("Invalid email format")

    # URL format
    url_pattern = r'^https?://.+'
    if not re.match(url_pattern, config.webhook_url):
        errors.append("URL must start with http:// or https://")

    # Alphanumeric only
    if not config.identifier.isalnum():
        errors.append("Identifier must be alphanumeric")

    return errors
```

### Numeric Ranges

```python
async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    # Range check
    if config.port < 1024 or config.port > 65535:
        errors.append("Port must be between 1024 and 65535")

    # Minimum value
    if config.timeout < 1:
        errors.append("Timeout must be at least 1 second")

    # Maximum value
    if config.max_connections > 10000:
        errors.append("Max connections cannot exceed 10000")

    # Positive numbers only
    if config.retry_count < 0:
        errors.append("Retry count must be non-negative")

    return errors
```

### Enum/Choice Validation

```python
async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    # Valid choices
    valid_regions = ["us-east-1", "us-west-2", "eu-west-1"]
    if config.region not in valid_regions:
        errors.append(f"Region must be one of: {', '.join(valid_regions)}")

    # Valid protocols
    valid_protocols = {"http", "https", "tcp", "udp"}
    if config.protocol not in valid_protocols:
        errors.append(f"Protocol must be one of: {', '.join(valid_protocols)}")

    return errors
```

### Path Security

```python
async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    # Prevent path traversal
    if ".." in config.path:
        errors.append("Path cannot contain '..'")

    # Require absolute path
    from pathlib import Path
    if not Path(config.path).is_absolute():
        errors.append("Path must be absolute")

    # Restrict to specific directory
    allowed_base = Path("/var/app")
    try:
        resolved = Path(config.path).resolve()
        if not str(resolved).startswith(str(allowed_base)):
            errors.append(f"Path must be under {allowed_base}")
    except Exception:
        errors.append("Invalid path format")

    return errors
```

### List Validation

```python
async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    # Non-empty list
    if not config.tags:
        errors.append("At least one tag is required")

    # List size limits
    if len(config.items) > 100:
        errors.append("Cannot have more than 100 items")

    # Validate each item
    for item in config.allowed_ips:
        if not is_valid_ip(item):
            errors.append(f"Invalid IP address: {item}")

    # No duplicates
    if len(config.names) != len(set(config.names)):
        errors.append("Names must be unique")

    return errors
```

### Conditional Validation

```python
async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    # If-then validation
    if config.use_ssl and not config.certificate_path:
        errors.append("Certificate path required when SSL is enabled")

    # Mutual exclusivity
    if config.use_password and config.use_key:
        errors.append("Cannot use both password and key authentication")

    # Required together
    if config.username and not config.password:
        errors.append("Password required when username is provided")

    return errors
```

### Cross-Field Validation

```python
async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    # Compare fields
    if config.min_size > config.max_size:
        errors.append("Min size cannot be greater than max size")

    # Date ranges
    if config.start_date and config.end_date:
        if config.start_date >= config.end_date:
            errors.append("Start date must be before end date")

    # Port ranges
    if config.port_range_start > config.port_range_end:
        errors.append("Invalid port range")

    return errors
```

---

## Async Validation

### API Validation

Validate against external APIs:

```python
import httpx

async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    # Check if username is available
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://api.example.com/users/{config.username}/exists"
            )
            if response.json()["exists"]:
                errors.append(f"Username '{config.username}' is already taken")
        except Exception as e:
            errors.append(f"Failed to validate username: {e}")

    return errors
```

### Database Validation

```python
async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    # Check if email is unique
    async with get_db_connection() as db:
        exists = await db.fetchval(
            "SELECT EXISTS(SELECT 1 FROM users WHERE email = $1)",
            config.email
        )
        if exists:
            errors.append(f"Email '{config.email}' is already registered")

    return errors
```

---

## Best Practices

### 1. Clear Error Messages

```python
# Bad
errors.append("Invalid input")

# Good
errors.append("Name must be 3-50 characters long")
```

### 2. Validate Early

```python
async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    # Check required fields first
    if not config.name:
        errors.append("Name is required")
        return errors  # Stop early if critical field missing

    # Then validate format
    if len(config.name) < 3:
        errors.append("Name must be at least 3 characters")

    return errors
```

### 3. Return All Errors

```python
async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    # Collect all errors instead of returning after first one
    if len(config.name) < 3:
        errors.append("Name too short")

    if not config.email:
        errors.append("Email required")

    if config.port < 1024:
        errors.append("Port too low")

    # Return all errors at once
    return errors
```

### 4. Use Helper Functions

```python
def is_valid_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def is_valid_url(url: str) -> bool:
    import re
    pattern = r'^https?://.+'
    return bool(re.match(pattern, url))

async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    if not is_valid_email(config.email):
        errors.append("Invalid email format")

    if not is_valid_url(config.webhook):
        errors.append("Invalid webhook URL")

    return errors
```

### 5. Consider Performance

```python
async def _validate_config(self, config: Config) -> list[str]:
    errors = []

    # Quick checks first (no API calls)
    if not config.name:
        errors.append("Name required")
        return errors

    # Expensive checks only if basic validation passes
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/validate/{config.name}")
        if not response.json()["valid"]:
            errors.append("Name not available")

    return errors
```

---

## Testing Validation

```python
import pytest
from my_provider.resources.server import Server, ServerConfig

@pytest.mark.asyncio
async def test_name_validation():
    server = Server()

    # Test too short
    config = ServerConfig(name="ab", port=8080)
    errors = await server._validate_config(config)
    assert "Name must be at least 3 characters" in errors

    # Test valid
    config = ServerConfig(name="server1", port=8080)
    errors = await server._validate_config(config)
    assert len(errors) == 0

@pytest.mark.asyncio
async def test_port_validation():
    server = Server()

    # Test invalid port
    config = ServerConfig(name="server1", port=99999)
    errors = await server._validate_config(config)
    assert "Port must be between" in errors[0]
```

---

## See Also

- [Create a Resource](create-resource.md) - Resource basics
- [Building Your First Resource](../../tutorials/building-your-first-resource.md) - Step-by-step tutorial
- [Resource Lifecycle Reference](../../reference/resource-lifecycle.md) - Complete API
- [Testing Resources](../../guides/development/testing-providers.md) - Testing validation
