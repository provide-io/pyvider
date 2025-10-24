# 📊 Creating a Data Source

This guide will help you create a new data source for your `pyvider` provider.

## 📄 Defining the Data Source Schema

The data source schema defines the configuration options for the data source. You can define the data source schema in a new file in the `data_sources` directory, using the `@data_source` decorator.

```python
from pyvider.data_sources import data_source, DataSourceConfig

@data_source
class MyDataSource(DataSourceConfig):
    """
    MyDataSource is a custom data source that does amazing things.
    """
    name: str
```

In this example, we define a data source with a single configuration option, `name`.

## 🧠 Implementing the Data Source Logic

The data source logic is implemented in the same file as the data source schema. The data source logic is responsible for reading the data from the external API or service.

```python
from pyvider.data_sources import data_source, DataSourceConfig

@data_source
class MyDataSource(DataSourceConfig):
    """
    MyDataSource is a custom data source that does amazing things.
    """
    name: str

    def read(self, ctx):
        # Read the data from the external API or service.
        return {
            "id": "my-id",
            "name": self.name,
            "output": "my-output",
        }
```

In this example, we implement the `read` method, which is called by `pyvider` to read the data from the data source.
