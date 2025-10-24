# 📦 Installation Guide

This guide covers everything you need to install Pyvider and set up your development environment for building Terraform providers in Python.

## 🚦 System Requirements

### Minimum Requirements
- **Python**: 3.11 or higher
- **Operating System**: Linux, macOS, or Windows
- **Memory**: 2GB RAM minimum
- **Disk Space**: 500MB for Pyvider and dependencies

### Recommended Setup
- **Python**: 3.11+ (latest stable version)
- **Package Manager**: [uv](https://github.com/astral-sh/uv) for fast dependency management
- **IDE**: VS Code or PyCharm with Python extensions
- **Memory**: 4GB+ RAM for comfortable development

## 🎯 Installation Methods

### Method 1: Using pip (Simple)

The quickest way to get started with Pyvider:

```bash
# Basic installation
pip install pyvider

# With all optional dependencies
pip install pyvider[all]

# For development (includes testing tools)
pip install pyvider[dev]
```

### Method 2: Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a blazing-fast Python package manager that we recommend for Pyvider development:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a new project
uv init my-provider
cd my-provider

# Add Pyvider as a dependency
uv add pyvider

# For development setup
uv add --dev pytest pytest-asyncio pytest-cov mypy ruff
```

### Method 3: Using Poetry

If you prefer Poetry for dependency management:

```bash
# Create a new project
poetry new my-provider
cd my-provider

# Add Pyvider
poetry add pyvider

# Add development dependencies
poetry add --group dev pytest pytest-asyncio pytest-cov mypy ruff
```

### Method 4: From Source (Advanced)

For contributing or testing the latest features:

```bash
# Clone the repository
git clone https://github.com/provide-io/pyvider.git
cd pyvider

# Set up development environment
uv sync  # On Windows: .\env.ps1

# Install in editable mode
pip install -e .

# Run tests to verify installation
pytest
```

## 🔧 Environment Setup

### 1. Virtual Environment (Recommended)

Always use a virtual environment to avoid dependency conflicts:

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install Pyvider
pip install pyvider
```

### 2. Development Environment Setup

For provider development, set up your project structure:

```bash
# Create project structure
mkdir -p my_provider/{provider,resources,data_sources,functions,tests}
touch my_provider/__init__.py
touch my_provider/provider/__init__.py
touch my_provider/resources/__init__.py
touch my_provider/data_sources/__init__.py
touch my_provider/functions/__init__.py
```

### 3. Environment Variables

Configure optional environment variables:

```bash
# Enable debug logging
export PYVIDER_LOG_LEVEL=DEBUG

# Set custom plugin directory
export PYVIDER_PLUGIN_DIR=~/.terraform.d/plugins

# Enable performance profiling
export PYVIDER_PROFILE=1
```

## 📋 Dependency Configuration

### pyproject.toml Example

Here's a complete `pyproject.toml` for a Pyvider provider project:

```toml
[project]
name = "my-terraform-provider"
version = "0.1.0"
description = "A Terraform provider built with Pyvider"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "pyvider>=1.0.0",
    "httpx>=0.24.0",  # For HTTP APIs
    "pydantic>=2.0.0",  # For validation
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
    "black>=23.0.0",
]

[build-system]
requires = ["setuptools>=65", "wheel"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "-v --cov=my_provider --cov-report=term-missing"

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "I", "N", "W", "B", "UP"]
ignore = ["E501"]  # Line too long

[tool.black]
line-length = 100
target-version = ["py311"]
```

## ✅ Verification

After installation, verify everything is working:

### 1. Check Pyvider Installation

```bash
# Verify Pyvider is installed
python -c "import pyvider; print(pyvider.__version__)"

# Check CLI availability
pyvider --version

# List available commands
pyvider --help
```

### 2. Run Component Discovery Test

Create a simple test file to verify component discovery:

```python
# test_installation.py
from pyvider import provider, resource

@provider
class TestProvider:
    """Test provider to verify installation"""
    metadata = {"name": "test", "version": "0.1.0"}

@resource
class TestResource:
    """Test resource"""
    pass

if __name__ == "__main__":
    from pyvider.hub import ComponentHub
    hub = ComponentHub()
    print(f"Found {len(hub.providers)} provider(s)")
    print(f"Found {len(hub.resources)} resource(s)")
```

Run it:

```bash
python test_installation.py
# Should output:
# Found 1 provider(s)
# Found 1 resource(s)
```

### 3. Test CLI Commands

```bash
# List discovered components
pyvider components list

# Validate configuration
pyvider config validate

# Show system information
pyvider info
```

## 🔌 IDE Setup

### Visual Studio Code

Install recommended extensions:

```json
// .vscode/extensions.json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff",
        "ms-python.mypy-type-checker",
        "littlefoxteam.vscode-python-test-adapter"
    ]
}
```

Configure settings:

```json
// .vscode/settings.json
{
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

### PyCharm

1. Open **Settings** → **Project** → **Python Interpreter**
2. Add Pyvider to your project interpreter
3. Enable **pytest** as the test runner
4. Configure **mypy** for type checking
5. Set up **ruff** for linting

## 🐳 Docker Setup (Optional)

For containerized development:

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Pyvider
RUN pip install --no-cache-dir pyvider[all]

# Copy your provider code
COPY . .

# Install provider dependencies
RUN pip install --no-cache-dir -e .

# Run provider
CMD ["pyvider", "provide"]
```

Build and run:

```bash
docker build -t my-provider .
docker run -p 50051:50051 my-provider
```

## 🚨 Common Installation Issues

### Issue: Python Version Too Old

```bash
ERROR: pyvider requires Python 3.11 or higher
```

**Solution**: Upgrade Python or use pyenv to manage versions:

```bash
# Install pyenv
curl https://pyenv.run | bash

# Install Python 3.11
pyenv install 3.11.7
pyenv global 3.11.7
```

### Issue: Missing Build Tools

```bash
ERROR: Microsoft Visual C++ 14.0 is required (Windows)
ERROR: error: Microsoft Visual C++ 14.0 or greater is required
```

**Solution**: Install build tools:
- **Windows**: Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
- **macOS**: Install Xcode Command Line Tools: `xcode-select --install`
- **Linux**: Install build-essential: `sudo apt-get install build-essential`

### Issue: Permission Denied

```bash
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Solution**: Use a virtual environment or install with `--user`:

```bash
pip install --user pyvider
```

### Issue: Conflicting Dependencies

```bash
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```

**Solution**: Use uv or create a fresh virtual environment:

```bash
# With uv
uv venv
uv pip install pyvider

# With standard venv
python -m venv fresh_env
source fresh_env/bin/activate
pip install pyvider
```

## 🔄 Upgrading Pyvider

Keep Pyvider up to date for the latest features and fixes:

```bash
# Using pip
pip install --upgrade pyvider

# Using uv
uv add --upgrade pyvider

# Using poetry
poetry update pyvider

# Check current version
pyvider --version
```

## 📚 Next Steps

Now that you have Pyvider installed:

1. **[Quick Start Guide](quick-start.md)** - Build your first provider in 5 minutes
2. **[Pyvider Components Examples](https://github.com/provide-io/pyvider-components)** - 100+ working examples
3. **[Architecture Overview](../core-concepts/architecture.md)** - Understand how Pyvider works
4. **[API Reference](../api/index.md)** - Explore the API documentation

## 💬 Getting Help

If you encounter issues during installation:

- Check the [Troubleshooting Guide](../troubleshooting.md)
- Search [GitHub Issues](https://github.com/provide-io/pyvider/issues)
- Ask in our [Discord Community](https://discord.gg/pyvider)
- Post on [Stack Overflow](https://stackoverflow.com/questions/tagged/pyvider) with tag `pyvider`

---

<p align="center">
  Ready to build? Continue to the <a href="quick-start.md">Quick Start Guide →</a>
</p>