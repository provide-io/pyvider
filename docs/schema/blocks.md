# 🧱 Blocks

This guide provides a reference for the `pyvider` Block schema type.

## 📄 Overview

Blocks are used to define the nested objects in your schema. Blocks are defined using the `Block` class.

## 🚀 Basic Example

Here is a basic example of how to define a block.

### Terraform Configuration (HCL)

```hcl
resource "my-provider_my-resource" "example" {
  my_block {
    my_attribute = "hello world"
  }
}
```

### Pyvider Schema

```python
from pyvider.schema import Block, Attribute

my_block = Block(
    name="my_block",
    attributes=[
        Attribute(
            name="my_attribute",
            type="string",
            required=True,
            description="This is my attribute.",
        )
    ],
)
```

In this example, we define a block named `my_block` with a single attribute named `my_attribute`.

## ⚙️ Arguments

The `Block` class accepts the following arguments:

-   `name`: The name of the block.
-   `attributes`: A list of attributes in the block.
-   `blocks`: A list of nested blocks in the block.
-   `required`: A boolean indicating whether the block is required.
-   `optional`: A boolean indicating whether the block is optional.
-   `computed`: A boolean indicating whether the block is computed.
-   `sensitive`: A boolean indicating whether the block is sensitive.
-   `description`: A description of the block.
-   `validators`: A list of validators to apply to the block. See the [Validators](./05-validators.md) documentation for a list of available validators.
```
