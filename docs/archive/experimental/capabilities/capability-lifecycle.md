# 🔄 Capability Lifecycle

This guide explains the `pyvider` capability lifecycle.

## 📄 Overview

The `pyvider` capability lifecycle consists of the following steps:

1.  **Initialization:** `pyvider` initializes the capability and discovers the resources, data sources, and functions.
2.  **Configuration:** `pyvider` configures the capability with the configuration from the Terraform configuration file.
3.  **Termination:** `pyvider` terminates the capability.

## 🧠 Implementing the Capability Logic

You can hook into the capability lifecycle by implementing the following methods in your capability class:

-   `configure`: This method is called to configure the capability.
-   `setup`: This method is called to set up the capability.
-   `teardown`: This method is called to tear down the capability.
```
