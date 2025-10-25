# Configuration Guide

This guide covers how to configure Pyvider providers in your Terraform configurations, including provider-level settings, environment variables, and best practices for managing sensitive data.

## Provider Configuration Basics

Provider configuration is defined in the Terraform configuration file using the `provider` block:

```hcl
provider "mycloud" {
  api_key  = "your-api-key"
  endpoint = "https://api.mycloud.com"
  timeout  = 30
}
```

The configuration attributes available depend on the provider's schema definition.

## Defining Provider Configuration

In your provider Python code, define the configuration schema in `_build_schema()`:

```python
from pyvider.providers import register_provider, BaseProvider, ProviderMetadata
from pyvider.schema import s_provider, a_str, a_num, a_bool, PvsSchema
import attrs

@attrs.define
class MyCloudConfig:
    """Provider configuration structure."""
    api_key: str
    endpoint: str = "https://api.mycloud.com"
    timeout: int = 30
    debug: bool = False


@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    """MyCloud infrastructure provider."""

    def __init__(self):
        super().__init__(
            metadata=ProviderMetadata(
                name="mycloud",
                version="1.0.0",
                protocol_version="6"
            )
        )
        self.config: MyCloudConfig | None = None

    def _build_schema(self) -> PvsSchema:
        """Define provider configuration schema."""
        return s_provider({
            "api_key": a_str(
                required=True,
                sensitive=True,
                description="API key for authentication"
            ),
            "endpoint": a_str(
                default="https://api.mycloud.com",
                description="API endpoint URL"
            ),
            "timeout": a_num(
                default=30,
                description="Request timeout in seconds"
            ),
            "debug": a_bool(
                default=False,
                description="Enable debug logging"
            ),
        })

    async def configure(self, config: dict) -> None:
        """Configure the provider with validated configuration."""
        await super().configure(config)

        # Convert dict to attrs instance
        self.config = MyCloudConfig(
            api_key=config["api_key"],
            endpoint=config.get("endpoint", "https://api.mycloud.com"),
            timeout=config.get("timeout", 30),
            debug=config.get("debug", False),
        )

        # Initialize API client
        self.client = MyCloudClient(
            api_key=self.config.api_key,
            endpoint=self.config.endpoint,
            timeout=self.config.timeout,
        )
```

## Environment Variables

Terraform supports environment variable interpolation in provider configuration:

```hcl
provider "mycloud" {
  api_key  = var.mycloud_api_key
  endpoint = var.mycloud_endpoint
}
```

Define variables:

```hcl
variable "mycloud_api_key" {
  type        = string
  description = "MyCloud API key"
  sensitive   = true
}

variable "mycloud_endpoint" {
  type        = string
  default     = "https://api.mycloud.com"
  description = "MyCloud API endpoint"
}
```

Set via environment variables:

```bash
export TF_VAR_mycloud_api_key="your-api-key"
export TF_VAR_mycloud_endpoint="https://api.mycloud.com"
```

Or via `.tfvars` file:

```hcl
# terraform.tfvars
mycloud_api_key  = "your-api-key"
mycloud_endpoint = "https://api.mycloud.com"
```

## Sensitive Data Handling

Mark sensitive attributes in your schema:

```python
def _build_schema(self) -> PvsSchema:
    return s_provider({
        "api_key": a_str(
            required=True,
            sensitive=True,  # Marks value as sensitive
            description="API key for authentication"
        ),
        "password": a_str(
            required=True,
            sensitive=True,
            description="Password for authentication"
        ),
    })
```

Benefits of marking attributes as sensitive:
- Values are masked in Terraform output
- Not shown in `terraform plan` or `terraform show`
- Protected in state file (when using remote state with encryption)
- Hidden in logs

## Configuration Patterns

### Multiple Provider Instances

You can configure multiple instances of the same provider:

