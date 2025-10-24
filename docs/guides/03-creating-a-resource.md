# 📦 Creating a Resource

This guide will help you create a new resource for your `pyvider` provider.

## 📄 Defining the Resource Schema

The resource schema defines the configuration options for the resource. You can define the resource schema in a new file in the `resources` directory, using the `@resource` decorator.

```python
from pyvider.resources import resource, ResourceConfig

@resource
class MyResource(ResourceConfig):
    """
    MyResource is a custom resource that does amazing things.
    """
    name: str
```

In this example, we define a resource with a single configuration option, `name`.

## 🧠 Implementing the Resource Logic

The resource logic is implemented in the same file as the resource schema. The resource logic is responsible for creating, reading, updating, and deleting the resource.

```python
from pyvider.resources import resource, ResourceConfig

@resource
class MyResource(ResourceConfig):
    """
    MyResource is a custom resource that does amazing things.
    """
    name: str

    def create(self, ctx):
        # Create the resource.
        pass

    def read(self, ctx):
        # Read the resource.
        pass

    def update(self, ctx):
        # Update the resource.
        pass

    def delete(self, ctx):
        # Delete the resource.
        pass
```

In this example, we implement the `create`, `read`, `update`, and `delete` methods, which are called by `pyvider` to manage the resource lifecycle.

## 💾 Handling State

`pyvider` handles the resource state for you. The framework automatically saves the resource state to the Terraform state file. You can access the resource state in your resource logic using the `ctx.state` object.
