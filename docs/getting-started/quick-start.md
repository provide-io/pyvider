# 🚀 Quick Start Guide

Build your first Terraform provider in Python in just 5 minutes! This guide will walk you through creating a simple but functional provider that manages local files.

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ Python 3.11+ installed
- ✅ Pyvider installed (`pip install pyvider`)
- ✅ Terraform installed (for testing)
- ✅ 5 minutes of your time!

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
"""
Local File Provider - A simple Terraform provider for managing local files.
"""

from pathlib import Path
import hashlib
import attrs
from pyvider.providers import register_provider, BaseProvider, ProviderMetadata
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
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
        # Provider config will be set by configure()
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
        """Configure the provider with the given configuration."""
        await super().configure(config)
        # Convert config dict to attrs instance
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
    permissions: str = "644"


@attrs.define
class FileState:
    """File resource state."""
    id: str
    path: str
    content: str
    permissions: str
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
                description="Path to the file (relative to base directory)"
            ),
            "content": a_str(
                required=True,
                description="Content to write to the file"
            ),
            "permissions": a_str(
                default="644",
                description="File permissions (octal notation)"
            ),

            # Computed attributes (set by provider)
            "id": a_str(
                computed=True,
                description="Unique identifier for the file"
            ),
            "checksum": a_str(
                computed=True,
                description="SHA256 checksum of the content"
            ),
            "size": a_num(
                computed=True,
                description="File size in bytes"
            ),
        })

    async def _validate_config(self, config: FileConfig) -> list[str]:
        """Validate configuration."""
        errors = []
        if ".." in config.path:
            errors.append("Path cannot contain '..' for security reasons")
        if config.path.startswith("/"):
            errors.append("Path must be relative, not absolute")
        return errors
    
    async def _create_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        """Create a new file (apply phase)."""
        if not ctx.config:
            return None, None

        # Get provider configuration from hub
        from pyvider.hub import ProviderHub
        provider = ProviderHub.get_provider()
        provider_config = provider.provider_config

        # Construct full path
        base_dir = Path(provider_config.base_directory)
        file_path = base_dir / ctx.config.path

        # Create parent directories if needed
        if provider_config.create_directories:
            file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the file
        file_path.write_text(ctx.config.content)

        # Set permissions
        octal_perms = int(ctx.config.permissions, 8)
        file_path.chmod(octal_perms)

        # Calculate checksum
        checksum = hashlib.sha256(ctx.config.content.encode()).hexdigest()

        # Return state
        return FileState(
            id=str(file_path.absolute()),
            path=str(file_path.absolute()),
            content=ctx.config.content,
            permissions=ctx.config.permissions,
            checksum=checksum,
            size=len(ctx.config.content)
        ), None

    async def read(self, ctx: ResourceContext) -> FileState | None:
        """Read the current state of the file."""
        if not ctx.state:
            return None

        file_path = Path(ctx.state.path)

        # Check if file exists
        if not file_path.exists():
            return None  # File was deleted outside of Terraform

        # Read current content
        content = file_path.read_text()

        # Get current permissions
        mode = file_path.stat().st_mode
        permissions = oct(mode)[-3:]

        # Calculate checksum
        checksum = hashlib.sha256(content.encode()).hexdigest()

        # Return updated state
        return FileState(
            id=ctx.state.id,
            path=ctx.state.path,
            content=content,
            permissions=permissions,
            checksum=checksum,
            size=len(content)
        )

    async def _update_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        """Update an existing file (apply phase)."""
        if not ctx.config or not ctx.state:
            return None, None

        file_path = Path(ctx.state.path)

        # Update content if changed
        if ctx.config.content != ctx.state.content:
            file_path.write_text(ctx.config.content)

        # Update permissions if changed
        if ctx.config.permissions != ctx.state.permissions:
            octal_perms = int(ctx.config.permissions, 8)
            file_path.chmod(octal_perms)

        # Calculate new checksum
        checksum = hashlib.sha256(ctx.config.content.encode()).hexdigest()

        # Return updated state
        return FileState(
            id=ctx.state.id,
            path=ctx.state.path,
            content=ctx.config.content,
            permissions=ctx.config.permissions,
            checksum=checksum,
            size=len(ctx.config.content)
        ), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete the file (apply phase)."""
        if not ctx.state:
            return

        file_path = Path(ctx.state.path)
        if file_path.exists():
            file_path.unlink()

# ============================================
# FILE DATA SOURCE
# ============================================

@attrs.define
class FileContentConfig:
    """Data source configuration."""
    path: str


@attrs.define
class FileContentData:
    """Data source result."""
    id: str
    content: str
    size: int
    checksum: str
    exists: bool


@register_data_source("file_content")
class FileContent(BaseDataSource):
    """Reads content from an existing file."""

    config_class = FileContentConfig
    data_class = FileContentData

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define data source schema."""
        return s_data_source({
            # Configuration (input)
            "path": a_str(
                required=True,
                description="Path to the file to read"
            ),

            # Computed outputs
            "id": a_str(
                computed=True,
                description="File path as ID"
            ),
            "content": a_str(
                computed=True,
                description="File content"
            ),
            "size": a_num(
                computed=True,
                description="File size in bytes"
            ),
            "checksum": a_str(
                computed=True,
                description="SHA256 checksum"
            ),
            "exists": a_bool(
                computed=True,
                description="Whether the file exists"
            ),
        })

    async def read(self, config: FileContentConfig) -> FileContentData:
        """Read file content."""
        # Get provider configuration
        from pyvider.hub import ProviderHub
        provider = ProviderHub.get_provider()
        provider_config = provider.provider_config

        base_dir = Path(provider_config.base_directory)
        file_path = base_dir / config.path

        if file_path.exists():
            content = file_path.read_text()
            checksum = hashlib.sha256(content.encode()).hexdigest()
            return FileContentData(
                id=str(file_path.absolute()),
                content=content,
                size=len(content),
                checksum=checksum,
                exists=True
            )
        else:
            return FileContentData(
                id=str(file_path.absolute()),
                content="",
                size=0,
                checksum="",
                exists=False
            )

# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    # This allows the provider to be run directly
    from pyvider.cli import main
    main()
```

## 🧪 Step 2: Test the Provider Locally

Create a test file `test_provider.py`:

```python
#!/usr/bin/env python3
"""Test the local file provider."""

import asyncio
from pathlib import Path
import tempfile
import shutil

async def test_provider():
    """Test provider operations."""
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"📁 Testing in: {tmpdir}")
        
        # Import our provider components
        from local_provider import LocalProvider, File, FileContent
        
        # Create provider instance
        provider = LocalProvider()
        provider.config = LocalProvider.Config(
            base_directory=tmpdir,
            create_directories=True
        )
        
        # Test creating a file
        print("\n✅ Testing file creation...")
        file_resource = File()
        file_resource.provider = provider
        
        config = File.Config(
            path="test/hello.txt",
            content="Hello, Terraform!",
            permissions="644"
        )
        
        state = await file_resource.create(config)
        print(f"  Created: {state.path}")
        print(f"  Content: {state.content}")
        print(f"  Checksum: {state.checksum}")
        
        # Verify file exists
        actual_path = Path(tmpdir) / "test/hello.txt"
        assert actual_path.exists()
        assert actual_path.read_text() == "Hello, Terraform!"
        
        # Test reading the file
        print("\n📖 Testing file read...")
        read_state = await file_resource.read(state)
        assert read_state is not None
        assert read_state.content == "Hello, Terraform!"
        
        # Test updating the file
        print("\n🔄 Testing file update...")
        new_config = File.Config(
            path="test/hello.txt",
            content="Updated content!",
            permissions="600"
        )
        
        updated_state = await file_resource.update(new_config, state)
        assert updated_state.content == "Updated content!"
        assert actual_path.read_text() == "Updated content!"
        
        # Test data source
        print("\n📊 Testing data source...")
        data_source = FileContent()
        data_source.provider = provider
        
        ds_config = FileContent.Config(path="test/hello.txt")
        ds_state = await data_source.read(ds_config)
        assert ds_state.exists
        assert ds_state.content == "Updated content!"
        
        # Test deletion
        print("\n🗑️ Testing file deletion...")
        await file_resource.delete(updated_state)
        assert not actual_path.exists()
        
        print("\n✨ All tests passed!")

if __name__ == "__main__":
    asyncio.run(test_provider())
```

Run the test:

```bash
python test_provider.py
```

You should see:
```
📁 Testing in: /tmp/tmp_xyz123

✅ Testing file creation...
  Created: /tmp/tmp_xyz123/test/hello.txt
  Content: Hello, Terraform!
  Checksum: 3b7e72f9c8a5d4e2f1a6b8c9d0e3f4g5h6i7j8k9

📖 Testing file read...

🔄 Testing file update...

📊 Testing data source...

🗑️ Testing file deletion...

✨ All tests passed!
```

## 🔧 Step 3: Use with Terraform

Create a Terraform configuration `main.tf`:

```hcl
terraform {
  required_providers {
    local = {
      source = "example.com/tutorial/local"
      version = "0.1.0"
    }
  }
}

# Configure the provider
provider "local" {
  base_directory     = "./managed_files"
  create_directories = true
}

# Create a file resource
resource "local_file" "config" {
  path    = "config/app.conf"
  content = <<-EOT
    # Application Configuration
    app_name = "MyApp"
    version = "1.0.0"
    debug = false
  EOT
  permissions = "644"
}

# Create another file that references the first
resource "local_file" "readme" {
  path    = "README.md"
  content = <<-EOT
    # My Application
    
    Configuration file: ${local_file.config.path}
    Checksum: ${local_file.config.checksum}
    Size: ${local_file.config.size} bytes
  EOT
}

# Read an existing file
data "local_file_content" "license" {
  path = "../LICENSE"
}

# Output values
output "config_checksum" {
  value = local_file.config.checksum
}

output "license_exists" {
  value = data.local_file_content.license.exists
}

output "files_created" {
  value = [
    local_file.config.path,
    local_file.readme.path
  ]
}
```

## 🚀 Step 4: Package and Run the Provider

### Option 1: Development Mode

For development, run the provider directly:

```bash
# Start the provider in development mode
pyvider provide --debug

