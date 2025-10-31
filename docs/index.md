# Welcome to Pyvider Documentation

!!! warning "Alpha Software - v0.0.x"
    Pyvider is currently in **alpha** (v0.0.1000). While functional and actively developed, please note:

    - **APIs may change** before the 1.0 release
    - **Some documented features** may not be fully implemented yet
    - **Best suited** for internal tooling, experimentation, and early adopters
    - See [Roadmap](development/roadmap.md) for feature status and future plans

    For production use, test thoroughly and be prepared for potential breaking changes in future releases.

**Pyvider** is a revolutionary Python framework that enables you to build production-ready Terraform providers using pure Python. By combining Python's elegance with Terraform's infrastructure management capabilities, Pyvider opens up provider development to the vast Python ecosystem while maintaining full compatibility with Terraform's Plugin Protocol v6.

## 🎯 Our Mission

To democratize Terraform provider development by making it accessible to Python developers worldwide, enabling them to leverage their existing skills and Python's rich ecosystem to build robust infrastructure automation tools.

## ✨ Why Choose Pyvider?

### For Python Developers
- **🐍 Native Python Experience**: Write providers using familiar Python patterns and idioms
- **📚 Rich Ecosystem**: Access thousands of Python libraries for cloud APIs, databases, and services
- **🎓 Gentle Learning Curve**: No need to learn Go or complex protocol details
- **🧪 Familiar Testing**: Use pytest and your favorite Python testing tools

### For Infrastructure Teams
- **⚡ Rapid Development**: Build providers 3-5x faster than traditional Go implementations
- **🔒 Type Safety**: Leverage Python's type hints and attrs for robust, maintainable code
- **📊 Better Observability**: Built-in structured logging with provide.foundation
- **🚀 Production Ready**: Battle-tested with comprehensive error handling and state management

### For Organizations
- **💼 Lower Barrier to Entry**: Tap into your existing Python talent pool
- **🔄 Faster Iteration**: Quick prototyping and development cycles
- **🎯 Focused Development**: Decorators handle protocol complexity—teams focus on business logic
- **✅ Enterprise Ready**: Full Terraform compatibility with no compromises

## 📚 Documentation Overview

Our documentation is organized to help you quickly find what you need:

