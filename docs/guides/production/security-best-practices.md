# Security Best Practices

Building secure Terraform providers is critical as they often handle sensitive credentials, infrastructure access, and confidential data. This guide covers security best practices for Pyvider providers.

## Table of Contents

- [Secret Management](#secret-management)
- [Input Validation](#input-validation)
- [State Security](#state-security)
- [API Authentication](#api-authentication)
- [Logging and Observability](#logging-and-observability)
- [Dependency Security](#dependency-security)
- [Error Handling](#error-handling)
- [Network Security](#network-security)

---

## Secret Management

### Never Hardcode Secrets

**Bad:**
```python
@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    def __init__(self):
        super().__init__(...)
        self.api_key = "sk_live_12345..."  # NEVER DO THIS
```

**Good:**
```python
@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    async def configure(self, config: dict) -> None:
        await super().configure(config)
        # API key comes from Terraform configuration
        self.api_key = config["api_key"]
```

### Mark Sensitive Attributes

Always mark credentials and secrets as sensitive in your schema:

```python
def _build_schema(self) -> PvsSchema:
    return s_provider({
        "api_key": a_str(
            required=True,
            sensitive=True,  # Prevents logging and display
            description="API authentication key"
        ),
        "api_secret": a_str(
            required=True,
            sensitive=True,
            description="API secret"
        ),
        "password": a_str(
            sensitive=True,
            description="Database password"
        ),
    })
```

When marked as `sensitive=True`:
- Value is masked in Terraform output
- Not logged by Pyvider
- Shown as `(sensitive value)` in plans

### Use Environment Variables

Encourage users to use environment variables for secrets:

```hcl
# Terraform configuration
provider "mycloud" {
  api_key = var.api_key  # From TF_VAR_api_key environment variable
}

variable "api_key" {
  type      = string
  sensitive = true
}
```

### Private State for Sensitive Data

Use private state for data that shouldn't be in Terraform state:

```python
from pyvider.resources import BaseResource
from pyvider.resources.private_state import PrivateState

@register_resource("database")
class Database(BaseResource):
    async def _create_apply(
        self,
        ctx: ResourceContext
    ) -> tuple[State | None, dict | None]:
        # Create database
        db = await self.create_database(ctx.config)

        # Public state (visible in terraform.tfstate)
        public_state = State(
            id=db.id,
            endpoint=db.endpoint,
            port=db.port,
        )

        # Private state (encrypted, not in terraform.tfstate)
        private_state = {
            "master_password": db.master_password,
            "internal_token": db.internal_token,
        }

        return public_state, private_state
```

---

## Input Validation

### Validate All Inputs

Never trust user input. Always validate:

```python
def _build_schema(self) -> PvsSchema:
    return s_provider({
        "api_endpoint": a_str(
            required=True,
            validators=[
                lambda x: x.startswith("https://") or "API endpoint must use HTTPS",
                lambda x: len(x) < 2048 or "URL too long",
            ]
        ),
        "port": a_num(
            validators=[
                lambda x: 1 <= x <= 65535 or "Port must be 1-65535",
            ]
        ),
        "region": a_str(
            validators=[
                lambda x: x in ["us-east-1", "us-west-2", "eu-central-1"]
                          or "Invalid region",
            ]
        ),
    })
```

### Sanitize String Inputs

Protect against injection attacks:

```python
import re

def validate_resource_name(name: str) -> str | bool:
    """Validate resource name is safe."""
    # Only allow alphanumeric, hyphens, underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        return "Name must contain only letters, numbers, hyphens, and underscores"

    # Prevent overly long names
    if len(name) > 255:
        return "Name must be 255 characters or less"

    return True

@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "name": a_str(
            required=True,
            validators=[validate_resource_name]
        ),
    })
```

### Prevent Path Traversal

When working with file paths:

```python
from pathlib import Path

async def _create_apply(self, ctx: ResourceContext):
    # Get user-provided path
    requested_path = Path(ctx.config.path)

    # Prevent path traversal attacks
    if ".." in str(requested_path):
        raise ValueError("Path cannot contain '..'")

    # Resolve to absolute path
    abs_path = requested_path.resolve()

    # Ensure it's within allowed directory
    allowed_base = Path("/var/data").resolve()
    if not str(abs_path).startswith(str(allowed_base)):
        raise ValueError(f"Path must be within {allowed_base}")

    # Now safe to use
    abs_path.write_text(ctx.config.content)
```

### Limit Input Sizes

Prevent denial-of-service via large inputs:

```python
def _build_schema(self) -> PvsSchema:
    return s_resource({
        "content": a_str(
            required=True,
            validators=[
                # Max 1MB of content
                lambda x: len(x) <= 1_000_000 or "Content too large (max 1MB)",
            ]
        ),
        "tags": a_list(
            a_str(),
            validators=[
                # Max 100 tags
                lambda x: len(x) <= 100 or "Too many tags (max 100)",
            ]
        ),
    })
```

---

## State Security

### Encrypt Sensitive State Data

Use private state for sensitive information:

```python
# Private state is automatically encrypted by Pyvider
async def _create_apply(self, ctx):
    credentials = await self.generate_credentials()

    state = State(id="resource-123", endpoint="https://api.example.com")

    # Store credentials in encrypted private state
    private = {
        "access_key": credentials.access_key,
        "secret_key": credentials.secret_key,
    }

    return state, private
```

### Avoid Storing Secrets in State

When possible, avoid storing secrets entirely:

```python
# Bad - Secret in state
state = State(
    id="db-123",
    password="supersecret"  # Visible in terraform.tfstate
)

# Good - Reference to secret manager
state = State(
    id="db-123",
    password_secret_id="arn:aws:secretsmanager:..."  # Reference only
)
```

### Validate State on Read

Always validate state hasn't been tampered with:

```python
async def read(self, ctx: ResourceContext) -> State | None:
    if not ctx.state:
        return None

    # Verify the resource actually exists
    try:
        current = await self.api.get_resource(ctx.state.id)
    except ResourceNotFoundError:
        logger.warning(
            "Resource not found during read - may have been deleted outside Terraform",
            resource_id=ctx.state.id
        )
        return None

    # Verify critical attributes match
    if current.type != ctx.state.type:
        logger.error(
            "Resource type mismatch - possible state corruption",
            expected=ctx.state.type,
            actual=current.type
        )
        raise StateCorruptionError("Resource type has changed")

    return State(...)
```

---

## API Authentication

### Use OAuth 2.0 When Possible

```python
import httpx

@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    async def configure(self, config: dict) -> None:
        await super().configure(config)

        # Use OAuth 2.0 with token refresh
        self.oauth_client = OAuth2Client(
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            token_url=config["token_url"],
        )

        # Get initial token
        self.access_token = await self.oauth_client.get_token()

    async def _api_request(self, method: str, path: str, **kwargs):
        """Make authenticated API request with automatic token refresh."""
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"

        try:
            response = await self.http_client.request(
                method, path, headers=headers, **kwargs
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                # Token expired - refresh and retry
                self.access_token = await self.oauth_client.refresh_token()
                headers["Authorization"] = f"Bearer {self.access_token}"
                response = await self.http_client.request(
                    method, path, headers=headers, **kwargs
                )
                response.raise_for_status()
                return response
            raise
```

### Validate API Certificates

Always verify SSL/TLS certificates:

```python
async def configure(self, config: dict) -> None:
    await super().configure(config)

    # Default: Verify SSL certificates
    verify_ssl = config.get("verify_ssl", True)

    if not verify_ssl:
        logger.warning(
            "SSL verification disabled - this is insecure and should only be "
            "used in development environments"
        )

    self.http_client = httpx.AsyncClient(
        verify=verify_ssl,  # Verify by default
        timeout=30.0,
    )
```

### Implement Request Signing

For APIs that require request signing:

```python
import hashlib
import hmac
from datetime import datetime

def sign_request(
    method: str,
    url: str,
    secret_key: str,
    timestamp: datetime | None = None
) -> str:
    """Sign API request with HMAC-SHA256."""
    if timestamp is None:
        timestamp = datetime.utcnow()

    # Create canonical request
    canonical = f"{method}\n{url}\n{timestamp.isoformat()}"

    # Sign with HMAC-SHA256
    signature = hmac.new(
        secret_key.encode(),
        canonical.encode(),
        hashlib.sha256
    ).hexdigest()

    return signature
```

---

## Logging and Observability

### Never Log Sensitive Data

```python
from provide.foundation import logger

# Bad - Logs sensitive data
logger.info("Authenticating", api_key=api_key)  # NEVER

# Good - Logs safely
logger.info("Authenticating", api_key_length=len(api_key))
logger.info("Authenticating")  # No sensitive data
```

### Redact Sensitive Information

```python
def redact_sensitive(data: dict) -> dict:
    """Redact sensitive fields from data before logging."""
    sensitive_keys = {"password", "api_key", "secret", "token", "credential"}

    redacted = {}
    for key, value in data.items():
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            redacted[key] = "***REDACTED***"
        elif isinstance(value, dict):
            redacted[key] = redact_sensitive(value)
        else:
            redacted[key] = value

    return redacted

# Usage
logger.debug("API response", data=redact_sensitive(response_data))
```

### Log Security Events

Log authentication attempts, access control decisions, and errors:

```python
async def configure(self, config: dict) -> None:
    try:
        await super().configure(config)

        # Validate API key
        is_valid = await self.validate_api_key(config["api_key"])

        if not is_valid:
            logger.warning(
                "Authentication failed - invalid API key",
                api_endpoint=config["api_endpoint"],
            )
            raise ProviderConfigurationError("Invalid API key")

        logger.info(
            "Authentication successful",
            api_endpoint=config["api_endpoint"],
        )

    except Exception as e:
        logger.error(
            "Provider configuration failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        raise
```

---

## Dependency Security

### Pin Dependencies

In `pyproject.toml`:

```toml
[project]
dependencies = [
    "pyvider>=0.0.3,<0.1.0",  # Pin to known-good versions
    "httpx>=0.24.0,<0.25.0",
    "cryptography>=41.0.0,<42.0.0",
]
```

### Audit Dependencies Regularly

```bash
# Check for known vulnerabilities
pip-audit

# Or with uv
uv tool install pip-audit
uv run pip-audit
```

### Use Minimal Dependencies

Only include dependencies you actually need:

```python
# Bad - Importing entire library for one function
import pandas as pd
data = pd.DataFrame(...)

# Good - Use stdlib when possible
import csv
data = list(csv.DictReader(...))
```

---

## Error Handling

### Don't Expose Internal Details

```python
# Bad - Exposes internal structure
except Exception as e:
    raise Exception(f"Database error: {e}\nQuery: {sql_query}\nConnection: {db_conn}")

# Good - Generic error message
except DatabaseError as e:
    logger.error("Database operation failed", error=str(e))
    raise ResourceError("Failed to update resource - please check provider logs")
```

### Handle Errors Gracefully

```python
async def _create_apply(self, ctx: ResourceContext):
    try:
        result = await self.api.create_resource(ctx.config)
        return State(...), None

    except APIError as e:
        # Log detailed error
        logger.error(
            "API call failed",
            error=str(e),
            status_code=e.status_code,
        )

        # Return user-friendly error
        if e.status_code == 401:
            raise ProviderError("Authentication failed - check your API credentials")
        elif e.status_code == 403:
            raise ProviderError("Permission denied - check API key permissions")
        elif e.status_code == 429:
            raise ProviderError("Rate limit exceeded - try again later")
        else:
            raise ProviderError(f"API error: {e.user_message}")

    except Exception as e:
        # Catch-all for unexpected errors
        logger.exception("Unexpected error during resource creation")
        raise ProviderError("An unexpected error occurred - check provider logs")
```

---

## Network Security

### Use TLS/HTTPS Only

```python
def _build_schema(self) -> PvsSchema:
    return s_provider({
        "api_endpoint": a_str(
            required=True,
            validators=[
                lambda x: x.startswith("https://") or "API endpoint must use HTTPS",
            ]
        ),
    })
```

### Implement Timeouts

Prevent hanging connections:

```python
self.http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(
        connect=5.0,   # Connection timeout
        read=30.0,     # Read timeout
        write=10.0,    # Write timeout
        pool=5.0,      # Pool timeout
    )
)
```

### Rate Limiting

Implement rate limiting to prevent abuse:

```python
from datetime import datetime, timedelta
import asyncio

class RateLimiter:
    def __init__(self, max_requests: int, time_window: timedelta):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        """Wait if rate limit exceeded."""
        async with self.lock:
            now = datetime.now()

            # Remove old requests
            self.requests = [
                req_time for req_time in self.requests
                if now - req_time < self.time_window
            ]

            # Wait if limit reached
            if len(self.requests) >= self.max_requests:
                oldest = min(self.requests)
                wait_time = (oldest + self.time_window - now).total_seconds()
                if wait_time > 0:
                    logger.debug("Rate limit reached, waiting", wait_seconds=wait_time)
                    await asyncio.sleep(wait_time)

            self.requests.append(now)
```

---

## Security Checklist

Before releasing your provider, verify:

- [ ] All secrets marked as `sensitive=True`
- [ ] No hardcoded credentials or API keys
- [ ] Input validation on all user-provided data
- [ ] Path traversal protection for file operations
- [ ] Private state used for sensitive data
- [ ] TLS/HTTPS enforced for all API calls
- [ ] SSL certificate verification enabled
- [ ] Request timeouts configured
- [ ] Sensitive data never logged
- [ ] Error messages don't expose internals
- [ ] Dependencies pinned to specific versions
- [ ] Security audit performed on dependencies
- [ ] Rate limiting implemented
- [ ] Authentication properly handled
- [ ] Authorization checked on all operations

---

## Security Resources

- **OWASP Top 10**: [https://owasp.org/www-project-top-ten/](https://owasp.org/www-project-top-ten/)
- **CWE Top 25**: [https://cwe.mitre.org/top25/](https://cwe.mitre.org/top25/)
- **Python Security**: [https://python.readthedocs.io/en/stable/library/security_warnings.html](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- **Terraform Security**: [https://developer.hashicorp.com/terraform/docs/language/values/sensitive.html](https://developer.hashicorp.com/terraform/docs/language/values/sensitive.html)

---

## Reporting Security Issues

If you discover a security vulnerability in Pyvider:

1. **Do NOT open a public issue**
2. Email security details to: [security contact - see repo]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We take security seriously and will respond promptly to all reports.

---

## Related Documentation

- [Error Handling Guide](../development/error-handling.md) - Exception handling patterns
- [Logging Guide](../development/logging.md) - Structured logging
- [Best Practices](../production/best-practices.md) - General best practices
- [Testing Providers](../development/testing-providers.md) - Security testing