```hcl
# Production environment
provider "mycloud" {
  alias    = "prod"
  api_key  = var.prod_api_key
  endpoint = "https://api.prod.mycloud.com"
}

# Staging environment
provider "mycloud" {
  alias    = "staging"
  api_key  = var.staging_api_key
  endpoint = "https://api.staging.mycloud.com"
}

# Use specific provider instance
resource "mycloud_server" "web" {
  provider = mycloud.prod
  name     = "web-server"
}
```

### Region-Based Configuration

```hcl
provider "mycloud" {
  api_key = var.api_key
  region  = "us-west-2"
}
```

Provider implementation:

```python
def _build_schema(self) -> PvsSchema:
    return s_provider({
        "api_key": a_str(required=True, sensitive=True),
        "region": a_str(
            default="us-east-1",
            description="AWS-compatible region identifier"
        ),
    })
```

### Retry and Timeout Configuration

```hcl
provider "mycloud" {
  api_key         = var.api_key
  timeout         = 60
  max_retries     = 3
  retry_delay     = 5
}
```

Implementation:

```python
@attrs.define
class RetryConfig:
    """Retry configuration."""
    max_retries: int = 3
    retry_delay: int = 5
    timeout: int = 60


def _build_schema(self) -> PvsSchema:
    return s_provider({
        "timeout": a_num(
            default=60,
            description="Request timeout in seconds"
        ),
        "max_retries": a_num(
            default=3,
            description="Maximum number of retry attempts"
        ),
        "retry_delay": a_num(
            default=5,
            description="Delay between retries in seconds"
        ),
    })

async def configure(self, config: dict) -> None:
    await super().configure(config)

    retry_config = RetryConfig(
        timeout=config.get("timeout", 60),
        max_retries=config.get("max_retries", 3),
        retry_delay=config.get("retry_delay", 5),
    )

    self.client = MyCloudClient(
        api_key=config["api_key"],
        retry_config=retry_config,
    )
```

## Configuration Validation

Implement custom validation logic in the provider:

```python
async def configure(self, config: dict) -> None:
    """Configure provider with validation."""
    await super().configure(config)

    # Validate endpoint URL
    endpoint = config.get("endpoint", "")
    if not endpoint.startswith(("http://", "https://")):
        raise ProviderConfigurationError(
            "Endpoint must be a valid HTTP(S) URL"
        )

    # Validate timeout
    timeout = config.get("timeout", 30)
    if timeout < 1 or timeout > 300:
        raise ProviderConfigurationError(
            "Timeout must be between 1 and 300 seconds"
        )

    # Test connection
    try:
        self.client = MyCloudClient(
            api_key=config["api_key"],
            endpoint=endpoint,
            timeout=timeout,
        )
        await self.client.test_connection()
    except ConnectionError as e:
        raise ProviderConfigurationError(
            f"Failed to connect to {endpoint}: {e}"
        )

    self.config = MyCloudConfig(
        api_key=config["api_key"],
        endpoint=endpoint,
        timeout=timeout,
    )
```

## Accessing Provider Configuration in Resources

Resources can access provider configuration through the hub:

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.hub import hub

@register_resource("server")
class Server(BaseResource):
    async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        """Create server using provider configuration."""
        # Get provider instance
        provider = hub.get_component("singleton", "provider")
        if provider is None or provider.config is None:
            raise RuntimeError("Provider has not been configured yet.")

        # Access provider config
        api_key = provider.config.api_key
        endpoint = provider.config.endpoint

        # Use provider's client
        server = await provider.client.create_server(
            name=ctx.config.name,
            region=provider.config.region,
        )

        return ServerState(...), None
```

## Configuration Examples

### Basic Authentication

```hcl
provider "mycloud" {
  username = var.username
  password = var.password
}
```

```python
def _build_schema(self) -> PvsSchema:
    return s_provider({
        "username": a_str(required=True, description="Username"),
        "password": a_str(required=True, sensitive=True, description="Password"),
    })
```

### Token Authentication

```hcl
provider "mycloud" {
  token = var.api_token
}
```

```python
def _build_schema(self) -> PvsSchema:
    return s_provider({
        "token": a_str(
            required=True,
            sensitive=True,
            description="API authentication token"
        ),
    })
