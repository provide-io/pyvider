# Welcome to Pyvider Documentation

!!! warning "Alpha Software - v0.0.x"
    Pyvider is currently in **alpha** (v0.0.1000). While functional and actively developed, please note:

    - **APIs may change** before the 1.0 release
    - **Some documented features** may not be fully implemented yet
    - **Best suited** for internal tooling, experimentation, and early adopters
    - See [Roadmap](development/roadmap/) for feature status and future plans

    For production use, test thoroughly and be prepared for potential breaking changes in future releases.

**Pyvider** is a revolutionary Python framework that enables you to build production-ready Terraform providers using pure Python. By combining Python's elegance with Terraform's infrastructure management capabilities, Pyvider opens up provider development to the vast Python ecosystem while maintaining full compatibility with Terraform's Plugin Protocol v6.

## Quick Start

<div class="feature-grid">
  <div class="feature-card">
    <h3>📦 Install</h3>
    <p>Get Pyvider installed in minutes</p>
    <p><a href="getting-started/installation/">Install Pyvider →</a></p>
  </div>
  <div class="feature-card">
    <h3>🚀 5-Minute Tutorial</h3>
    <p>Build your first provider</p>
    <p><a href="getting-started/quick-start/">Quick Start Guide →</a></p>
  </div>
  <div class="feature-card">
    <h3>📚 100+ Examples</h3>
    <p>Working code you can use today</p>
    <p><a href="https://github.com/provide-io/pyvider-components">Browse Components →</a></p>
  </div>
  <div class="feature-card">
    <h3>🤔 Why Pyvider?</h3>
    <p>Understand the vision</p>
    <p><a href="explanation/design-philosophy/">Design Philosophy →</a></p>
  </div>
</div>

## Documentation Structure

### 🚀 [Getting Started](getting-started/installation/)
- [Installation](getting-started/installation/) - Set up Pyvider
- [Quick Start](getting-started/quick-start/) - Build your first provider in 5 minutes
- [Pyvider Components](https://github.com/provide-io/pyvider-components) - 100+ working examples

### 📖 [Developer Guides](guides/building-components/creating-providers/)
Build production-ready providers:
- [Creating Providers](guides/building-components/creating-providers/) - Provider configuration
- [Creating Resources](guides/building-components/creating-resources/) - CRUD operations
- [Creating Data Sources](guides/building-components/creating-data-sources/) - Read-only data
- [Creating Functions](guides/building-components/creating-functions/) - Transformations
- [Testing Providers](guides/development/testing-providers/) - Testing strategies
- [Best Practices](guides/production/best-practices/) - Production patterns

### 🏛️ [Core Concepts](explanation/architecture/)
Understand Pyvider's foundation:
- [Architecture](explanation/architecture/) - System design and data flow
- [Design Philosophy](explanation/design-philosophy/) - Vision and principles
- [Component Model](explanation/component-model/) - Hub-based discovery
- [Schema System](explanation/schema-system/) - Type-safe data modeling

### 📦 [Schema System](schema/overview/)
- [Overview](schema/overview/) - Schema introduction
- [Types](schema/types/) - Available schema types
- [Attributes](schema/attributes/) - Attribute definitions
- [Blocks](schema/blocks/) - Nested blocks
- [Validators](schema/validators/) - Input validation

### 📘 [API Reference](api/index/)
- [Schema API](api/schema/index/) - Attributes, blocks, and validation
- [CLI Commands](api/cli/) - Command-line interface
- [Common Types](api/common/) - Type system reference

### 🤝 [Contributing](contributing/guidelines/)
- [Contribution Guidelines](contributing/guidelines/) - How to contribute
- [Code of Conduct](contributing/code-of-conduct/) - Community standards

### 🔮 [Roadmap](development/roadmap/)
- [Development Roadmap](development/roadmap/) - Future features and plans

## Part of the provide.io Ecosystem

This project is part of a larger ecosystem of tools for Python and Terraform development.

**[View Ecosystem Overview →](https://docs.provide.io/provide-foundation/ecosystem/)**

Understand how provide-foundation, pyvider, flavorpack, and other projects work together.

## Prerequisites

- **Python 3.11+** installed
- Basic understanding of **Terraform** concepts
- Familiarity with **Python** type hints and **attrs** (helpful but not required)

## 📦 Ready-to-Use Components

The **[pyvider-components](https://github.com/provide-io/pyvider-components)** repository provides 100+ production-ready components:

- **Resources**: file_content, local_directory, timed_token
- **Data Sources**: env_variables, file_info, http_api, lens_jq
- **Functions**: String manipulation, numeric operations, JQ transformations

Install with: `pip install pyvider-components`

## 💬 Community & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/provide-io/pyvider/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/provide-io/pyvider/discussions)

## 📈 Project Status

- **Version**: 0.0.1000 (Alpha)
- **Protocol**: Terraform Plugin Protocol v6
- **Python**: 3.11+
- **License**: Apache 2.0
- **Status**: Alpha - Under Active Development

---

<p align="center">
  Made with ❤️ by the team at <a href="https://provide.io">Provide</a>
</p>
