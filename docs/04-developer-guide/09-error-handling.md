# 🚨 Error Handling

This guide explains how to handle errors in your `pyvider` provider.

## 📄 Overview

`pyvider` provides a set of built-in exceptions that you can use to handle errors in your provider. These exceptions are all subclasses of the `PyviderError` exception.

## 🚀 Basic Example

Here is a basic example of how to handle an error in your provider:

```python
from pyvider.exceptions import PyviderError

def my_function():
    raise PyviderError("This is my error message.")
```

In this example, we raise a `PyviderError` exception with a custom error message.

## ⚙️ Available Exceptions

The following exceptions are available:

-   `PyviderError`: The base class for all `pyvider` exceptions.
-   `ConversionError`: An error occurred during type conversion.
-   `FrameworkConfigurationError`: An error occurred during framework configuration.
-   `PluginError`: An error occurred in the plugin.
-   `PyviderValueError`: An invalid value was encountered.
-   `InvalidTypeError`: An invalid type was encountered.
-   `UnsupportedTypeError`: An unsupported type was encountered.
-   `ComponentConfigurationError`: An error occurred during component configuration.
-   `FunctionError`: An error occurred in a function.
-   `FunctionRegistrationError`: An error occurred during function registration.
-   `FunctionValidationError`: An error occurred during function validation.
-   `GRPCError`: An error occurred in the gRPC layer.
-   `ProviderError`: An error occurred in the provider.
-   `ProviderConfigurationError`: An error occurred during provider configuration.
-   `ProviderInitializationError`: An error occurred during provider initialization.
-   `ComponentRegistryError`: An error occurred in the component registry.
-   `ValidatorRegistrationError`: An error occurred during validator registration.
-   `ResourceError`: An error occurred in a resource.
-   `DataSourceError`: An error occurred in a data source.
-   `CapabilityError`: An error occurred in a capability.
-   `ResourceValidationError`: An error occurred during resource validation.
-   `ResourceNotFoundError`: A resource was not found.
-   `ResourceOperationError`: An error occurred during a resource operation.
-   `ResourceLifecycleContractError`: An error occurred in the resource lifecycle contract.
-   `SchemaError`: An error occurred in the schema.
-   `SchemaValidationError`: An error occurred during schema validation.
-   `SchemaRegistrationError`: An error occurred during schema registration.
-   `SchemaParseError`: An error occurred during schema parsing.
-   `SchemaConversionError`: An error occurred during schema conversion.
-   `SerializationError`: An error occurred during serialization.
-   `DeserializationError`: An error occurred during deserialization.
-   `ValidationError`: An error occurred during validation.
-   `AttributeValidationError`: An error occurred during attribute validation.
```
