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

### Known Limitations: Deferred Changes

A component that raises `Deferral` is honored only when the client sets
`client_capabilities.deferral_allowed` on that request. When it does not,
Pyvider returns an `Invalid Deferral` error diagnostic, as the protocol
requires. Two client gaps make this reachable today:

- **Terraform 1.16.3 and earlier** send an empty client-capabilities
  message on `OpenEphemeralResource` and on the `PlanResourceChange` call
  for a partially-expanded resource, so a deferral from either is an error
  even with deferrals enabled. Fixed in Terraform 1.16.4
  ([hashicorp/terraform#39237](https://github.com/hashicorp/terraform/pull/39237)).
  Deferrals themselves are enabled only in experimental Terraform builds and
  in Stacks; stable builds reject `-allow-deferral`.
- **OpenTofu (through v1.13.0-rc1)** never sets `deferral_allowed`, so any
  deferral is returned as an error.

## Module Reference
