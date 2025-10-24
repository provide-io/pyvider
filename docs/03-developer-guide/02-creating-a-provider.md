# 🛠️ Creating a Provider

This guide will help you create a new `pyvider` provider.

## 🚀 Setting up a New Provider Project

To create a new provider project, you can use the `pyvider` command-line tool:

```bash
pyvider new my-provider
```

This will create a new directory called `my-provider` with a basic provider project structure, including a `pyproject.toml` file, a `src` directory, and a `tests` directory.

## 📄 Defining the Provider Schema

The provider schema defines the configuration options for the provider. You can define the provider schema in the `provider.py` file using the `@register_provider` decorator.

```python
from pyvider.providers import register_provider, BaseProvider, ProviderMetadata
from pyvider.schema import Attribute
import attrs

@register_provider("myprovider")
class MyProvider(BaseProvider):
    """
    MyProvider is a custom provider that does amazing things.
    """

    def __init__(self):
        super().__init__(
            metadata=ProviderMetadata(
                name="myprovider",
                version="1.0.0"
            )
        )

    @attrs.define
    class Config:
        my_api_key: str = Attribute(
            required=True,
            sensitive=True,
            description="API key for authentication"
        )
```

In this example, we define a provider with a single configuration option, `my_api_key`.

## 🧠 Implementing the Provider Logic

The provider logic is implemented in the `provider.py` file. The provider logic is responsible for configuring the provider and creating the resources, data sources, and functions.

```python
from pyvider.providers import register_provider, BaseProvider, ProviderMetadata
from pyvider.schema import Attribute
import attrs

@register_provider("myprovider")
class MyProvider(BaseProvider):
    """
    MyProvider is a custom provider that does amazing things.
    """

    def __init__(self):
        super().__init__(
            metadata=ProviderMetadata(
                name="myprovider",
                version="1.0.0"
            )
        )

    @attrs.define
    class Config:
        my_api_key: str = Attribute(
            required=True,
            sensitive=True,
            description="API key for authentication"
        )

    async def configure(self, config: Config) -> None:
        """Configure the provider with the given configuration."""
        # Initialize your API client or other setup
        pass
```

In this example, we implement the `configure` method, which is called by `pyvider` to configure the provider.
