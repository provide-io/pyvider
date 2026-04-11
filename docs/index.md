---
hide:
  - navigation
---

# Welcome to Pyvider Documentation

Build Terraform providers in Python — full Protocol v6, decorator-based API, async-first.

!!! tip "Current Status"
    Pyvider is in active development. See the announcement banner above for current version status.

**Pyvider** is a Python framework that enables you to build Terraform providers using pure Python. By combining Python's expressiveness with Terraform's infrastructure management capabilities, Pyvider makes provider development accessible to the Python ecosystem while maintaining full compatibility with Terraform's Plugin Protocol v6.

## Quick Start

<div class="feature-grid">
  <a class="feature-card" href="getting-started/installation/">
    <h3>📦 Install</h3>
    <p>Get Pyvider installed in minutes</p>
    <span class="card-link">Install Pyvider →</span>
  </a>
  <a class="feature-card" href="getting-started/quick-start/">
    <h3>🚀 5-Minute Tutorial</h3>
    <p>Build your first provider</p>
    <span class="card-link">Quick Start Guide →</span>
  </a>
  <a class="feature-card" href="https://github.com/provide-io/pyvider-components">
    <h3>📚 Components</h3>
    <p>Working code you can use today</p>
    <span class="card-link">Browse Components →</span>
  </a>
  <a class="feature-card" href="explanation/design-philosophy/">
    <h3>🤔 Why Pyvider?</h3>
    <p>Understand the vision</p>
    <span class="card-link">Design Philosophy →</span>
  </a>
</div>

## Documentation Structure

### 🚀 [Getting Started](getting-started/installation.md)

- [Installation](getting-started/installation.md) - Set up Pyvider
- [Quick Start](getting-started/quick-start.md) - Build your first provider in 5 minutes
- [Pyvider Components](https://github.com/provide-io/pyvider-components) - Ready-to-use working examples

### 📖 [Developer Guides](guides/building-components/creating-providers.md)

Build production-focused providers:

- [Creating Providers](guides/building-components/creating-providers.md) - Provider configuration
- [Creating Resources](guides/building-components/creating-resources.md) - CRUD operations
- [Creating Data Sources](guides/building-components/creating-data-sources.md) - Read-only data
- [Creating Functions](guides/building-components/creating-functions.md) - Transformations
- [Testing Providers](guides/development/testing-providers.md) - Testing strategies
- [Best Practices](guides/production/best-practices.md) - Production patterns

### 🏛️ [Core Concepts](explanation/architecture.md)

Understand Pyvider's foundation:

- [Architecture](explanation/architecture.md) - System design and data flow
- [Design Philosophy](explanation/design-philosophy.md) - Vision and principles
- [Component Model](explanation/component-model.md) - Hub-based discovery
- [Schema System](explanation/schema-system.md) - Type-safe data modeling

### 📦 [Schema System](schema/overview.md)

- [Overview](schema/overview.md) - Schema introduction
- [Types](schema/types.md) - Available schema types
- [Attributes](schema/attributes.md) - Attribute definitions
- [Blocks](schema/blocks.md) - Nested blocks
- [Validators](schema/validators.md) - Input validation

### 📘 [API Reference](api/index.md)

- [Schema API](api/schema/index.md) - Attributes, blocks, and validation
- [CLI Commands](api/cli.md) - Command-line interface
- [Common Types](api/common.md) - Type system reference

### 🤝 [Contributing](contributing/guidelines.md)

- [Contribution Guidelines](contributing/guidelines.md) - How to contribute
- [Code of Conduct](contributing/code-of-conduct.md) - Community standards

## Prerequisites

- **Python 3.11+** installed
- Basic understanding of **Terraform** concepts
- Familiarity with **Python** type hints and **attrs** (helpful but not required)

## 📦 Ready-to-Use Components

The **[pyvider-components](https://github.com/provide-io/pyvider-components)** repository provides production-focused components:

- **Resources**: file_content, local_directory, timed_token
- **Data Sources**: env_variables, file_info, http_api, lens_jq
- **Functions**: String manipulation, numeric operations, JQ transformations

Install with: `uv add pyvider-components`

## 💬 Community & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/provide-io/pyvider/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/provide-io/pyvider/discussions)

## 📈 Project Status

- **Version**: 0.3.0 (Pre-release)
- **Protocol**: Terraform Plugin Protocol v6
- **Python**: 3.11+
- **License**: Apache 2.0
- **Status**: Alpha - Under Active Development

______________________________________________________________________
