# 🧮 Creating a Function

This guide will help you create a new function for your `pyvider` provider.

## 📄 Defining the Function Schema

The function schema defines the arguments and return value for the function. You can define the function schema in a new file in the `functions` directory, using the `@function` decorator.

```python
from pyvider.functions import function

@function
def my_function(input: str) -> str:
    """
    MyFunction is a custom function that does amazing things.
    """
    return input.upper()
```

In this example, we define a function with a single string argument and a string return value.

## 🧠 Implementing the Function Logic

The function logic is implemented in the same file as the function schema. The function logic is responsible for performing the custom logic.

```python
from pyvider.functions import function

@function
def my_function(input: str) -> str:
    """
    MyFunction is a custom function that does amazing things.
    """
    return input.upper()
```

In this example, we implement the function logic directly in the function body.
