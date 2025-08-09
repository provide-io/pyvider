# 🧩 Capability Composition

This guide explains how to compose `pyvider` capabilities.

## 📄 Overview

`pyvider` allows you to compose capabilities to create more complex and powerful providers. You can compose capabilities by adding them to the `capabilities` list in your provider's `pyvider.toml` file.

## 🚀 Basic Example

Here is a basic example of how to compose capabilities:

```toml
# pyvider.toml

[provider]
name = "my-provider"

[build]
capabilities = [
    "my-capability-1",
    "my-capability-2",
]
```

In this example, we add the `my-capability-1` and `my-capability-2` capabilities to our provider. `pyvider` will automatically discover and register the capabilities with the `hub`.

## 🧠 Capability Order

The order in which you list the capabilities in the `pyvider.toml` file is important. `pyvider` will initialize and configure the capabilities in the order they are listed. This means that if you have a capability that depends on another capability, you should list the dependency first.
```
