# 📊 The `jq` Data Source

Now that we have our `jq` function, let's create the `jq` data source. This data source will read a JSON file and apply a `jq` filter to it.

## 📄 The Schema

First, let's define the schema for our data source. Create a new file called `data_sources/jq.py` and add the following code:

```python
from pyvider.data_sources import data_source, DataSourceConfig

@data_source
class Jq(DataSourceConfig):
    """
    Reads a JSON file and applies a jq filter to it.
    """
    path: str
    filter: str
```

In this schema, we define a data source named `Jq` with two string attributes: `path` and `filter`.

## 🧠 The Logic

Now, let's implement the logic for our data source. We'll use the `pyjq` library to apply the `jq` filter to the JSON file.

```python
import json
import pyjq
from pyvider.data_sources import data_source, DataSourceConfig

@data_source
class Jq(DataSourceConfig):
    """
    Reads a JSON file and applies a jq filter to it.
    """
    path: str
    filter: str

    def read(self, ctx):
        with open(self.path, "r") as f:
            data = json.load(f)

        result = pyjq.one(self.filter, data)

        return {
            "id": self.path,
            "result": result,
        }
```

And with that, we've created our `jq` data source! In the next section, we'll learn how to test our new components.
```
