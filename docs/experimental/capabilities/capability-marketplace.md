# Capability Marketplace

> **Note**: The capability marketplace is planned for future development.

The Pyvider Capability Marketplace will be a central hub for discovering and sharing reusable capabilities across the Pyvider community.

## Planned Features

### Discovery
- Browse capabilities by category (authentication, caching, logging, data transformation)
- Search by functionality and keywords
- View usage examples and documentation

### Distribution
- Publish capabilities as PyPI packages
- Version management and compatibility tracking
- Community ratings and reviews

### Integration
- One-command installation via pip
- Automatic registration with Pyvider
- Dependency resolution

## Current Alternative: pyvider-components

While the capability marketplace is in development, check out the [pyvider-components repository](https://github.com/provide-io/pyvider-components) for a collection of ready-to-use components:

### Available Components

**Resources:**
- `file_content` - Manage file contents with atomic writes
- `local_directory` - Directory creation and permission management
- `timed_token` - Time-limited token generation
- And more...

**Data Sources:**
- `env_variables` - Read environment variables
- `file_info` - Get file metadata
- `http_api` - Fetch data from HTTP APIs
- `lens_jq` - Transform JSON with jq queries
- And more...

**Functions:**
- String manipulation (upper, lower, format, etc.)
- Numeric operations (add, subtract, multiply, etc.)
- List operations (join, split, etc.)
- JQ transformations
- And more...

## Using pyvider-components

```bash
# Install the components package
pip install pyvider-components

# Components are automatically discovered
# Use them in your Terraform configurations
```

See the [pyvider-components documentation](https://github.com/provide-io/pyvider-components/tree/main/docs) for detailed usage examples.

## Contributing

Interested in creating capabilities? See:
- [Creating Capabilities](creating-capabilities.md)
- [Bundling Components](bundling-components.md)
- [Contributing Guidelines](../../contributing/guidelines.md)

## Stay Updated

- Watch the [Pyvider roadmap](../../development/roadmap.md) for marketplace updates
- Join discussions on [GitHub](https://github.com/provide-io/pyvider/discussions)
- Follow announcements for marketplace launch
