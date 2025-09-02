# Changelog

All notable changes to Pyvider will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation suite with architecture guides
- Enhanced component model documentation
- Complete API reference documentation
- Developer guides and tutorials

### Changed
- Migrated from Python 3.12+ to Python 3.11+ for broader compatibility
- Updated all type hints to use modern Python syntax
- Improved error messages and diagnostics

### Fixed
- Component discovery issues in certain environments
- State management race conditions
- Schema validation edge cases

## [1.0.0] - 2024-12-15

### Added
- 🎉 **Initial Production Release**
- Complete Terraform Plugin Protocol v6 implementation
- Component-based architecture with decorators
- Type-safe schema system using attrs
- Full CRUD lifecycle for resources
- Data source support for read-only operations
- Provider functions for transformations
- Ephemeral resources for short-lived connections
- State encryption for sensitive data
- Comprehensive CLI with multiple commands
- Built-in testing framework
- Hub-based component discovery
- Async/await support throughout
- Structured logging with provide.foundation
- Performance optimizations
- Docker support

### Core Components

#### Providers (`@register_provider`)
- Provider configuration management
- Authentication handling
- Shared client initialization
- Metadata management

#### Resources (`@register_resource`)
- Full CRUD operations (create, read, update, delete)
- State management
- Import support
- Move support
- Private state encryption

#### Data Sources (`@register_data_source`)
- Read-only data fetching
- Computed attributes
- Filtering and queries

#### Functions (`@register_function`)
- Pure transformations
- Type-safe input/output
- Async execution

#### Ephemeral Resources (`@register_ephemeral_resource`)
- Open/renew/close lifecycle
- Connection management
- Lease renewal

### Protocol Features
- GetProviderSchema
- ValidateProviderConfig
- ConfigureProvider
- ValidateResourceConfig
- ValidateDataResourceConfig
- UpgradeResourceState
- ReadResource
- PlanResourceChange
- ApplyResourceChange
- ImportResourceState
- MoveResourceState
- ReadDataSource
- GetFunctions
- CallFunction
- OpenEphemeralResource
- RenewEphemeralResource
- CloseEphemeralResource
- StopProvider

### CLI Commands
- `pyvider --version` - Show version
- `pyvider components list` - List discovered components
- `pyvider provide` - Start provider server
- `pyvider config validate` - Validate configuration
- `pyvider schema generate` - Generate schema
- `pyvider build` - Build provider binary

### Testing Support
- pytest integration
- Async test support
- Component test fixtures
- Mock providers
- Coverage reporting

## [0.9.0] - 2024-11-01 (Beta)

### Added
- Beta release with core functionality
- Basic resource lifecycle
- Initial protocol implementation
- Schema generation from attrs classes

### Changed
- Refactored component discovery
- Improved error handling

### Fixed
- Memory leaks in long-running providers
- Schema validation bugs

## [0.5.0] - 2024-09-15 (Alpha)

### Added
- Alpha release for testing
- Basic provider framework
- Resource decorators
- Simple CLI

### Known Issues
- Limited protocol support
- No state encryption
- Missing ephemeral resources

## [0.1.0] - 2024-07-01 (Pre-Alpha)

### Added
- Initial proof of concept
- Basic gRPC server
- Resource registration
- Minimal schema support

---

## Version History Summary

| Version | Date | Status | Highlights |
|---------|------|--------|------------|
| 1.0.0 | 2024-12-15 | **Stable** | Production release with full Protocol v6 |
| 0.9.0 | 2024-11-01 | Beta | Feature complete, testing phase |
| 0.5.0 | 2024-09-15 | Alpha | Public testing release |
| 0.1.0 | 2024-07-01 | Pre-Alpha | Initial concept |

## Upgrade Guide

### From 0.9.x to 1.0.0

#### Breaking Changes

1. **Decorator API Changes**:
```python
# Old (0.9.x)
from pyvider import provider, resource

@provider("mycloud")
class MyProvider: ...

# New (1.0.0)
from pyvider.providers import register_provider

@register_provider("mycloud")
class MyProvider(BaseProvider): ...
```

2. **Base Class Requirements**:
```python
# All components must inherit from base classes
class MyResource(BaseResource): ...
class MyDataSource(BaseDataSource): ...
class MyFunction(BaseFunction): ...
```

3. **Schema Definition**:
```python
# Old (0.9.x)
schema = {
    "name": {"type": "string", "required": True}
}

# New (1.0.0)
@attrs.define
class Config:
    name: str = Attribute(required=True)
```

#### Migration Steps

1. Update imports to use new module paths
2. Inherit from appropriate base classes
3. Convert schema dictionaries to attrs classes
4. Update decorator usage
5. Test thoroughly with new version

### From 0.5.x to 1.0.0

Complete rewrite recommended. The API has changed significantly and is not backward compatible.

## Deprecation Policy

- Features marked as deprecated will be maintained for at least 2 minor versions
- Deprecation warnings will be logged when deprecated features are used
- Migration guides will be provided for all deprecations

## Support Policy

| Version | Support Status | End of Support |
|---------|---------------|----------------|
| 1.0.x | **Active** | Current |
| 0.9.x | Security only | 2025-03-01 |
| 0.5.x | End of life | 2024-12-31 |
| 0.1.x | End of life | 2024-10-01 |

## Reporting Issues

Please report issues on our [GitHub Issue Tracker](https://github.com/provide-io/pyvider/issues).

Include:
- Pyvider version
- Python version
- Operating system
- Minimal reproduction code
- Error messages and stack traces

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

[Unreleased]: https://github.com/provide-io/pyvider/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/provide-io/pyvider/compare/v0.9.0...v1.0.0
[0.9.0]: https://github.com/provide-io/pyvider/compare/v0.5.0...v0.9.0
[0.5.0]: https://github.com/provide-io/pyvider/compare/v0.1.0...v0.5.0
[0.1.0]: https://github.com/provide-io/pyvider/releases/tag/v0.1.0