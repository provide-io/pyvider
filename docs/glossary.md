# Glossary

Definitions of common terms used in Pyvider and Terraform provider development.

## A

### Attribute

A key-value pair in a schema that defines configuration or state data. Attributes can be strings, numbers, booleans, lists, maps, or complex objects.

**Example:**

```python
"name": a_str(required=True)
```

See: [Schema Types](schema/types.md)

### Async/Await

Python's asynchronous programming syntax. Pyvider uses async/await for non-blocking I/O operations.

**Example:**

```python
async def read(self, ctx):
    data = await provider.api.get_resource(id)
    return State(**data)
```

## B

### Base Class

Abstract classes that provide common functionality. Pyvider provides `BaseProvider`, `BaseResource`, `BaseDataSource`, etc.

### Block

A structured container in Terraform that can hold attributes and other blocks. Defined with `b_*` functions in Pyvider.

**Example:**

```hcl
config {
  timeout = 30
  retries = 3
}
```

See: [Schema Blocks](schema/blocks.md)

## C

### Component

A registered Terraform provider element (provider, resource, data source, or function).

### Component Hub

Pyvider's auto-discovery system that registers and manages all components via decorators.

See: [Component Model](explanation/component-model.md)

### Computed Attribute

An attribute whose value is determined by the provider, not the user. Marked with `computed=True`.

**Example:**

```python
"id": a_str(computed=True)
```

### Config

User-provided configuration for a resource, data source, or provider.

### Context (`ctx`)

An object passed to lifecycle methods containing configuration, state, and other runtime data.

### CRUD

Create, Read, Update, Delete - the four basic operations for managing resources.

### CTY

Terraform's type system (Configuration Type System). Pyvider handles CTY conversion automatically.

## D

### Data Source

A read-only component that fetches external data for use in Terraform configurations.

**Example:**

```python
@register_data_source("user")
class User(BaseDataSource):
    async def read(self, ctx):
        return UserData(...)
```

See: [Creating Data Sources](guides/building-components/creating-data-sources.md)

### Decorator

Python syntax (`@decorator`) used to register components with Pyvider.

**Examples:**

- `@register_provider("name")`
- `@register_resource("name")`
- `@register_data_source("name")`

## E

### Ephemeral Resource

A short-lived resource with open/renew/close lifecycle instead of create/update/delete. Used for temporary credentials, sessions, etc.

See: [API Reference - Ephemerals](api/ephemerals.md)

## F

### Factory Function

Functions like `a_str()`, `s_resource()`, `b_list()` that create schema objects.

### Flavor / Flavorpack

A packaging tool for creating standalone Python application binaries. Used to package Pyvider providers.

### Function

A callable component that performs transformations or computations in Terraform.

**Example:**

```python
@register_function(name="encode_base64")
class EncodeBase64(BaseFunction):
    async def call(self, ctx):
        return base64.b64encode(ctx.params.input)
```

## G

### gRPC

Google Remote Procedure Call - the communication protocol between Terraform and providers.

## H

### HCL (HashiCorp Configuration Language)

Terraform's configuration language.

**Example:**

```hcl
resource "mycloud_server" "web" {
  name = "web-server"
  size = "large"
}
```

### Hub

See: Component Hub

## I

### Import

The process of bringing existing infrastructure under Terraform management. Resources can implement `import_resource()` to support this.

## L

### Lifecycle

The sequence of operations a resource goes through: create, read, update, delete (CRUD).

## M

### Metadata

Information about a provider (name, version, protocol version).

**Example:**

```python
ProviderMetadata(
    name="mycloud",
    version="1.0.0",
    protocol_version="6"
)
```

## P

### Plan

Terraform's preview of changes before applying them. Shows what will be created, updated, or destroyed.

### Plugin Protocol

The specification for communication between Terraform and providers. Pyvider implements Protocol v6.

### Private State

Encrypted storage for sensitive data that shouldn't appear in terraform.tfstate.

**Example:**

```python
return state, {"password": db.password}  # Private state (encrypted)
```

See: [Security Best Practices](guides/production/security-best-practices.md)

### Provider

The root component that configures authentication and shared resources for a Terraform provider.

**Example:**

```python
@register_provider("mycloud")
class MyCloudProvider(BaseProvider):
    async def configure(self, config):
        self.api_client = APIClient(config["api_key"])
```

See: [Creating Providers](guides/building-components/creating-providers.md)

### Protocol v6

Version 6 of the Terraform Plugin Protocol. Pyvider implements this version.

### PvsSchema

Pyvider Schema - the schema definition type returned by `s_resource()`, `s_provider()`, etc.

## R

### Read Operation

Fetching the current state of a resource from the actual infrastructure to detect drift.

### Register

The act of making a component available to Terraform via a decorator.

### Required Attribute

An attribute that users must provide. Marked with `required=True`.

**Example:**

```python
"api_key": a_str(required=True)
```

### Resource

A manageable infrastructure component with full CRUD lifecycle.

**Example:**

```python
@register_resource("server")
class Server(BaseResource):
    async def _create_apply(self, ctx):
        # Create server
        pass
```

See: [Creating Resources](guides/building-components/creating-resources.md)

## S

### Schema

Defines the structure, types, and constraints of configuration and state data.

**Example:**

```python
s_resource({
    "name": a_str(required=True),
    "port": a_num(default=8080),
})
```

See: [Schema System](schema/overview.md)

### Sensitive Attribute

An attribute whose value should be masked in logs and output. Marked with `sensitive=True`.

**Example:**

```python
"password": a_str(sensitive=True)
```

### State

The current condition of managed infrastructure, stored by Terraform.

### State Drift

When actual infrastructure differs from Terraform's state file. Detected via `read()` operations.

## T

### Terraform

HashiCorp's infrastructure-as-code tool.

### Type System

Pyvider's schema type system that maps Python types to Terraform types (CTY).

## U

### Update Operation

Modifying an existing resource. An "update" is triggered when a user modifies a non-computed attribute of an existing resource in their .tf configuration and runs `terraform apply`. Implemented in `_update_apply()`.

## V

### Validator

A function that checks if an attribute value is valid.

**Example:**

```python
"port": a_num(
    validators=[
        lambda x: 1 <= x <= 65535 or "Invalid port"
    ]
)
```

See: [Schema Validators](schema/validators.md)

## W

### Workspace

A Terraform workspace containing separate state. Providers may need to handle multi-workspace scenarios.

______________________________________________________________________

## Related Documentation

- [Core Concepts](explanation/architecture.md) - Architecture overview
- [Component Model](explanation/component-model.md) - How components work
- [Schema System](schema/overview.md) - Schema definitions
- [Quick Reference](quick-reference.md) - API quick lookup
- [FAQ](faq.md) - Frequently asked questions

______________________________________________________________________

**Missing a term?** [Suggest an addition](https://github.com/provide-io/pyvider/discussions) in GitHub Discussions.
