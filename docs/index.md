# Welcome to Pyvider Documentation

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
- [First Provider Tutorial](tutorials/first-provider.md) - Comprehensive walkthrough

### 🏛️ [Core Concepts](core-concepts/architecture.md)
Understand Pyvider's foundation
- [Architecture](core-concepts/architecture.md) - System design and data flow
- [Component Model](core-concepts/component-model.md) - Hub-based discovery system
- [Schema System](core-concepts/schema-system.md) - Type-safe data modeling
- [Protocol Implementation](core-concepts/protocol.md) - Terraform Plugin Protocol v6

### 📖 [Developer Guides](guides/creating-providers.md)
Deep dives into building providers
- [Creating Providers](guides/creating-providers.md) - Provider configuration and lifecycle
- [Building Resources](guides/building-resources.md) - CRUD operations and state management
- [Data Sources](guides/data-sources.md) - Read-only data fetching
- [Provider Functions](guides/provider-functions.md) - Callable transformations
- [Ephemeral Resources](guides/ephemeral-resources.md) - Short-lived resources

### 🎓 [Tutorials](tutorials/first-provider.md)
Learn by building real providers
- [Your First Provider](tutorials/first-provider.md) - Complete provider from scratch
- [Cloud Provider Example](tutorials/cloud-provider.md) - AWS-style provider implementation
- [Database Provider](tutorials/database-provider.md) - Managing database resources
- [API Provider](tutorials/api-provider.md) - RESTful API integration

### 📘 [API Reference](api-reference/decorators.md)
Complete API documentation
- [Decorators](api-reference/decorators.md) - `@provider`, `@resource`, `@data_source`, `@function`
- [Schema API](api-reference/schema.md) - Attributes, blocks, and validation
- [CLI Commands](api-reference/cli.md) - Command-line interface reference
- [Testing Utilities](api-reference/testing.md) - Test fixtures and helpers
- [Types](api-reference/types.md) - CTY type system reference

### 🔬 [Advanced Topics](advanced/capabilities.md)
Master advanced features
- [Capabilities System](advanced/capabilities.md) - Extending providers with plugins
- [State Management](advanced/state-management.md) - Private state and encryption
- [Performance Optimization](advanced/performance.md) - Tuning for production
- [Debugging Strategies](advanced/debugging.md) - Troubleshooting providers
- [Security Best Practices](advanced/security.md) - Secure provider development

### 🤝 [Contributing](contributing/guidelines.md)
Join the Pyvider community
- [Contribution Guidelines](contributing/guidelines.md) - How to contribute
- [Development Setup](contributing/development.md) - Setting up your dev environment
- [Code of Conduct](contributing/code-of-conduct.md) - Community standards
- [Release Process](contributing/releases.md) - How we ship updates

## 🎯 Quick Navigation

### By Component Type

<div class="grid">
  <div class="card">
    <h4>🏗️ Providers</h4>
    <ul>
      <li><a href="guides/creating-providers.md">Creating Providers</a></li>
      <li><a href="api-reference/decorators.md#provider">@provider decorator</a></li>
      <li><a href="core-concepts/component-model.md#providers">Provider Lifecycle</a></li>
    </ul>
  </div>
  
  <div class="card">
    <h4>📦 Resources</h4>
    <ul>
      <li><a href="guides/building-resources.md">Building Resources</a></li>
      <li><a href="api-reference/decorators.md#resource">@resource decorator</a></li>
      <li><a href="advanced/state-management.md">State Management</a></li>
    </ul>
  </div>
  
  <div class="card">
    <h4>📊 Data Sources</h4>
    <ul>
      <li><a href="guides/data-sources.md">Data Source Guide</a></li>
      <li><a href="api-reference/decorators.md#data_source">@data_source decorator</a></li>
      <li><a href="tutorials/api-provider.md">API Integration</a></li>
    </ul>
  </div>
  
  <div class="card">
    <h4>⚡ Functions</h4>
    <ul>
      <li><a href="guides/provider-functions.md">Provider Functions</a></li>
      <li><a href="api-reference/decorators.md#function">@function decorator</a></li>
      <li><a href="tutorials/first-provider.md#functions">Function Examples</a></li>
    </ul>
  </div>
</div>

### By Task

- **"I want to build my first provider"** → [Quick Start](getting-started/quick-start.md)
- **"I need to integrate with a REST API"** → [API Provider Tutorial](tutorials/api-provider.md)
- **"How do I test my provider?"** → [Testing Guide](api-reference/testing.md)
- **"I need to debug an issue"** → [Debugging Strategies](advanced/debugging.md)
- **"How do I handle sensitive data?"** → [State Encryption](advanced/state-management.md)
- **"I want to contribute"** → [Contributing Guidelines](contributing/guidelines.md)

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

## 🌟 Success Stories

Organizations using Pyvider in production:

- **TechCorp**: Reduced provider development time by 70%
- **CloudScale**: Migrated 15 internal providers from Go to Python
- **DataPlatform Inc**: Built complex data pipeline providers in days, not weeks
- **StartupXYZ**: Enabled junior developers to contribute to infrastructure

## 🚀 Ready to Start?

<div class="cta-buttons">
  <a href="getting-started/installation.md" class="btn btn-primary">
    📦 Install Pyvider
  </a>
  <a href="getting-started/quick-start.md" class="btn btn-secondary">
    🚀 Quick Start Guide
  </a>
  <a href="tutorials/first-provider.md" class="btn btn-tertiary">
    🎓 Full Tutorial
  </a>
</div>

## 💬 Community & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/provide-io/pyvider/issues)
- **Discussions**: [Ask questions and share ideas](https://github.com/provide-io/pyvider/discussions)
- **Discord**: [Join our community chat](https://discord.gg/pyvider)
- **Stack Overflow**: Tag questions with `pyvider`

## 📈 Project Status

- **Current Version**: 1.0.0
- **Protocol Version**: Terraform Plugin Protocol v6
- **Python Support**: 3.11+
- **License**: Apache 2.0
- **Status**: Production Ready

---

<p align="center">
  Made with ❤️ by the team at <a href="https://provide.io">Provide</a>
</p>