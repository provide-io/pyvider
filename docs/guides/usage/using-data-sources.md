# Using Data Sources

Data sources provide read-only access to information from your infrastructure or external systems. This guide covers how to use data sources effectively in your Terraform configurations.

## What are Data Sources?

Data sources query existing infrastructure without managing it. They're used to:
- Fetch configuration from existing resources
- Query external APIs for information
- Retrieve metadata for use in resource configuration
- Lookup values dynamically during planning

## Basic Usage

Query a data source in Terraform:

```hcl
data "mycloud_image" "ubuntu" {
  name   = "ubuntu-22.04"
  region = "us-west-2"
}

resource "mycloud_server" "web" {
  name     = "web-server"
  image_id = data.mycloud_image.ubuntu.id  # Use data source output
  size     = "small"
}
```

## Common Patterns

### Lookup by Filter

Find resources matching specific criteria:

```hcl
data "mycloud_images" "available" {
  name_filter = "ubuntu-*"
  region      = "us-west-2"
  active_only = true
}

output "image_count" {
  value = length(data.mycloud_images.available.ids)
}
```

### Query Configuration

Fetch settings from external systems:

```hcl
data "mycloud_config" "settings" {
  environment = var.environment
}

resource "mycloud_server" "app" {
  name    = "app-server"
  timeout = data.mycloud_config.settings.default_timeout
}
```

### Retrieve Metadata

Get information about the provider or account:

```hcl
data "mycloud_account" "current" {}

output "account_id" {
  value = data.mycloud_account.current.id
}
```

## Data Source Dependencies

### Data Sources in Resources

Resources can depend on data source outputs:

```hcl
data "mycloud_network" "main" {
  name = "main-network"
}

resource "mycloud_server" "web" {
  network_id = data.mycloud_network.main.id  # Implicit dependency
}
```

### Data Sources Referencing Resources

Data sources can use resource outputs:

```hcl
resource "mycloud_network" "app" {
  name = "app-network"
  cidr = "10.0.0.0/16"
}

data "mycloud_network_details" "app" {
  network_id = mycloud_network.app.id  # Reads from resource
}
```

## Real-World Examples

### Environment-Specific Configuration

```hcl
variable "environment" {
  type = string
}

data "mycloud_config" "env" {
  environment = var.environment
}

resource "mycloud_server" "app" {
  name    = "${var.environment}-app"
  size    = data.mycloud_config.env.instance_size
  replicas = data.mycloud_config.env.replica_count
}
```

### Service Discovery

```hcl
data "mycloud_services" "databases" {
  type   = "database"
  status = "running"
}

resource "mycloud_server" "app" {
  name = "app-server"

  environment = {
    DB_HOST = data.mycloud_services.databases.endpoints[0]
  }
}
```

### Certificate Management

```hcl
data "mycloud_certificate" "tls" {
  domain = "example.com"
  latest = true
}

resource "mycloud_load_balancer" "web" {
  name          = "web-lb"
  certificate_id = data.mycloud_certificate.tls.id
}
```

## Performance Considerations

### Caching

Data sources are evaluated during planning and cached:

```hcl
# Queried once during terraform plan
data "mycloud_images" "all" {
  region = "us-west-2"
}

# All resources use cached data
resource "mycloud_server" "web1" {
  image_id = data.mycloud_images.all.ids[0]
}

resource "mycloud_server" "web2" {
  image_id = data.mycloud_images.all.ids[0]
}
```

### Filtering

Filter data sources to reduce query size:

```hcl
# Good: Specific filter
data "mycloud_images" "ubuntu" {
  name_filter = "ubuntu-22.04-*"
  region      = "us-west-2"
}

# Avoid: Fetching all data then filtering in Terraform
data "mycloud_images" "all" {
  region = "us-west-2"
}

locals {
  ubuntu_images = [
    for img in data.mycloud_images.all.images :
    img if can(regex("ubuntu-22.04", img.name))
  ]
}
```

