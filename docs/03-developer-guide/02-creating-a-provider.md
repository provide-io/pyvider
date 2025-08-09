# 🛠️ Creating a Provider

This guide will help you create a new `pyvider` provider.

## 🚀 Setting up a New Provider Project

To create a new provider project, you can use the `pyvider` command-line tool:

```bash
pyvider new my-provider
```

This will create a new directory called `my-provider` with a basic provider project structure, including a `pyproject.toml` file, a `src` directory, and a `tests` directory.

## 📄 Defining the Provider Schema

The provider schema defines the configuration options for the provider. You can define the provider schema in the `provider.py` file using the `@provider` decorator.

```python
from pyvider.providers import provider, ProviderConfig

@provider
class MyProvider(ProviderConfig):
    """
    MyProvider is a custom provider that does amazing things.
    """
    my_api_key: str
```

In this example, we define a provider with a single configuration option, `my_api_key`.

## 🧠 Implementing the Provider Logic

The provider logic is implemented in the `provider.py` file. The provider logic is responsible for configuring the provider and creating the resources, data sources, and functions.

```python
from pyvider.providers import provider, ProviderConfig

@provider
class MyProvider(ProviderConfig):
    """
    MyProvider is a custom provider that does amazing things.
    """
    my_api_key: str

    def configure(self):
        # Initialize the provider with the given configuration.
        pass
```

In this example, we implement the `configure` method, which is called by `pyvider` to configure the provider.