# In another terminal, run Terraform
terraform init -upgrade
terraform plan
terraform apply
```

### Option 2: Build and Install

Package the provider for distribution using the Flavor build system:

```bash
# Build the provider binary using the build script
# (See CLAUDE.md and scripts/build_provider.py for details)
python scripts/build_provider.py

# The built provider binary will be in the dist/ directory
# Move to Terraform plugin directory
mkdir -p ~/.terraform.d/plugins/example.com/tutorial/local/0.1.0/linux_amd64
cp dist/terraform-provider-local ~/.terraform.d/plugins/example.com/tutorial/local/0.1.0/linux_amd64/

# Now Terraform can find it
terraform init
terraform apply
```

## 📊 Step 5: Verify Results

After running `terraform apply`, you should see:

```
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

config_checksum = "a3f5c7d9e1b3..."
license_exists = true
files_created = [
  "./managed_files/config/app.conf",
  "./managed_files/README.md"
]
```

Check the created files:

```bash
$ tree managed_files/
managed_files/
├── config/
│   └── app.conf
└── README.md

$ cat managed_files/config/app.conf
# Application Configuration
app_name = "MyApp"
version = "1.0.0"
debug = false
```

## 🎉 Congratulations!

You've just built your first Terraform provider in Python! In just a few minutes, you've:

- ✅ Created a complete provider with configuration
- ✅ Implemented a full CRUD resource (File)
- ✅ Added a data source (FileContent)
- ✅ Tested the provider locally
- ✅ Used it with real Terraform configuration

## 🔍 What's Happening Behind the Scenes?

When you run your provider, Pyvider:

1. **Discovers Components**: Finds all `@provider`, `@resource`, and `@data_source` decorators
2. **Generates Schema**: Converts Python types to Terraform schema
3. **Handles Protocol**: Manages all gRPC communication with Terraform
4. **Manages State**: Tracks resource state between operations
5. **Provides Type Safety**: Ensures data matches your type definitions

## 📚 Key Concepts Demonstrated

### 🎯 Decorators
- `@provider`: Registers your provider class
- `@resource`: Defines a manageable resource
- `@data_source`: Creates a read-only data source

### 📋 Schema Definition
- `@attrs.define`: Creates type-safe configuration classes
- `Attribute()`: Defines schema fields with validation
- `computed=True`: Fields calculated by the provider
- `required=True`: Fields that must be provided

### 🔄 Resource Lifecycle
- `create()`: Called when resource is first created
- `read()`: Refreshes resource state
- `update()`: Modifies existing resource
- `delete()`: Removes resource

## 🚦 Next Steps

Now that you understand the basics:

### 1. Enhance the Provider

Add more features to your local file provider:

```python
@resource
class Directory:
    """Manages a local directory."""
    # Implementation here

@function
class HashFile:
    """Computes hash of a file."""
    # Implementation here
```

### 2. Add Error Handling

```python
async def create(self, config: Config) -> State:
    try:
        # ... file operations ...
    except PermissionError:
        raise ResourceError("Insufficient permissions")
    except OSError as e:
        raise ResourceError(f"Failed to create file: {e}")
```

### 3. Add Validation

```python
@attrs.define
class Config:
    path: str = Attribute(
        required=True,
        validators=[
            lambda x: not x.startswith("/"),  # No absolute paths
            lambda x: ".." not in x,  # No parent directory access
        ]
    )
```

### 4. Add Import Support

```python
async def import_resource(self, resource_id: str) -> State:
    """Import existing file into Terraform state."""
    file_path = Path(resource_id)
    if not file_path.exists():
        raise ResourceError(f"File not found: {resource_id}")
    
    content = file_path.read_text()
    # ... return state ...
```

## 📖 Learn More

Ready to dive deeper? Check out:

- **[Pyvider Components Examples](https://github.com/provide-io/pyvider-components)** - 100+ working examples
- **[Architecture Guide](../core-concepts/architecture.md)** - Understand Pyvider's internals
- **[Schema System](../core-concepts/schema-system.md)** - Master schema definition
- **[Testing Providers](../guides/testing-providers.md)** - Write comprehensive tests

## 💡 Tips for Success

1. **Start Simple**: Begin with basic resources before adding complexity
2. **Test Early**: Write tests as you develop
3. **Use Type Hints**: Leverage Python's type system for safety
4. **Handle Errors**: Provide clear error messages for users
5. **Document Well**: Add docstrings to all components

## 🆘 Getting Help

If you run into issues:

- Check the [Troubleshooting Guide](../troubleshooting.md)
- Search [GitHub Issues](https://github.com/provide-io/pyvider/issues)
- Join our [Discord Community](https://discord.gg/pyvider)
- Ask on [Stack Overflow](https://stackoverflow.com/questions/tagged/pyvider)

---

<p align="center">
  🎊 <strong>Congratulations on building your first provider!</strong> 🎊<br>
  Ready for more? Continue to the <a href="../tutorials/first-provider.md">Complete Tutorial →</a>
</p>