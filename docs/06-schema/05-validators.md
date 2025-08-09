# ✅ Validators

This guide provides a reference for the `pyvider` schema validators.

## 📄 Overview

Validators are used to enforce constraints on the values in your schema. Validators are defined using the `Validator` class.

## 🚀 Basic Example

Here is a basic example of how to define a validator:

```python
from pyvider.schema import Attribute, Validator

my_attribute = Attribute(
    name="my_attribute",
    type="string",
    required=True,
    description="This is my attribute.",
    validators=[
        Validator(
            expression="len(value) > 0",
            message="my_attribute must not be empty.",
        )
    ],
)
```

In this example, we define a validator that checks that the length of the `my_attribute` value is greater than 0.

## ⚙️ Arguments

The `Validator` class accepts the following arguments:

-   `expression`: A Python expression that returns `True` if the value is valid, and `False` otherwise. The `value` variable is available in the expression, and contains the value of the attribute or block.
-   `message`: The error message to display if the validation fails.
```
