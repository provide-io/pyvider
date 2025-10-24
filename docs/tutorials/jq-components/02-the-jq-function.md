# 🛠️ The `jq` Function

The first component we'll create is the `jq` function. This function will take a JSON string and a `jq` filter as input, and return the result of applying the filter to the JSON string.

## 📄 The Schema

First, let's define the schema for our function. Create a new file called `functions/jq.py` and add the following code:

```python
from pyvider.functions import function

@function
def jq(json: str, filter: str) -> str:
    """
    Applies a jq filter to a JSON string.
    """
    # We'll implement this later.
    pass
```

In this schema, we define a function named `jq` with two string arguments: `json` and `filter`. The function returns a string.

## 🧠 The Logic

Now, let's implement the logic for our function. We'll use the `pyjq` library to apply the `jq` filter to the JSON string.

First, we need to add `pyjq` to our `pyproject.toml` file:

```toml
# pyproject.toml

[project]
# ...
dependencies = [
    # ...
    "pyjq",
]
```

Now, let's update our `functions/jq.py` file with the implementation of the `jq` function:

```python
import pyjq
from pyvider.functions import function

@function
def jq(json_string: str, filter: str) -> str:
    """
    Applies a jq filter to a JSON string.
    """
    return pyjq.one(filter, text=json_string)
```

And with that, we've created our `jq` function! In the next section, we'll create the `jq` data source.
```
