# Building Your First Resource

!!! info "Alpha Status"
    pyvider is in alpha. This tutorial covers **stable** functionality.
    See [project status](../index/) for details.

Welcome! In this tutorial, you'll build your first Terraform resource using pyvider. By the end, you'll have a working file resource that creates, reads, updates, and deletes local files through Terraform.

**What You'll Learn:**

- How resources work in Terraform
- Creating a resource class with pyvider
- Defining schemas for user configuration
- Implementing lifecycle methods (CRUD operations)
- Testing your resource with Terraform

**Time to Complete:** 15-20 minutes

**Prerequisites:**

- Python 3.11+ installed
- pyvider installed ([installation guide](../getting-started/installation/))
- Basic Python knowledge
- Basic Terraform knowledge

---

## What is a Resource?

A resource in Terraform represents a piece of infrastructure that can be managed (created, updated, deleted). Think of resources as the things you want to manage:

- A file on disk
- A server in the cloud
- A database record
- An API object

Resources have a **lifecycle**:

1. **Create** - Make something new
2. **Read** - Check current state
3. **Update** - Modify existing thing
4. **Delete** - Remove it

Terraform handles this lifecycle automatically. You just implement the operations!

---

## Step 1: Create Your Provider Package

First, let's create a simple provider package structure:

```bash
mkdir -p my_provider/resources
touch my_provider/__init__.py
touch my_provider/resources/__init__.py
touch my_provider/resources/file.py
```

Your structure should look like:
```
my_provider/
├── __init__.py
└── resources/
    ├── __init__.py
    └── file.py      # We'll work in this file
```

---

## Step 2: Define Runtime Types

Open `my_provider/resources/file.py` and start by defining the data structures.

Resources work with two types of data:

- **Configuration** - What the user provides in their Terraform code
- **State** - What actually exists (tracked by Terraform)

Let's define these using attrs:

```python
import attrs

# Configuration: User inputs from Terraform
@attrs.define
class FileConfig:
    """What the user configures."""
    path: str           # Where to create the file
    content: str        # What to write in the file
    mode: str = "644"   # File permissions (optional, defaults to 644)

# State: What we track
@attrs.define
class FileState:
    """What Terraform tracks about the file."""
    id: str             # Unique identifier
    path: str           # File path
    content: str        # Current content
    mode: str           # Current permissions
    size: int           # File size in bytes (computed by us)
```

**Why separate Config and State?**

- Config = what user wants
- State = what currently exists
- Terraform compares them to know when to update

---

## Step 3: Create the Resource Class

Now let's create the resource class itself:

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, a_num, PvsSchema