### 🚀 [Getting Started](getting-started/installation.md)
New to Pyvider? Start here!
- [Installation](getting-started/installation.md) - Set up Pyvider in your environment
- [Quick Start](getting-started/quick-start.md) - Build your first provider in 5 minutes
- [Pyvider Components](https://github.com/provide-io/pyvider-components) - 100+ working examples

### 🏛️ [Core Concepts](explanation/architecture.md)
Understand Pyvider's foundation
- [Architecture](explanation/architecture.md) - System design and data flow
- [Component Model](explanation/component-model.md) - Hub-based discovery system
- [Schema System](explanation/schema-system.md) - Type-safe data modeling

### 📖 [Developer Guides](guides/building-components/creating-providers.md)
Deep dives into building providers
- [Creating Providers](guides/building-components/creating-providers.md) - Provider configuration and lifecycle
- [Creating Resources](guides/building-components/creating-resources.md) - CRUD operations and state management
- [Creating Data Sources](guides/building-components/creating-data-sources.md) - Read-only data fetching
- [Creating Functions](guides/building-components/creating-functions.md) - Callable transformations
- [Testing Providers](guides/development/testing-providers.md) - Testing strategies and best practices
- [Best Practices](guides/production/best-practices.md) - Production-ready patterns
- [Error Handling](guides/development/error-handling.md) - Robust error management
- [Logging](guides/development/logging.md) - Structured logging with foundation
- [Debugging](guides/development/debugging.md) - Troubleshooting providers
- [Security Best Practices](guides/production/security-best-practices.md) - Secure provider development
- [Performance Optimization](guides/production/performance-optimization.md) - Building fast providers

### 🎓 [Examples & Tutorials](getting-started/quick-start.md)
Learn by building real providers
- [Quick Start Guide](getting-started/quick-start.md) - Build your first provider in 5 minutes
- [Building an HTTP API Provider](tutorials/intermediate-provider.md) - Intermediate tutorial
- [Pyvider Components Examples](https://github.com/provide-io/pyvider-components/tree/main/examples) - 100+ working examples
  - Resources: file_content, local_directory, timed_token
  - Data Sources: env_variables, http_api, lens_jq
  - Functions: String, numeric, and JQ operations

### 📘 [API Reference](api/index.md)
Complete API documentation
- [Schema API](api/schema/index.md) - Attributes, blocks, and validation
- [CLI Commands](api/cli.md) - Command-line interface reference
- [Common Types](api/common.md) - Type system reference

### 📦 [Schema System](schema/overview.md)
Type-safe data modeling
- [Overview](schema/overview.md) - Schema system introduction
- [Types](schema/types.md) - Available schema types
- [Attributes](schema/attributes.md) - Attribute definitions
- [Blocks](schema/blocks.md) - Nested blocks
- [Validators](schema/validators.md) - Input validation

### 🔌 [Capabilities (Experimental)](capabilities/overview.md)
Planned composition mechanism for code reuse
- [Overview](capabilities/overview.md) - Experimental capabilities system (not fully implemented)
- For working code reuse patterns, see [Best Practices](guides/production/best-practices.md)

### 🤝 [Contributing](contributing/guidelines.md)
Join the Pyvider community
- [Contribution Guidelines](contributing/guidelines.md) - How to contribute
- [Code of Conduct](contributing/code-of-conduct.md) - Community standards

### 🔮 [Development](development/roadmap.md)
Project roadmap and planned features
- [Roadmap](development/roadmap.md) - Future features and CLI commands

---

## Part of the provide.io Ecosystem

This project is part of a larger ecosystem of tools for Python and Terraform development.

**[View Ecosystem Overview →](https://docs.provide.io/provide-foundation/ecosystem/)**

Understand how provide-foundation, pyvider, flavorpack, and other projects work together.

---

## 🎯 Quick Navigation

### By Component Type

<div class="grid">
  <div class="card">
    <h4>🏗️ Providers</h4>
    <ul>
      <li><a href="guides/building-components/creating-providers.md">Creating Providers</a></li>
      <li><a href="guides/advanced/provider-lifecycle.md">Provider Lifecycle</a></li>
      <li><a href="explanation/component-model.md">Component Model</a></li>
    </ul>
  </div>

  <div class="card">
    <h4>📦 Resources</h4>
    <ul>
      <li><a href="guides/building-components/creating-resources.md">Creating Resources</a></li>
      <li><a href="guides/usage/managing-resources.md">Managing Resources</a></li>
      <li><a href="schema/overview.md">Schema System</a></li>
    </ul>
  </div>

  <div class="card">
    <h4>📊 Data Sources</h4>
    <ul>
      <li><a href="guides/building-components/creating-data-sources.md">Creating Data Sources</a></li>
      <li><a href="guides/usage/using-data-sources.md">Using Data Sources</a></li>
      <li><a href="https://github.com/provide-io/pyvider-components/tree/main/examples/data_source">API Integration Examples</a></li>
    </ul>
  </div>

  <div class="card">
    <h4>⚡ Functions</h4>
    <ul>
      <li><a href="guides/building-components/creating-functions.md">Creating Functions</a></li>
      <li><a href="guides/usage/using-functions.md">Using Functions</a></li>
      <li><a href="https://github.com/provide-io/pyvider-components/tree/main/examples/function">Function Examples</a></li>
    </ul>
  </div>
</div>

### By Task

- **"I want to build my first provider"** → [Quick Start](getting-started/quick-start.md)
- **"I need to integrate with a REST API"** → [HTTP API Examples](https://github.com/provide-io/pyvider-components/tree/main/examples/data_source/http_api)
- **"How do I test my provider?"** → [Testing Providers](guides/development/testing-providers.md)
- **"I need to debug an issue"** → [Debugging Guide](guides/development/debugging.md)
- **"How do I handle errors properly?"** → [Error Handling](guides/development/error-handling.md)
- **"I want to contribute"** → [Contributing Guidelines](contributing/guidelines.md)

## 📦 Ready-to-Use Components

Looking for pre-built components? Check out **[pyvider-components](https://github.com/provide-io/pyvider-components)**!

The pyvider-components repository provides a comprehensive collection of production-ready components:

- **Resources**: file_content, local_directory, timed_token, and more
- **Data Sources**: env_variables, file_info, http_api, lens_jq, and more
- **Functions**: String manipulation, numeric operations, JQ transformations, and more
- **100+ Working Examples**: Complete Terraform configurations with documentation
- **Installation**: `pip install pyvider-components`

Perfect for:
- Learning by example
- Quick prototyping
- Production use
- Understanding best practices

## 🚦 Prerequisites

Before diving into Pyvider, you should have:

- **Python 3.11+** installed
- Basic understanding of **Terraform** concepts (providers, resources, state)
- Familiarity with **Python** type hints and **attrs** (helpful but not required)
- **Git** for version control

## 🛠️ Development Tools

Pyvider integrates seamlessly with modern Python development tools:

- **uv** - Fast Python package manager (recommended)
- **pytest** - Testing framework
- **mypy/pyright** - Type checking
- **ruff** - Fast Python linter and formatter
- **provide.foundation** - Structured logging
- **flavor** - Provider packaging tool

## 📊 Comparison with Traditional Providers

| Feature | Pyvider (Python) | Traditional (Go) |
|---------|------------------|------------------|
| **Language** | Python 3.11+ | Go |
| **Learning Curve** | Gentle (Python devs) | Steep |
| **Development Speed** | Fast | Moderate |
| **Ecosystem** | Vast (PyPI) | Growing |
| **Type Safety** | Type hints + attrs | Static typing |
| **Testing** | pytest | go test |
| **Debugging** | Python debuggers | delve |
| **Performance** | Excellent | Excellent |
| **Protocol Support** | v6 (latest) | v5/v6 |

## 🌟 Early Adopters

Pyvider is currently in alpha and being used by early adopters for:

- **Internal tooling**: Building custom providers for company-specific infrastructure
- **Rapid prototyping**: Testing provider concepts before committing to Go implementations
- **Python-first teams**: Leveraging existing Python expertise for IaC
- **Educational projects**: Teaching Terraform provider development concepts

## 🚀 Ready to Start?

<div class="cta-buttons">
  <a href="getting-started/installation.md" class="btn btn-primary">
    📦 Install Pyvider
  </a>
  <a href="getting-started/quick-start.md" class="btn btn-secondary">
    🚀 Quick Start Guide
  </a>
  <a href="https://github.com/provide-io/pyvider-components" class="btn btn-tertiary">
    📚 Browse Examples
  </a>
</div>

## 💬 Community & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/provide-io/pyvider/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/provide-io/pyvider/discussions)

**Note**: As an alpha project, the best way to get support is through GitHub Issues and Discussions.

## 📈 Project Status

- **Current Version**: 0.0.1000 (Alpha)
- **Protocol Version**: Terraform Plugin Protocol v6
- **Python Support**: 3.11+
- **License**: Apache 2.0
- **Status**: Alpha - Under Active Development
- **Stability**: API may change before 1.0 release
- **Documentation**: Some features documented may not be fully implemented - check [Roadmap](development/roadmap.md)

---

<p align="center">
  Made with ❤️ by the team at <a href="https://provide.io">Provide</a>
</p>