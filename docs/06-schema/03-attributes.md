# 📦 Attributes

This guide provides a reference for the `pyvider` Attribute schema type.

## 📄 Overview

Attributes are used to define the simple values in your schema, such as strings, numbers, and booleans. Attributes are defined using the `Attribute` class.

## 🚀 Basic Example

Here is a basic example of how to define an attribute.

### Terraform Configuration (HCL)

```hcl
resource "my-provider_my-resource" "example" {
  my_attribute = "hello world"
}
```

### Pyvider Schema

```python
from pyvider.schema import Attribute

my_attribute = Attribute(
    name="my_attribute",
    type="string",
    required=True,
    description="This is my attribute.",
)
```

In this example, we define an attribute named `my_attribute` with a type of `string`. The `required` attribute is set to `True`, which means that the attribute must be set in the Terraform configuration. The `description` attribute is used to provide a description of the attribute.

## ⚙️ Arguments

The `Attribute` class accepts the following arguments:

-   `name`: The name of the attribute.
-   `type`: The type of the attribute. See the [Types](./02-types.md) documentation for a list of available types.
-   `required`: A boolean indicating whether the attribute is required.
-   `optional`: A boolean indicating whether the attribute is optional.
-   `computed`: A boolean indicating whether the attribute is computed.
-   `sensitive`: A boolean indicating whether the attribute is sensitive.
-   `description`: A description of the attribute.
-   `validators`: A list of validators to apply to the attribute. See the [Validators](./05-validators.md) documentation for a list of available validators.
```