@register_resource("file")
class File(BaseResource):
    """Manages a local file."""

    # Link our runtime types
    config_class = FileConfig
    state_class = FileState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define what Terraform users see."""
        return s_resource({
            # User inputs
            "path": a_str(required=True, description="File path"),
            "content": a_str(required=True, description="File content"),
            "mode": a_str(default="644", description="File permissions"),

            # Provider outputs (we compute these)
            "id": a_str(computed=True, description="File ID"),
            "size": a_num(computed=True, description="File size in bytes"),
        })
```

**What's happening here?**

- `@register_resource("file")` - Registers this as a Terraform resource
- `config_class` / `state_class` - Links our attrs classes
- `get_schema()` - Defines what users configure in Terraform HCL

---

## Step 4: Implement Read (Check State)

The `read()` method checks if the resource still exists and returns its current state:

```python
async def read(self, ctx: ResourceContext) -> FileState | None:
    """Refresh state from filesystem."""
    # If no existing state, nothing to read
    if not ctx.state:
        return None

    from pathlib import Path
    file_path = Path(ctx.state.path)

    # Check if file still exists
    if not file_path.exists():
        return None  # File was deleted outside Terraform

    # File exists! Return current state
    content = file_path.read_text()
    return FileState(
        id=ctx.state.id,
        path=str(file_path),
        content=content,
        mode=ctx.state.mode,
        size=len(content),
    )
```

**Why return None?**

- `None` tells Terraform "this resource doesn't exist anymore"
- Terraform will then know to recreate it

---

## Step 5: Implement Create

The `_create_apply()` method creates a new file:

```python
async def _create_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
    """Create file."""
    if not ctx.config:
        return None, None

    from pathlib import Path
    file_path = Path(ctx.config.path)

    # Write the file
    file_path.write_text(ctx.config.content)

    # Return new state
    return FileState(
        id=str(file_path.absolute()),
        path=str(file_path),
        content=ctx.config.content,
        mode=ctx.config.mode,
        size=len(ctx.config.content),
    ), None
```

**Return value explained:**

- First element: New state to track
- Second element: Private data (advanced, we don't need it)

---

## Step 6: Implement Update

The `_update_apply()` method modifies an existing file:

```python
async def _update_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
    """Update file."""
    if not ctx.config or not ctx.state:
        return None, None

    from pathlib import Path
    file_path = Path(ctx.state.path)

    # Update the file content
    file_path.write_text(ctx.config.content)

    # Return updated state
    return FileState(
        id=ctx.state.id,
        path=ctx.state.path,
        content=ctx.config.content,
        mode=ctx.config.mode,
        size=len(ctx.config.content),
    ), None
```

---

## Step 7: Implement Delete

The `_delete_apply()` method removes the file:

```python
async def _delete_apply(self, ctx: ResourceContext) -> None:
    """Delete file."""
    if not ctx.state:
        return

    from pathlib import Path
    file_path = Path(ctx.state.path)

    # Delete file if it exists
    if file_path.exists():
        file_path.unlink()
```

---

## Step 8: Add Validation (Optional but Recommended)

Let's add configuration validation to prevent bad inputs:

```python
async def _validate_config(self, config: FileConfig) -> list[str]:
    """Validate configuration."""
    errors = []

    # Prevent path traversal attacks
    if ".." in config.path:
        errors.append("Path cannot contain '..'")

    # Validate file mode format
    if not config.mode.isdigit() or len(config.mode) != 3:
        errors.append("Mode must be 3 digits (e.g., '644')")

    return errors
```

---

## Complete Code

Here's your complete `file.py`:

```python
import attrs
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, a_num, PvsSchema
from pathlib import Path

# Runtime configuration class
@attrs.define
class FileConfig:
    path: str
    content: str
    mode: str = "644"

# Runtime state class
@attrs.define
class FileState:
    id: str
    path: str
    content: str
    mode: str
    size: int

@register_resource("file")
class File(BaseResource):
    """Manages a local file."""

    config_class = FileConfig
    state_class = FileState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define Terraform schema."""
        return s_resource({
            # User inputs
            "path": a_str(required=True, description="File path"),
            "content": a_str(required=True, description="File content"),
            "mode": a_str(default="644", description="File permissions"),

            # Provider outputs
            "id": a_str(computed=True, description="File ID"),
            "size": a_num(computed=True, description="File size in bytes"),
        })

    async def _validate_config(self, config: FileConfig) -> list[str]:
        """Validate configuration."""
        errors = []
        if ".." in config.path:
            errors.append("Path cannot contain '..'")
        return errors

    async def read(self, ctx: ResourceContext) -> FileState | None:
        """Refresh state from filesystem."""
        if not ctx.state:
            return None

        file_path = Path(ctx.state.path)

        if not file_path.exists():
            return None  # File deleted outside Terraform

        content = file_path.read_text()
        return FileState(
            id=ctx.state.id,
            path=str(file_path),
            content=content,
            mode=ctx.state.mode,
            size=len(content),
        )

    async def _create_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        """Create file."""
        if not ctx.config:
            return None, None

        file_path = Path(ctx.config.path)
        file_path.write_text(ctx.config.content)

        return FileState(
            id=str(file_path.absolute()),
            path=str(file_path),
            content=ctx.config.content,
            mode=ctx.config.mode,
            size=len(ctx.config.content),
        ), None

    async def _update_apply(self, ctx: ResourceContext) -> tuple[FileState | None, None]:
        """Update file."""
        if not ctx.config or not ctx.state:
            return None, None

        file_path = Path(ctx.state.path)
        file_path.write_text(ctx.config.content)

        return FileState(
            id=ctx.state.id,
            path=ctx.state.path,
            content=ctx.config.content,
            mode=ctx.config.mode,
            size=len(ctx.config.content),
        ), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete file."""
        if not ctx.state:
            return

        file_path = Path(ctx.state.path)
        if file_path.exists():
            file_path.unlink()
```

---

## Step 9: Test with Terraform

Create a Terraform configuration file `test.tf`:

```hcl
terraform {
  required_providers {
    local = {
      source = "mycompany/local"
    }
  }
}

resource "local_file" "greeting" {
  path    = "hello.txt"
  content = "Hello from Terraform!"
  mode    = "644"
}

output "file_size" {
  value = local_file.greeting.size
}
```

Run it:

```bash
terraform init
terraform plan
terraform apply
```

You should see:

- `terraform plan` shows the file will be created
- `terraform apply` creates `hello.txt`
- The output shows the file size

Try modifying the content and running `terraform apply` again to see updates!

---

## What You've Learned

Congratulations! You've built your first pyvider resource. You now understand:

✅ **Resource Lifecycle** - Create, read, update, delete operations
✅ **Schema Definition** - Defining what users configure
✅ **Runtime Types** - Separating config from state
✅ **Validation** - Preventing bad configurations
✅ **Testing** - Using Terraform to test your resource

---

## Next Steps

Now that you understand the basics, explore:

- **[Building Your First Data Source](building-your-first-data-source/)** - Read-only queries
- **[How to Create a Resource](../how-to-guides/resources/create-resource/)** - Quick reference
- **[Add Validation](../how-to-guides/resources/add-validation/)** - Advanced validation patterns
- **[Resource Lifecycle Reference](../reference/resource-lifecycle/)** - Complete API documentation
- **[Intermediate Provider Tutorial](intermediate-provider/)** - Build a more complex HTTP API provider

---

## Troubleshooting

**Q: My resource isn't being registered**

Make sure you're calling `register_resource()` as a decorator and importing the module.

**Q: Validation errors aren't showing**

Check that `_validate_config()` is async and returns a list of strings.

**Q: State isn't being tracked**

Ensure you're returning `FileState` objects from `_create_apply()` and `_update_apply()`.

For more help, see [Troubleshooting Guide](../troubleshooting/).
