# Building Your First Resource

!!! info "Release Status"
    Pyvider is in pre-release. This tutorial covers **stable** functionality. Some APIs may change during the pre-release series.
    See [project status](../index.md#-project-status) for details.

Welcome! In this tutorial, you'll build your first Terraform resource using pyvider. By the end, you'll have a working file resource that creates, reads, updates, and deletes local files through Terraform.

**What You'll Learn:**

- How resources work in Terraform
- Creating a resource class with Pyvider
- Defining schemas for user configuration
- Implementing lifecycle methods (CRUD operations)
- Testing your resource with Terraform

**Time to Complete:** 15-20 minutes

**Prerequisites:**

- Python 3.11+ installed
- Pyvider installed ([installation guide](../getting-started/installation.md))
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
--8<-- "snippets/resources/file_complete.py:types"
```

**Why separate Config and State?**

- Config = what user wants
- State = what currently exists
- Terraform compares them to know when to update

---

## Step 3: Create the Resource Class

Now let's create the resource class itself:

```python
--8<-- "snippets/resources/file_complete.py:schema"
```

**What's happening here?**

- `@register_resource("file")` - Registers this as a Terraform resource
- `config_class` / `state_class` - Links our attrs classes
- `get_schema()` - Defines what users configure in Terraform HCL

---

## Step 4: Implement Read (Check State)

The `read()` method checks if the resource still exists and returns its current state:

```python
--8<-- "snippets/resources/file_complete.py:read"
```

**Why return None?**

- `None` tells Terraform "this resource doesn't exist anymore"
- Terraform will then know to recreate it

---

## Step 5: Implement Create

The `_create_apply()` method creates a new file:

```python
--8<-- "snippets/resources/file_complete.py:create"
```

**Return value explained:**

- First element: New state to track
- Second element: Private data (advanced, we don't need it)

---

## Step 6: Implement Update

The `_update_apply()` method modifies an existing file:

```python
--8<-- "snippets/resources/file_complete.py:update"
```

---

## Step 7: Implement Delete

The `_delete_apply()` method removes the file:

```python
--8<-- "snippets/resources/file_complete.py:delete"
```

---

## Step 8: Add Validation (Optional but Recommended)

Let's add configuration validation to prevent bad inputs:

```python
--8<-- "snippets/resources/file_complete.py:validation"
```

---

## Complete Code

Here's your complete `file.py`:

```python
--8<-- "snippets/resources/file_complete.py"
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

Congratulations! You've built your first Pyvider resource. You now understand:

✅ **Resource Lifecycle** - Create, read, update, delete operations
✅ **Schema Definition** - Defining what users configure
✅ **Runtime Types** - Separating config from state
✅ **Validation** - Preventing bad configurations
✅ **Testing** - Using Terraform to test your resource

---

## Next Steps

Now that you understand the basics, explore:

- **[Building Your First Data Source](building-your-first-data-source.md)** - Read-only queries
- **[How to Create a Resource](../how-to-guides/resources/create-resource.md)** - Quick reference
- **[Add Validation](../how-to-guides/resources/add-validation.md)** - Advanced validation patterns
- **[Resource Lifecycle Reference](../reference/resource-lifecycle.md)** - Complete API documentation
- **[Intermediate Provider Tutorial](intermediate-provider.md)** - Build a more complex HTTP API provider

---

## Troubleshooting

**Q: My resource isn't being registered**

Make sure you're calling `register_resource()` as a decorator and importing the module.

**Q: Validation errors aren't showing**

Check that `_validate_config()` is async and returns a list of strings.

**Q: State isn't being tracked**

Ensure you're returning `FileState` objects from `_create_apply()` and `_update_apply()`.

For more help, see [Troubleshooting Guide](../troubleshooting.md).
