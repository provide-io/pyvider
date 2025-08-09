# User Guide

This guide will help you get started with using `pyvider` to manage your infrastructure.

## Installation

### Prerequisites

- Python 3.12 or later
- Terraform 1.0 or later

### Installing `pyvider`

You can install `pyvider` using pip:

```bash
pip install pyvider
```

### Installing the Provider

To install a provider, you first need to build it using the `pyvider` command-line tool:

```bash
pyvider build
```

This will create a binary file in the `dist` directory. You can then install the provider by copying the binary to the Terraform plugins directory:

```bash
mkdir -p ~/.terraform.d/plugins/local/providers/my-provider/0.1.0/linux_amd64
cp dist/terraform-provider-my-provider ~/.terraform.d/plugins/local/providers/my-provider/0.1.0/linux_amd64/
```

## Configuration

### Configuring the Provider

To configure the provider, you need to add a `provider` block to your Terraform configuration file:

```terraform
provider "my-provider" {
  # provider-level configuration
}
```

### Authentication

`pyvider` provides a capability to add authentication to your provider. This is demonstrated with an example of API key authentication, but you will need to implement the specific authentication method required for your provider.

### Provider-level Configuration

You can configure the provider using the `provider` block in your Terraform configuration file. The available configuration options will depend on the provider you are using.

## Resources

### Managing Resources

You can manage resources using the `resource` block in your Terraform configuration file. The available resource types will depend on the provider you are using.

### Creating, Reading, Updating, and Deleting Resources

`pyvider` handles the resource lifecycle for you. When you run `terraform apply`, `pyvider` will create, read, update, or delete resources as needed.

### Resource-specific Configuration

You can configure a resource using the `resource` block in your Terraform configuration file. The available configuration options will depend on the resource type you are using.

## Data Sources

### Using Data Sources

You can use data sources to fetch information from an external API or service. To use a data source, you need to add a `data` block to your Terraform configuration file.

### Configuring Data Sources

You can configure a data source using the `data` block in your Terraform configuration file. The available configuration options will depend on the data source you are using.

## Functions

### Using Functions

You can use functions to perform custom logic in your Terraform configuration. To use a function, you need to call it from within your Terraform configuration file.

### Function-specific Configuration

You can configure a function by passing arguments to it when you call it. The available arguments will depend on the function you are using.

## Examples

### Basic Examples

Here is a basic example of how to use `pyvider` to manage a simple resource:

```terraform
resource "my-provider_my-resource" "example" {
  name = "my-resource"
}
```

### Advanced Examples

Here is an advanced example of how to use `pyvider` to manage a more complex resource:

```terraform
resource "my-provider_my-resource" "example" {
  name = "my-resource"

  nested_block {
    attribute = "value"
  }
}
```

### Real-world Use Cases

`pyvider` can be used to manage a wide variety of infrastructure resources, including:

- Cloud resources (e.g., VMs, databases, networks)
- SaaS services (e.g., monitoring, logging, CI/CD)
- On-premises infrastructure (e.g., servers, storage, networking)
```