## Error Handling

### Missing Data

Handle cases where data isn't found:

```hcl
data "mycloud_image" "ubuntu" {
  name = "ubuntu-22.04"
}

# Terraform will error if image not found
# Provider should return clear error message
```

### Optional Data

Use count for optional data sources:

```hcl
data "mycloud_certificate" "tls" {
  count  = var.enable_tls ? 1 : 0
  domain = "example.com"
}

resource "mycloud_load_balancer" "web" {
  certificate_id = var.enable_tls ? data.mycloud_certificate.tls[0].id : null
}
```

## Best Practices

### 1. Use Specific Filters

Query only what you need:

```hcl
# Good
data "mycloud_images" "ubuntu" {
  name   = "ubuntu-22.04-amd64"
  region = "us-west-2"
}

# Avoid
data "mycloud_images" "all" {}
```

### 2. Minimize Data Source Calls

Reuse data sources across multiple resources:

```hcl
data "mycloud_network" "main" {
  name = "main-network"
}

resource "mycloud_server" "web1" {
  network_id = data.mycloud_network.main.id
}

resource "mycloud_server" "web2" {
  network_id = data.mycloud_network.main.id  # Reuses cached data
}
```

### 3. Document Data Sources

Add descriptions to clarify usage:

```hcl
data "mycloud_config" "app" {
  environment = var.environment

  # Fetches environment-specific configuration including:
  # - Instance sizes
  # - Replica counts
  # - Timeout values
}
```

### 4. Handle Missing Data Gracefully

Validate data source results:

```hcl
data "mycloud_network" "app" {
  name = var.network_name
}

# Validate result exists
resource "null_resource" "validate" {
  count = data.mycloud_network.app.id != "" ? 0 : 1

  provisioner "local-exec" {
    command = "echo 'Network ${var.network_name} not found' && exit 1"
  }
}
```

## Common Use Cases

### Configuration Management

Fetch external configuration:

```hcl
data "mycloud_config" "app" {
  application = "web-app"
  environment = var.environment
}

resource "mycloud_server" "app" {
  name = "app-server"

  environment = merge(
    data.mycloud_config.app.variables,
    var.additional_env_vars
  )
}
```

### Resource Discovery

Find existing infrastructure:

```hcl
data "mycloud_vpc" "main" {
  default = true
}

data "mycloud_subnets" "public" {
  vpc_id = data.mycloud_vpc.main.id
  public = true
}

resource "mycloud_server" "web" {
  subnet_id = data.mycloud_subnets.public.ids[0]
}
```

### Dynamic Values

Compute values at plan time:

```hcl
data "mycloud_availability_zones" "available" {
  region = var.region
}

resource "mycloud_server" "distributed" {
  count = length(data.mycloud_availability_zones.available.names)

  name = "server-${count.index}"
  zone = data.mycloud_availability_zones.available.names[count.index]
}
```

## Comparison: Data Sources vs Resources

| Aspect | Data Sources | Resources |
|--------|--------------|-----------|
| **Purpose** | Read-only queries | Create/Update/Delete |
| **State** | Not stored in state | Stored in state |
| **Lifecycle** | Query during plan | Full CRUD lifecycle |
| **Updates** | Re-queried on each plan | Only updated on changes |
| **Dependencies** | Can depend on resources | Can depend on data sources |

## Examples from pyvider-components

The [pyvider-components](https://github.com/provide-io/pyvider-components) repository includes many data source examples:

- `env_variables` - Read environment variables
- `file_info` - Get file metadata
- `http_api` - Query HTTP endpoints
- `lens_jq` - Transform JSON with JQ

## See Also

- [Creating Data Sources](../building-components/creating-data-sources.md) - How to implement data sources
- [Managing Resources](managing-resources.md) - Resource lifecycle management
- [Best Practices](../production/best-practices.md) - Provider development patterns
- [Pyvider Components](https://github.com/provide-io/pyvider-components) - Working examples
