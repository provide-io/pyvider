# Resources vs Data Sources

Understanding the fundamental difference between resources and data sources in Terraform providers.

---

## Conceptual Difference

### Resources: Infrastructure Management

Resources represent **managed infrastructure** - things your Terraform configuration creates, updates, and destroys.

**Think of resources as:**
- Active management
- Write operations
- State tracking
- Lifecycle management

**Examples:**
- Creating a server
- Managing a database
- Configuring a firewall rule
- Creating a DNS record

**User intent:** "Make this exist and keep it that way"

---

### Data Sources: Information Retrieval

Data sources are **read-only queries** - they fetch information without creating or modifying anything.

**Think of data sources as:**
- Passive querying
- Read operations
- No state (refreshed each run)
- Information lookup

**Examples:**
- Query available server images
- Look up existing VPC
- Fetch current IP address
- Read file contents

**User intent:** "Tell me what exists"

---

## Technical Differences

| Aspect | Resource | Data Source |
|--------|----------|-------------|
| **Purpose** | Manage infrastructure | Query information |
| **Operations** | Create, Read, Update, Delete | Read only |
| **State** | Tracked by Terraform | No state (re-queried) |
| **Lifecycle** | Full CRUD lifecycle | Single read operation |
| **Changes** | Can modify remote systems | Never modifies anything |
| **Methods** | `read()`, `_create_apply()`, `_update_apply()`, `_delete_apply()` | `read()` only |
| **Schema** | Inputs + computed outputs | Inputs + computed outputs |
| **Context** | ResourceContext with state | Just config parameter |

---

## When to Use Each

### Use a Resource When:

✅ You need to **create** something
```hcl
resource "mycloud_server" "web" {
  name = "web-server"
  size = "large"
}
```

✅ You need to **manage lifecycle** (create, update, delete)
```hcl
resource "mycloud_database" "main" {
  name = "production-db"
  size = 100  # Can be updated
}
```

✅ Terraform should **track state** and detect drift
```hcl
resource "mycloud_file" "config" {
  path    = "/etc/app/config.yaml"
  content = templatefile("config.yaml.tpl", {})
}
# Terraform will recreate if deleted outside Terraform
```

✅ You need **update-in-place** behavior
```hcl
resource "mycloud_server" "app" {
  name  = "app-server"
  tags  = var.tags  # Update tags without recreating server
}
```

---

### Use a Data Source When:

✅ You need to **query existing** infrastructure
```hcl
data "mycloud_image" "ubuntu" {
  name = "ubuntu-22.04"
}

resource "mycloud_server" "web" {
  image_id = data.mycloud_image.ubuntu.id
}
```

✅ You need information from external systems
```hcl
data "mycloud_vpc" "main" {
  filter = "name=production"
}

resource "mycloud_server" "app" {
  vpc_id = data.mycloud_vpc.main.id
}
```

✅ You need **dynamic lookups**
```hcl
data "mycloud_available_zones" "current" {
  region = var.region
}

# Use in resource
resource "mycloud_server" "regional" {
  for_each = toset(data.mycloud_available_zones.current.zones)
  zone     = each.key
}
```

✅ You need data that **changes independently** of Terraform
```hcl
data "mycloud_current_ip" "me" {}

# Use for security group
resource "mycloud_security_rule" "allow_me" {
  source_ip = data.mycloud_current_ip.me.ip
}
# IP is refreshed on every terraform plan
```

---

## Design Philosophy

### Resource Philosophy

**"Declarative Infrastructure"**

- User declares desired state
- Terraform makes it so
- Continuous reconciliation
- Provider owns the lifecycle

**Resource contract:**
```
User: "I want a server named 'web' with size 'large'"
Provider: "I will create it and keep it that way"
Terraform: "I will track its state and detect any drift"
```

---

### Data Source Philosophy

**"Information Bridge"**

- User requests information
- Provider fetches it
- No ownership or management
- Fresh data on every run

**Data source contract:**
```
User: "What is the latest Ubuntu image ID?"
Provider: "Here it is: ami-12345"
Terraform: "I will ask again next time you run plan"
```

---

## Common Anti-Patterns

### ❌ Using Resource for Read-Only Queries

```hcl
# BAD: Resource for something that shouldn't be managed
resource "mycloud_latest_image" "ubuntu" {
  name = "ubuntu"  # This queries, doesn't create!
}
```