```

### OAuth2 Configuration

```hcl
provider "mycloud" {
  client_id     = var.client_id
  client_secret = var.client_secret
  auth_url      = "https://auth.mycloud.com/oauth2/token"
}
```

```python
def _build_schema(self) -> PvsSchema:
    return s_provider({
        "client_id": a_str(required=True),
        "client_secret": a_str(required=True, sensitive=True),
        "auth_url": a_str(
            default="https://auth.mycloud.com/oauth2/token"
        ),
    })
```

### TLS/SSL Configuration

```hcl
provider "mycloud" {
  api_key            = var.api_key
  tls_verify         = true
  tls_ca_cert_file   = "/path/to/ca.pem"
  tls_client_cert    = "/path/to/client.pem"
  tls_client_key     = "/path/to/client-key.pem"
}
```

```python
def _build_schema(self) -> PvsSchema:
    return s_provider({
        "api_key": a_str(required=True, sensitive=True),
        "tls_verify": a_bool(default=True),
        "tls_ca_cert_file": a_str(description="Path to CA certificate"),
        "tls_client_cert": a_str(description="Path to client certificate"),
        "tls_client_key": a_str(sensitive=True, description="Path to client key"),
    })
```

## Best Practices

### 1. Use Sensible Defaults

Provide defaults for optional configuration:

```python
"timeout": a_num(
    default=30,
    description="Request timeout in seconds"
),
"max_retries": a_num(
    default=3,
    description="Maximum retry attempts"
),
```

### 2. Mark Sensitive Data

Always mark sensitive attributes:

```python
"api_key": a_str(
    required=True,
    sensitive=True,  # Critical for security
    description="API key for authentication"
),
```

### 3. Validate Early

Validate configuration in `configure()` before creating resources:

```python
async def configure(self, config: dict) -> None:
    await super().configure(config)

    # Validate configuration
    if config["timeout"] < 1:
        raise ProviderConfigurationError("Timeout must be positive")

    # Test connectivity
    await self.test_connection(config)
```

### 4. Document Configuration

Provide clear descriptions for all configuration attributes:

```python
"endpoint": a_str(
    default="https://api.mycloud.com",
    description="API endpoint URL. Use https://api.staging.mycloud.com for staging."
),
```

### 5. Use Type-Safe Config Classes

Create attrs classes for configuration:

```python
@attrs.define
class ProviderConfig:
    """Type-safe provider configuration."""
    api_key: str
    endpoint: str = "https://api.mycloud.com"
    timeout: int = 30

    def __attrs_post_init__(self):
        """Validate after initialization."""
        if self.timeout < 1:
            raise ValueError("Timeout must be positive")
```

### 6. Cache Clients

Initialize API clients once in `configure()`:

```python
async def configure(self, config: dict) -> None:
    await super().configure(config)

    # Initialize client once
    self.client = MyCloudClient(
        api_key=config["api_key"],
        endpoint=config.get("endpoint"),
    )

    # Test connection
    await self.client.ping()
```

## Common Issues

### Missing Required Configuration

**Error:**
```
Error: Missing required argument

The argument "api_key" is required, but no definition was found.
```

**Solution:**
Ensure required attributes are marked in schema and provided in configuration:

```python
"api_key": a_str(required=True, ...)
```

### Invalid Configuration Values

**Error:**
```
Error: Invalid provider configuration
```

**Solution:**
Add validation in `configure()`:

```python
async def configure(self, config: dict) -> None:
    if not config.get("api_key"):
        raise ProviderConfigurationError("api_key cannot be empty")
```

### Sensitive Data Exposure

**Issue:** Sensitive values appearing in logs or output

**Solution:** Mark all sensitive attributes:

```python
"password": a_str(required=True, sensitive=True),
"api_token": a_str(required=True, sensitive=True),
```

## See Also

- [Creating Providers](../building-components/creating-providers.md) - Complete provider development guide
- [Best Practices](../production/best-practices.md) - Provider development best practices
- [Error Handling](../development/error-handling.md) - Error handling patterns
- [Schema System](../../schema/overview.md) - Schema definition reference
