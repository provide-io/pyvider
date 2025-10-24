# 🧮 Computed Attributes

This guide explains how to use computed attributes in your `pyvider` schema.

## 📄 Overview

Computed attributes are attributes whose values are not known until the resource is created or updated. Computed attributes are defined using the `computed` argument in the `Attribute` class.

## 🚀 Basic Example

Here is a basic example of how to define a computed attribute:

```python
from pyvider.schema import Attribute

my_attribute = Attribute(
    name="my_attribute",
    type="string",
    computed=True,
    description="This is my computed attribute.",
)
```

In this example, we define a computed attribute named `my_attribute` with a type of `string`.

## 🧠 Implementing the Resource Logic

When you have a computed attribute, you need to set its value in the `create` and `update` methods of your resource.

```python
from pyvider.resources import resource, ResourceConfig

@resource
class MyResource(ResourceConfig):
    """
    MyResource is a custom resource that does amazing things.
    """
    my_attribute: str

    def create(self, ctx):
        # Create the resource.
        ctx.state["my_attribute"] = "my-computed-value"

    def read(self, ctx):
        # Read the resource.
        pass

    def update(self, ctx):
        # Update the resource.
        ctx.state["my_attribute"] = "my-new-computed-value"

    def delete(self, ctx):
        # Delete the resource.
        pass
```

In this example, we set the value of the `my_attribute` attribute in the `create` and `update` methods.
```
