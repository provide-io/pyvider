# 🤫 Sensitive Data

This guide explains how to handle sensitive data in your `pyvider` schema.

## 📄 Overview

Sensitive data is data that should not be displayed in the Terraform UI or logs. Sensitive data is defined using the `sensitive` argument in the `Attribute` class.

## 🚀 Basic Example

Here is a basic example of how to define a sensitive attribute:

```python
from pyvider.schema import Attribute

my_attribute = Attribute(
    name="my_attribute",
    type="string",
    sensitive=True,
    description="This is my sensitive attribute.",
)
```

In this example, we define a sensitive attribute named `my_attribute` with a type of `string`.

## 🧠 Behavior in Terraform

When an attribute is marked as sensitive, its value will be replaced with `(sensitive)` in the Terraform UI and logs.
```
