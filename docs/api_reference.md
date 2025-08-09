# API Reference

This section provides a reference for the `pyvider` API.

## Provider API

### `PyviderProvider`

The `PyviderProvider` class is the main entry point for a provider. It is responsible for configuring the provider and creating the resources, data sources, and functions.

### `ProviderHandler`

The `ProviderHandler` class is responsible for handling the gRPC requests from Terraform.

## Resource API

### `Resource`

The `Resource` class is the base class for all resources. It provides the basic functionality for managing a resource, such as creating, reading, updating, and deleting the resource.

### `ResourceConfig`

The `ResourceConfig` class is used to define the schema for a resource.

## Data Source API

### `DataSource`

The `DataSource` class is the base class for all data sources. It provides the basic functionality for reading data from an external API or service.

### `DataSourceConfig`

The `DataSourceConfig` class is used to define the schema for a data source.

## Function API

### `Function`

The `Function` class is the base class for all functions. It provides the basic functionality for performing custom logic.

### `FunctionConfig`

The `FunctionConfig` class is used to define the schema for a function.

## Hub API

### `Hub`

The `Hub` class is the central registry for all the components in the framework.

### `ComponentRegistry`

The `ComponentRegistry` class is used to register and discover components.
