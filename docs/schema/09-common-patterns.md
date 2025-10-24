# 🧩 Common Patterns

This guide provides solutions to common schema design problems.

## 📄 Optional with Default

Sometimes, you want to have an attribute that is optional, but has a default value if it's not set. You can do this using the `optional` and `default` arguments in the `Attribute` class.

```python
from pyvider.schema import Attribute

my_attribute = Attribute(
    name="my_attribute",
    type="string",
    optional=True,
    default="my-default-value",
    description="This is my attribute.",
)
```

## 📄 Required and Computed

Sometimes, you want to have an attribute that is required, but is also computed. This is useful when you have an attribute that is required, but its value is not known until the resource is created.

You can do this by setting both the `required` and `computed` arguments to `True`.

```python
from pyvider.schema import Attribute

my_attribute = Attribute(
    name="my_attribute",
    type="string",
    required=True,
    computed=True,
    description="This is my attribute.",
)
```
```