**Why bad:** Resources should manage lifecycle. If this is read-only, it's a data source.

**Fix:**
```hcl
# GOOD: Data source for queries
data "mycloud_latest_image" "ubuntu" {
  name = "ubuntu"
}
```

---

### ❌ Using Data Source for Mutable State

```hcl
# BAD: Data source that tries to modify
data "mycloud_server_config" "web" {
  server_id = mycloud_server.web.id
  config = {...}  # Trying to configure server via data source!
}
```

**Why bad:** Data sources are read-only. This should be a resource property.

**Fix:**
```hcl
# GOOD: Resource manages configuration
resource "mycloud_server" "web" {
  name   = "web-server"
  config = {...}  # Part of resource
}
```

---

### ❌ Storing Non-Deterministic Data

```hcl
# BAD: Data source with different results each time
data "mycloud_random_server" "any" {
  # Returns different server each query!
}
```

**Why bad:** Data sources should be deterministic (same inputs = same outputs).

**Fix:** If you need randomness, use a resource to track it:
```hcl
# GOOD: Resource for persistent random value
resource "random_integer" "server_index" {
  min = 1
  max = 100
}
```

---

## Implementation Comparison

### Resource Implementation

```python
from pyvider.resources import BaseResource

class Server(BaseResource):
    # Multiple lifecycle methods
    async def read(self, ctx) -> State | None:
        """Check current state."""
        pass

    async def _create_apply(self, ctx) -> tuple[State, None]:
        """Create server."""
        pass

    async def _update_apply(self, ctx) -> tuple[State, None]:
        """Update server."""
        pass

    async def _delete_apply(self, ctx) -> None:
        """Delete server."""
        pass
```

**Complexity:** Multiple methods, state management, lifecycle coordination

---

### Data Source Implementation

```python
from pyvider.data_sources import BaseDataSource

class ServerQuery(BaseDataSource):
    # Single read method
    async def read(self, config) -> Data:
        """Query servers."""
        servers = await api.list_servers(config.filter)
        return Data(id=config.filter, servers=servers)
```

**Simplicity:** One method, no state, just query and return

---

## State Management

### Resources Have State

```hcl
resource "mycloud_server" "web" {
  name = "web-server"
}
```

**Terraform tracks:**
```json
{
  "id": "server-123",
  "name": "web-server",
  "size": "large",
  "status": "running"
}
```

Changes are detected by comparing state with reality.

---

### Data Sources Have No State

```hcl
data "mycloud_server_list" "running" {
  status = "running"
}
```

**Terraform does not track state.** Every `terraform plan` re-fetches the data.

---

## Refresh Behavior

### Resources: Drift Detection

1. `terraform plan` calls `read()`
2. Compares current state with desired state
3. Shows what needs to change

**Example:**
```
Server exists but tags changed:
  ~ tags: {env: "dev"} → {env: "prod"}

Terraform will update in-place.
```

---

### Data Sources: Always Refresh

1. `terraform plan` calls `read()`
2. Uses fresh data immediately
3. No comparison with previous run

**Example:**
```
Query returned 5 servers (was 3 last time)

This is expected - data sources always refresh.
```

---

## When Something Could Be Either

Sometimes the same concept could be implemented as either:

### Example: DNS Record

**As a Resource:**
```hcl
resource "mycloud_dns_record" "www" {
  domain = "example.com"
  name   = "www"
  value  = mycloud_server.web.ip
}
# Terraform creates and manages the DNS record
```

**As a Data Source:**
```hcl
data "mycloud_dns_record" "www" {
  domain = "example.com"
  name   = "www"
}
# Terraform queries existing DNS record
```

**Decision criteria:**
- **Resource** if you want Terraform to create/manage it
- **Data source** if it exists externally and you just need its value

---

## Summary

**Resources = Active Management**
- Create, update, delete infrastructure
- Terraform owns the lifecycle
- State tracked and drift detected
- Use for things Terraform should manage

**Data Sources = Passive Queries**
- Read information only
- No lifecycle management
- No state tracking
- Use for lookups and external data

---

## See Also

- [Building Your First Resource](../tutorials/building-your-first-resource.md) - Resource tutorial
- [Building Your First Data Source](../tutorials/building-your-first-data-source.md) - Data source tutorial
- [Resource Lifecycle Reference](../reference/resource-lifecycle.md) - Resource API
- [Data Source API Reference](../reference/data-source-api.md) - Data source API
