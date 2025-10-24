# 🚀 Quick Start Guide

Build your first Terraform provider in Python! This guide walks you through creating a simple but functional provider in about 5 minutes.

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ Python 3.11+ installed
- ✅ Pyvider installed (`pip install pyvider` or `uv add pyvider`)
- ✅ Basic understanding of Terraform concepts
- ✅ Familiarity with Python async/await

## ⚠️ Alpha Notice

Pyvider is in alpha. The APIs shown here may change before 1.0. This example is tested and working as of version 0.0.1000.

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
from pyvider.data_sources import register_data_source, BaseDataSource
from pyvider.schema import s_provider, s_resource, s_data_source, a_str, a_num, a_bool, PvsSchema

# ============================================
# PROVIDER DEFINITION
# ============================================

@attrs.define
class ProviderConfig:
    """Provider configuration."""
    base_directory: str = "."
    create_directories: bool = True


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
        self.provider_config: ProviderConfig | None = None

    def _build_schema(self) -> PvsSchema:
        """Define provider schema."""
        return s_provider({
            "base_directory": a_str(
                default=".",
                description="Base directory for file operations"
            ),
            "create_directories": a_bool(
                default=True,
                description="Automatically create parent directories"
            ),
        })

    async def configure(self, config: dict) -> None:
        """Configure the provider."""
        await super().configure(config)
        self.provider_config = ProviderConfig(
            base_directory=config.get("base_directory", "."),
            create_directories=config.get("create_directories", True),
        )

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
            # Configuration attributes
            "path": a_str(
                required=True,
                description="Path to the file"
            ),
            "content": a_str(
                required=True,
                description="Content to write"
            ),

            # Computed attributes
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

        # Get provider config
        from pyvider.hub import hub
        provider = hub.get_component("singleton", "provider")
        if provider is None or provider.provider_config is None:
            raise RuntimeError("Provider is not configured yet.")
        provider_config = provider.provider_config

        # Write file
        file_path = Path(provider_config.base_directory) / ctx.config.path
        if provider_config.create_directories:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(ctx.config.content)

        # Return state
        checksum = hashlib.sha256(ctx.config.content.encode()).hexdigest()
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
  base_directory     = "./managed_files"
  create_directories = true
}

resource "local_file" "config" {
  path    = "config/app.conf"
  content = <<-EOT
    # Application Configuration
    app_name = "MyApp"
    version = "1.0.0"
  EOT
}

output "config_checksum" {
  value = local_file.config.checksum
}
```

## 🚀 Step 3: Run the Provider

```bash
# Make the provider executable
chmod +x local_provider.py

# Run directly for testing
python local_provider.py provide &

# In another terminal, run Terraform
terraform init
terraform plan
terraform apply

# Check the created file
cat managed_files/config/app.conf
```

## 📊 Expected Output

After running `terraform apply`, you should see:

```
Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:

config_checksum = "a3f5c7d9e1b3..."
```

And the file `managed_files/config/app.conf` will exist with your content.

## 🎉 Congratulations!

You've just built your first Terraform provider in Python! You've:

- ✅ Created a provider with configuration
- ✅ Implemented a full CRUD resource
- ✅ Used it with real Terraform

## 🔍 What's Happening?

When you run your provider, Pyvider:

1. **Discovers Components**: Finds all `@register_*` decorators
2. **Generates Schema**: Converts Python types to Terraform schema
3. **Handles Protocol**: Manages gRPC communication with Terraform
4. **Manages State**: Tracks resource state between operations
5. **Provides Type Safety**: Ensures data matches your `@attrs.define` classes

## 🚦 Next Steps

Now that you understand the basics, explore:

### Learn Core Concepts
- **[Architecture Overview](../core-concepts/architecture.md)** - Understand how Pyvider works
- **[Component Model](../core-concepts/component-model.md)** - Deep dive into components
- **[Schema System](../core-concepts/schema-system.md)** - Master schema definition

### Build Real Providers
- **[Creating Providers](../guides/creating-providers.md)** - Comprehensive provider guide
- **[Creating Resources](../guides/creating-resources.md)** - Advanced resource patterns
- **[Testing Providers](../guides/testing-providers.md)** - Write comprehensive tests
- **[Best Practices](../guides/best-practices.md)** - Production-ready patterns

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

## 🆘 Getting Help

If you run into issues:

- Check the [Troubleshooting Guide](../troubleshooting.md)
- Search [GitHub Issues](https://github.com/provide-io/pyvider/issues)
- Ask in [GitHub Discussions](https://github.com/provide-io/pyvider/discussions)

---

<p align="center">
  🎊 <strong>Ready to build more?</strong> 🎊<br>
  Check out the <a href="../guides/creating-providers.md">Complete Provider Development Guide →</a>
</p>
