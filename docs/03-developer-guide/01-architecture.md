# Chapter 4: The Alchemist's Handbook - The Developer Guide

Welcome, alchemist, to the developer guide. In this chapter, you'll learn how to transmute your ideas into pure gold, using the power of `pyvider`. You'll learn how to create your own resources, data sources, and functions, and how to combine them to create powerful and sophisticated providers.

## 🏛️ The Philosopher's Stone: The Architecture

At the heart of `pyvider` is a simple and elegant architecture that is designed to be both powerful and easy to use. The core components of the framework are:

- **Hub:** The hub is the central registry for all the components in the framework. It's responsible for discovering and registering resources, data sources, and functions.
- **Providers:** A provider is a collection of resources, data sources, and functions. It's the main entry point for your provider.
- **Resources:** A resource is a manageable infrastructure object, such as a VM, database, or network. Resources have a lifecycle that includes creating, reading, updating, and deleting.
- **Data Sources:** A data source is a read-only view of an external API or service. Data sources are used to fetch information that can be used to configure other resources.
- **Functions:** A function is a piece of custom logic that can be called from within a Terraform configuration. Functions are used to perform calculations or transformations that are not possible with the built-in Terraform functions.

## 🔌 The Universal Language: Communication with Terraform

`pyvider` communicates with Terraform using the gRPC protocol. The framework uses the `tfplugin6` protocol, which is the latest version of the Terraform plugin protocol. This protocol defines the messages and services that are used to communicate between Terraform and the provider.
