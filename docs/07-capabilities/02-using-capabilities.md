# 🚀 Using Capabilities

This guide will help you use capabilities in your `pyvider` provider.

## 📄 Overview

Capabilities are used to extend the functionality of your provider. To use a capability, you need to add it to the `capabilities` list in your provider's `pyvider.toml` file.

## 🚀 Basic Example

Here is a basic example of how to use a capability:

```toml
# pyvider.toml

[provider]
name = "my-provider"

[build]
capabilities = [
    "my-capability",
]
```

In this example, we add the `my-capability` capability to our provider. `pyvider` will automatically discover and register the capability with the `hub`.
```
