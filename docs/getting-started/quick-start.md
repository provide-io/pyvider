# 🚀 Quick Start Guide

Build your first Terraform provider in Python! This guide walks you through creating a simple but functional provider in about 5 minutes.

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ Python 3.11+ installed
- ✅ Pyvider installed (`uv add pyvider` or `uv add pyvider`)
- ✅ Basic understanding of Terraform concepts
- ✅ Familiarity with Python async/await

## ⚠️ Alpha Notice

This example is tested and working as of version 0.3.0.

## 🎯 What We'll Build

We'll create a **LocalFile Provider** that can:
- Create text files on your local filesystem
- Read file contents as data sources
- Update files when content changes
- Delete files when resources are destroyed

## 📝 Step 1: Create the Provider

Create a new file called `local_provider.py`:

```python
#!/usr/bin/env python3
"""Local File Provider - A simple Terraform provider for managing local files."""

from pathlib import Path
import hashlib
import attrs
from pyvider.providers import register_provider, BaseProvider, ProviderMetadata
from pyvider.resources import register_resource, BaseResource, ResourceContext
from pyvider.schema import s_provider, s_resource, a_str, a_num, PvsSchema

# ============================================
# PROVIDER DEFINITION
# ============================================

@register_provider("local")
class LocalProvider(BaseProvider):
    """Provider for managing local files."""

    def __init__(self):
        super().__init__(
            metadata=ProviderMetadata(
                name="local",
                version="0.1.0",
                protocol_version="6"
            )
        )

    def _build_schema(self) -> PvsSchema:
        """Define provider schema (no configuration needed for this simple example)."""
        return s_provider({})

# ============================================
# FILE RESOURCE
# ============================================

@attrs.define
class FileConfig:
    """File resource configuration."""
    path: str
    content: str


@attrs.define
class FileState:
    """File resource state."""
    id: str
    path: str
    content: str
    checksum: str
    size: int


@register_resource("file")
class File(BaseResource):
    """Manages a local text file."""

    config_class = FileConfig
    state_class = FileState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define resource schema."""
        return s_resource({
            # Configuration attributes (user inputs)
            "path": a_str(
                required=True,
                description="Path to the file"
            ),
            "content": a_str(
                required=True,
                description="Content to write"
            ),

            # Computed attributes (provider outputs)
            "id": a_str(
                computed=True,
                description="File identifier"
            ),
            "checksum": a_str(
                computed=True,
                description="SHA256 checksum"
            ),
            "size": a_num(
                computed=True,
                description="File size in bytes"
            ),
        })

    async def _create_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        """Create a new file."""
        if not ctx.config:
            return None, None

        # Create file path
        file_path = Path(ctx.config.path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        file_path.write_text(ctx.config.content)

        # Compute checksum
        checksum = hashlib.sha256(ctx.config.content.encode()).hexdigest()

        # Return state
        return FileState(
            id=str(file_path.absolute()),
            path=str(file_path.absolute()),
            content=ctx.config.content,
            checksum=checksum,
            size=len(ctx.config.content)
        ), None

    async def read(self, ctx: ResourceContext) -> FileState | None:
        """Read current file state."""
        if not ctx.state:
            return None

        file_path = Path(ctx.state.path)
        if not file_path.exists():
            return None  # File deleted outside Terraform

        content = file_path.read_text()
        checksum = hashlib.sha256(content.encode()).hexdigest()

        return FileState(
            id=ctx.state.id,
            path=ctx.state.path,
            content=content,
            checksum=checksum,
            size=len(content)
        )

    async def _update_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        """Update file content."""
        if not ctx.config or not ctx.state:
            return None, None

        file_path = Path(ctx.state.path)
        file_path.write_text(ctx.config.content)

        checksum = hashlib.sha256(ctx.config.content.encode()).hexdigest()
        return FileState(
            id=ctx.state.id,
            path=ctx.state.path,
            content=ctx.config.content,
            checksum=checksum,
            size=len(ctx.config.content)
        ), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete the file."""
        if not ctx.state:
            return

        file_path = Path(ctx.state.path)
        if file_path.exists():
            file_path.unlink()

# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    from pyvider.cli import main
    main()
```

## 🔧 Step 2: Create Terraform Configuration

Create `main.tf` in the same directory:

```hcl
terraform {
  required_providers {
    local = {
      source = "example.com/tutorial/local"
      version = "0.1.0"
    }
  }
}

provider "local" {
  # No configuration needed for this simple example
}

resource "local_file" "config" {
  path    = "managed_files/app.conf"
  content = <<-EOT
    # Application Configuration
    app_name = "MyApp"
    version = "1.0.0"
  EOT
}

resource "local_file" "readme" {
  path    = "managed_files/README.md"
  content = "# My Managed Files\n\nThis directory is managed by Terraform."
}

output "config_checksum" {
  value = local_file.config.checksum
}

output "readme_size" {
  value = local_file.readme.size
}
```

## 🚀 Step 3: Install and Run the Provider

### Option A: Development Mode (Recommended for Testing)

The easiest way to test your provider during development is to use `pyvider install`:

```bash
# Make sure you're in a directory with your provider code
# and have pyvider installed in your virtual environment

# Install the provider for Terraform
pyvider install

# Now run Terraform normally - it will find your provider
terraform init
terraform plan
terraform apply

# Check the created files
ls -la managed_files/
cat managed_files/app.conf
cat managed_files/README.md
```

!!! note "How This Works"
    `pyvider install` creates a wrapper script in Terraform's plugin directory that:

    1. Activates your virtual environment
    2. Runs your provider with the correct Python interpreter
    3. Allows Terraform to communicate with your provider via the plugin protocol

    This is the recommended approach for development and testing.

