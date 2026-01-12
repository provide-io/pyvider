# Handling Sensitive Data in Schemas

Sensitive data like passwords, API keys, and tokens require special handling to prevent accidental exposure in logs, state files, and terminal output.

## Marking Attributes as Sensitive

Use the `sensitive=True` parameter to mark attributes containing secrets:

```python
from pyvider.schema import s_resource, a_str

@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "api_key": a_str(
            required=True,
            sensitive=True,  # Marks as sensitive
            description="API authentication key"
        ),
        "password": a_str(
            required=True,
            sensitive=True,
            description="Database password"
        ),
        "username": a_str(
            required=True,
            description="Database username"  # Not sensitive
        ),
    })
```

## How Sensitive Attributes Behave

### In Terraform Output

Sensitive values are masked in `terraform plan` and `terraform apply` output:

```hcl
resource "mycloud_database" "main" {
  username = "admin"
  password = var.db_password  # Sensitive
  api_key  = var.api_key      # Sensitive
}
```

**Terraform output**:
```
# mycloud_database.main will be created
+ resource "mycloud_database" "main" {
    + username = "admin"
    + password = (sensitive value)
    + api_key  = (sensitive value)
  }
```

### In State Files

Terraform stores sensitive values in state but marks them as sensitive:

```json
{
  "attributes": {
    "username": "admin",
    "password": "secret123",
    "api_key": "key-abc123"
  },
  "sensitive_attributes": [
    {
      "type": "get_attr",
      "value": "password"
    },
    {
      "type": "get_attr",
      "value": "api_key"
    }
  ]
}
```

**Important**: State files still contain sensitive values. Secure your state:
- Use remote state with encryption (S3 + encryption, Terraform Cloud)
- Never commit state files to version control
- Restrict access to state storage

### In Provider Logs

Pyvider's logging system automatically masks sensitive values:

```python
# Your code
logger.debug("Configuring database", config=config.__dict__)

# Log output (sensitive values masked)
DEBUG - Configuring database config={'username': 'admin', 'password': '***', 'api_key': '***'}
```

## Common Sensitive Attributes

### Authentication Credentials

```python
"api_key": a_str(required=True, sensitive=True)
"api_secret": a_str(required=True, sensitive=True)
"access_token": a_str(required=True, sensitive=True)
"bearer_token": a_str(required=True, sensitive=True)
```

### Passwords

```python
"password": a_str(required=True, sensitive=True)
"admin_password": a_str(required=True, sensitive=True)
"db_password": a_str(required=True, sensitive=True)
```

### Private Keys and Certificates

```python
"private_key": a_str(required=True, sensitive=True)
"tls_key": a_str(required=True, sensitive=True)
"ssh_private_key": a_str(required=True, sensitive=True)
```

### Connection Strings

```python
"connection_string": a_str(required=True, sensitive=True)
"database_url": a_str(required=True, sensitive=True)
```

## Private State for Sensitive Data

For truly sensitive data that should be encrypted in state, use **private state**:

```python
from pyvider.resources.private_state import PrivateState

@register_resource("mycloud_api_token")
class ApiTokenResource(BaseResource):

    async def _create(self, ctx: ResourceContext, base_plan: dict):
        # Generate API token
        result = await self.api.create_token()

        # Sensitive data goes in private state (encrypted)
        private_data = {
            "access_token": result.access_token,
            "refresh_token": result.refresh_token,
            "secret_key": result.secret_key,
        }
        encrypted_private_state = PrivateState.encrypt(private_data)

        # Public data in regular state
        public_state = {
            **base_plan,
            "token_id": result.id,
            "expires_at": result.expires_at,
            # NO sensitive data here
        }

        return public_state, encrypted_private_state

    async def read(self, ctx: ResourceContext):
        # Access private state when needed
        if ctx.private_state:
            private_data = PrivateState.decrypt(ctx.private_state)
            access_token = private_data["access_token"]
            # Use token for API calls
```

**Private State Benefits**:
- Encrypted in Terraform state
- Requires `private_state_shared_secret` in pyvider.toml
- Additional layer of security beyond sensitive attributes

