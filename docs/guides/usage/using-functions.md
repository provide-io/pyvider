# Using Functions

Provider functions enable custom transformations and computations in your Terraform configurations. This guide shows how to use functions effectively.

## What are Provider Functions?

Functions are callable operations that transform input into output without managing infrastructure. They're useful for:
- Data transformation (JSON, strings, numbers)
- Hash computation
- Encoding/decoding operations
- Custom business logic

## Basic Usage

Call a provider function in Terraform:

```hcl
terraform {
  required_providers {
    mycloud = {
      source = "example.com/mycloud"
    }
  }
}

output "hashed_value" {
  value = provider::mycloud::hash("hello world")
}
```

## Common Patterns

### String Transformation

```hcl
locals {
  uppercase_name = provider::mycloud::to_upper(var.server_name)
  slugified      = provider::mycloud::slugify("My Server Name")
}
```

### JSON Manipulation

```hcl
locals {
  config_json = jsonencode({
    name = "app"
    port = 8080
  })

  transformed = provider::mycloud::jq_transform(
    local.config_json,
    ".name + \"-v2\""
  )
}
```

### Hash Generation

```hcl
resource "mycloud_api_key" "app" {
  name       = "app-key"
  secret_hash = provider::mycloud::sha256(var.api_secret)
}
```

### Encoding/Decoding

```hcl
locals {
  encoded_data = provider::mycloud::base64_encode("sensitive data")
  decoded_data = provider::mycloud::base64_decode(var.encoded_config)
}
```

## Using Functions with Resources

Functions integrate seamlessly with resource configuration:

```hcl
resource "mycloud_server" "app" {
  name = provider::mycloud::slugify(var.server_name)

  environment = {
    CONFIG_HASH = provider::mycloud::md5(file("config.json"))
  }

  tags = {
    fingerprint = provider::mycloud::sha256(var.deployment_id)
  }
}
```

## Function Composition

Chain functions for complex transformations:

```hcl
locals {
  # Encode JSON, then base64 encode the result
  encoded_config = provider::mycloud::base64_encode(
    jsonencode(var.config)
  )

  # Transform JSON with JQ, then hash the result
  config_hash = provider::mycloud::sha256(
    provider::mycloud::jq_transform(
      jsonencode(var.config),
      "sort_keys"
    )
  )
}
```

## Comparison with Built-in Functions

| Aspect | Provider Functions | Built-in Functions |
|--------|-------------------|-------------------|
| **Definition** | Defined by providers | Built into Terraform |
| **Namespace** | `provider::name::function` | Direct call (e.g., `length()`) |
| **Scope** | Provider-specific logic | General-purpose |
| **Examples** | `provider::mycloud::hash` | `length`, `concat`, `merge` |

Use built-in functions when possible; use provider functions for domain-specific operations.

## Best Practices

### 1. Use for Domain Logic

Provider functions should encapsulate provider-specific logic:

```hcl
# Good: Provider-specific validation
resource "mycloud_server" "app" {
  name = provider::mycloud::validate_name(var.server_name)
}

# Avoid: Use built-in functions for generic operations
# Bad:
value = provider::mycloud::to_upper(var.name)
# Good:
value = upper(var.name)
```

### 2. Keep Functions Pure

Functions should be deterministic (same input = same output):

```hcl
# Good: Pure function
hash = provider::mycloud::sha256("data")

# Avoid: Functions that depend on external state
# (Use data sources for this instead)
```

### 3. Document Function Usage

Add comments explaining function purpose:

```hcl
locals {
  # Hash server configuration for change detection
  # Uses SHA-256 to ensure consistent length
  config_fingerprint = provider::mycloud::sha256(
    jsonencode(var.server_config)
  )
}
```

## Examples from pyvider-components

The [pyvider-components](https://github.com/provide-io/pyvider-components) repository includes function examples:

- String functions (`upper`, `lower`, `slugify`)
- Numeric functions (`add`, `multiply`, `round`)
- JQ transformation functions
- Hash and encoding functions

## Real-World Use Cases

### Configuration Fingerprinting

```hcl
resource "mycloud_deployment" "app" {
  name = "app-deployment"

  config_hash = provider::mycloud::sha256(
    jsonencode({
      version     = var.app_version
      environment = var.environment
      replicas    = var.replica_count
    })
  )

  # Triggers redeployment when config changes
  triggers = {
    config = provider::mycloud::sha256(
      file("${path.module}/config.yaml")
    )
  }
}
```

### Data Transformation

```hcl
locals {
  # Transform API response using JQ
  processed_data = provider::mycloud::jq_transform(
    data.http.api_response.body,
    ".items | map(.name) | sort"
  )
}
```

### Name Sanitization

```hcl
resource "mycloud_bucket" "data" {
  # Ensure bucket name meets provider requirements
  name = provider::mycloud::sanitize_bucket_name(
    "${var.project}-${var.environment}-data"
  )
}
```

## Debugging Functions

Test function output using `terraform console`:

```bash
$ terraform console
> provider::mycloud::hash("test")
"9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"

> provider::mycloud::slugify("My Server Name")
"my-server-name"
```

## Performance Considerations

Functions execute during planning:

```hcl
# Evaluated once during plan
locals {
  hash = provider::mycloud::sha256(file("large-file.json"))
}

# All resources use cached value
resource "mycloud_server" "web1" {
  config_hash = local.hash
}

resource "mycloud_server" "web2" {
  config_hash = local.hash
}
```

## See Also

- [Creating Functions](../building-components/creating-functions.md) - How to implement provider functions
- [Best Practices](../production/best-practices.md) - Provider development patterns
- [Pyvider Components](https://github.com/provide-io/pyvider-components) - Working examples