### Option B: Direct Execution (For Debugging)

To test the provider directly without Terraform:

```bash
# Set the Terraform magic cookie (Terraform normally does this)
export TF_PLUGIN_MAGIC_COOKIE="d602bf8f470bc67ca7faa0386276bbdd4330efaf76d1a219cb4e95f7aa66ead0"

# Run the provider
python local_provider.py provide

# In another terminal with the same environment variable,
# run Terraform commands
```

!!! warning "Direct Execution Limitations"
    This approach is useful for debugging but not recommended for normal development.
    The provider must be launched by Terraform to work correctly in production scenarios.

## 📊 Expected Output

After running `terraform apply`, you should see:

```
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

config_checksum = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
readme_size = 62
```

And the files will exist:
- `managed_files/app.conf` with your configuration
- `managed_files/README.md` with the README content

## 🎉 Congratulations!

You've just built your first Terraform provider in Python! You've:

- ✅ Created a provider with minimal configuration
- ✅ Implemented a full CRUD resource (create, read, update, delete)
- ✅ Computed attributes (checksum, size)
- ✅ Used it with real Terraform

## 🔍 What's Happening?

When you run your provider, Pyvider:

1. **Discovers Components**: Finds all `@register_*` decorators
2. **Generates Schema**: Converts Python types to Terraform schema
3. **Handles Protocol**: Manages gRPC communication with Terraform
4. **Manages State**: Tracks resource state between operations
5. **Provides Type Safety**: Ensures data matches your `@attrs.define` classes

## 📚 Understanding the Code

### Provider Configuration

```python
@register_provider("local")
class LocalProvider(BaseProvider):
    """Minimal provider - no configuration needed."""
```

The `@register_provider` decorator registers your provider with Pyvider. For this simple example, we don't need any provider-level configuration.

### Resource Schema

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "path": a_str(required=True, description="Path to the file"),
        "content": a_str(required=True, description="Content to write"),
        "checksum": a_str(computed=True, description="SHA256 checksum"),
    })
```

The schema defines:
- **User inputs**: `path` and `content` (required)
- **Provider outputs**: `checksum` and `size` (computed)

### Resource Context

```python
async def _create_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
    # Access configuration
    file_path = Path(ctx.config.path)
    content = ctx.config.content

    # Create resource
    file_path.write_text(content)

    # Return state
    return FileState(...), None
```

The `ResourceContext` provides:
- `ctx.config` - User configuration (FileConfig)
- `ctx.state` - Previous state (FileState) for updates
- `ctx.planned_state` - Planned state from terraform plan
- `ctx.private_state` - Encrypted private state (if needed)

## 🚦 Next Steps

Now that you understand the basics, explore:

### Learn Core Concepts
- **[Architecture Overview](../explanation/architecture.md)** - Understand how Pyvider works
- **[Component Model](../explanation/component-model.md)** - Deep dive into components
- **[Schema System](../explanation/schema-system.md)** - Master schema definition

### Build Real Providers
- **[Creating Providers](../guides/building-components/creating-providers.md)** - Comprehensive provider guide
- **[Creating Resources](../guides/building-components/creating-resources.md)** - Advanced resource patterns
- **[Testing Providers](../guides/development/testing-providers.md)** - Write comprehensive tests
- **[Best Practices](../guides/production/best-practices.md)** - Production-focused patterns

### See Examples
- **[Pyvider Components](https://github.com/provide-io/pyvider-components)** - 100+ working examples including:
  - Resources: file_content, local_directory, timed_token
  - Data Sources: env_variables, http_api, lens_jq
  - Functions: String, numeric, and JQ operations

## 💡 Tips for Success

1. **Start Simple**: Begin with basic resources before adding complexity
2. **Test Incrementally**: Test each component as you develop
3. **Use Type Hints**: Leverage Python's type system for safety
4. **Handle Errors Gracefully**: Provide clear error messages
5. **Document Thoroughly**: Add docstrings and schema descriptions

## 🔄 Making Changes

Try modifying the example:

### Add Validation

```python
async def _validate_config(self, config: FileConfig) -> list[str]:
    """Validate configuration."""
    errors = []
    if ".." in config.path:
        errors.append("Path cannot contain '..'")
    if len(config.content) > 1_000_000:
        errors.append("Content too large (max 1MB)")
    return errors
```

### Add a Data Source

```python
@register_data_source("file_info")
class FileInfo(BaseDataSource):
    """Read file metadata."""

    @classmethod
    def get_schema(cls):
        return s_data_source({
            "path": a_str(required=True),
            "exists": a_bool(computed=True),
            "size": a_num(computed=True),
        })

    async def read(self, ctx: ResourceContext):
        file_path = Path(ctx.config.path)
        return FileInfoState(
            path=str(file_path),
            exists=file_path.exists(),
            size=file_path.stat().st_size if file_path.exists() else 0
        )
```

## 🆘 Getting Help

If you run into issues:

- Check the [Troubleshooting Guide](../troubleshooting.md)
- Search [GitHub Issues](https://github.com/provide-io/pyvider/issues)
- Ask in [GitHub Discussions](https://github.com/provide-io/pyvider/discussions)
- Review [pyvider-components examples](https://github.com/provide-io/pyvider-components)

---

<p align="center">
  🎊 <strong>Ready to build more?</strong> 🎊<br>
  Check out the <a href="../guides/creating-providers.md">Complete Provider Development Guide →</a>
</p>
