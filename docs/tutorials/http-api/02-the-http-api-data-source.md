# 🔮 The `http_api` Data Source

Now, let's create the `http_api` data source.

## 📄 The Schema

First, let's define the schema for our data source. Create a new file called `data_sources/http_api.py` and add the following code:

```python
from pyvider.data_sources import data_source, DataSourceConfig

@data_source
class HttpApi(DataSourceConfig):
    """
    Makes an HTTP GET request to a given URL and returns the response body.
    """
    url: str
```

In this schema, we define a data source named `HttpApi` with a single string attribute: `url`.

## 🧠 The Logic

Now, let's implement the logic for our data source. We'll use the `httpx` library to make the HTTP GET request.

First, we need to add `httpx` to our `pyproject.toml` file:

```toml
# pyproject.toml

[project]
# ...
dependencies = [
    # ...
    "httpx",
]
```

Now, let's update our `data_sources/http_api.py` file with the implementation of the `HttpApi` data source:

```python
import httpx
from pyvider.data_sources import data_source, DataSourceConfig

@data_source
class HttpApi(DataSourceConfig):
    """
    Makes an HTTP GET request to a given URL and returns the response body.
    """
    url: str

    def read(self, ctx):
        response = httpx.get(self.url)
        response.raise_for_status()
        return {
            "id": self.url,
            "body": response.text,
        }
```

And with that, we've created our `http_api` data source! In the next section, we'll learn how to test our new component.
```
