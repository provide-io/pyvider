# 📦 Bundling Components

This guide will help you bundle your `pyvider` components into reusable packages.

## 📄 Overview

`pyvider` allows you to bundle your resources, data sources, functions, and capabilities into reusable packages. This makes it easy to share your components between your providers.

To create a component bundle, you need to create a new Python package with a `pyvider.toml` file. The `pyvider.toml` file should contain a `[components]` section that lists the components in the bundle.

## 🚀 Basic Example

Here is a basic example of a `pyvider.toml` file for a component bundle:

```toml
# pyvider.toml

[components]
resources = [
    "my-resource",
]
data_sources = [
    "my-data-source",
]
functions = [
    "my-function",
]
capabilities = [
    "my-capability",
]
```

In this example, we define a component bundle that contains a resource, a data source, a function, and a capability.
```
