# 🛠️ Creating Capabilities

This guide will help you create your own `pyvider` capabilities.

## 📄 Overview

Capabilities are created in the same way as resources, data sources, and functions. You can create a new capability by creating a new file in the `capabilities` directory.

## 🚀 Basic Example

Here is a basic example of how to create a capability:

```python
from pyvider.capabilities import capability, CapabilityConfig

@capability
class MyCapability(CapabilityConfig):
    """
    MyCapability is a custom capability that does amazing things.
    """
    my_api_key: str

    def configure(self, provider):
        # Configure the capability.
        pass
```

In this example, we define a capability with a single configuration option, `my_api_key`. We also implement the `configure` method, which is called by `pyvider` to configure the capability.
```