## Best Practices

### 1. Mark All Sensitive Data

```python
# Good: All secrets marked sensitive
"api_key": a_str(sensitive=True)
"password": a_str(sensitive=True)
"token": a_str(sensitive=True)

# Bad: Secrets not marked
"api_key": a_str()  # Will appear in logs!
```

### 2. Use Variables for Sensitive Input

```hcl
# Good: Use Terraform variables
variable "api_key" {
  type      = string
  sensitive = true
}

resource "mycloud_api" "main" {
  api_key = var.api_key
}

# Bad: Hardcoded secrets
resource "mycloud_api" "main" {
  api_key = "hardcoded-key-123"  # Never do this!
}
```

### 3. Don't Log Sensitive Data

```python
# Good: Don't log sensitive values
async def configure(self, config: dict):
    self.api_key = config["api_key"]
    logger.info("Provider configured", endpoint=config["api_endpoint"])

# Bad: Logging secrets
async def configure(self, config: dict):
    self.api_key = config["api_key"]
    logger.info("Provider configured", api_key=self.api_key)  # Don't log!
```

### 4. Use Environment Variables

```hcl
# Good: Environment variables
provider "mycloud" {
  api_key = env.MYCLOUD_API_KEY
}
```

```bash
export MYCLOUD_API_KEY="secret-key"
terraform apply
```

### 5. Computed Sensitive Attributes

Generated secrets should also be marked sensitive:

```python
"generated_password": a_str(
    computed=True,
    sensitive=True,
    description="Auto-generated password"
)
```

## What NOT to Mark as Sensitive

Not everything needs to be sensitive:

```python
# These are usually NOT sensitive
"username": a_str()           # Usernames often public
"endpoint": a_str()           # API endpoints are public
"region": a_str()             # Regions are public
"instance_type": a_str()      # Instance types are public
"tags": a_list(a_str())       # Tags usually public

# These ARE sensitive
"password": a_str(sensitive=True)
"api_key": a_str(sensitive=True)
"secret_token": a_str(sensitive=True)
```

**Rule of thumb**: If exposing the value could compromise security, mark it sensitive.

## Testing with Sensitive Data

Use fixtures and environment variables for testing:

```python
import pytest

@pytest.fixture
def api_key():
    """Test API key from environment."""
    return os.getenv("TEST_API_KEY", "test-key-for-ci")

async def test_api_authentication(api_key):
    config = ProviderConfig(
        api_endpoint="https://api.test.example.com",
        api_key=api_key  # From fixture
    )

    provider = MyProvider()
    await provider.configure(config)

    # Test without logging the key
    assert provider._configured is True
```

## Secure State Configuration

Configure Terraform to use encrypted remote state:

```hcl
# S3 with encryption
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    kms_key_id     = "arn:aws:kms:..."
  }
}
```

## Private State Configuration

For encrypted private state, configure in `pyvider.toml`:

```toml
# pyvider.toml
private_state_shared_secret = "your-encryption-key-here"

# Or use environment variable
# export PYVIDER_PRIVATE_STATE_SECRET="your-encryption-key-here"
```

**Important**: Keep this secret secure. If lost, private state cannot be decrypted.

## Debugging Sensitive Data Issues

If you need to debug but have sensitive data:

```python
# Good: Log with masking
logger.debug(
    "API request failed",
    endpoint=self.api_endpoint,
    key_prefix=self.api_key[:4] + "****"  # Only show prefix
)

# Bad: Log full value
logger.debug("API request failed", api_key=self.api_key)
```

## Related Documentation

- [Overview](overview.md) - Schema system introduction
- [Types](types.md) - Available attribute types
- [Validators](validators.md) - Validation including sensitive data
- [Best Practices](best-practices.md) - Schema design guidelines
- [Security Practices](../guides/production/production-readiness.md#security-practices)

---

**Remember**: Security is layered. Mark attributes as sensitive, use private state for highly sensitive data, secure your state storage, and never log secrets. When in doubt, mark it sensitive.
