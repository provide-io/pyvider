# Protocols API

Implementation of Terraform Plugin Protocol v6 for gRPC communication.

## Overview

The protocols layer implements the official Terraform Plugin Protocol, handling all communication between Terraform and your provider.

### Key Components

- **Service** - gRPC service implementation
- **Handlers** - RPC method handlers
- **Protocol Buffers** - Auto-generated protobuf code
- **Utils** - Protocol utilities and helpers

### Supported Protocol

Pyvider implements **Terraform Plugin Protocol v6** with full support for:
- Provider configuration
- Resource CRUD operations
- Data source queries
- Provider functions
- Ephemeral resources
- Deferred changes
- State management

### RPC Methods

The protocol includes handlers for:
- `GetProviderSchema` - Schema discovery
- `ValidateProviderConfig` - Configuration validation
- `ConfigureProvider` - Provider setup
- `PlanResourceChange` - Change planning
- `ApplyResourceChange` - Resource apply
- `ReadResource` - State refresh
- `ReadDataSource` - Data source queries
- `CallFunction` - Function invocation

## Implementation Notes

Most protocol interaction is handled automatically by Pyvider. You typically don't need to work with these directly unless:
- Implementing advanced protocol features
- Debugging protocol issues
- Adding protocol extensions

## Module Reference
