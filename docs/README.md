# Pyvider Documentation

This directory contains all documentation for Pyvider, the Python framework for building Terraform providers.

## 📚 Documentation Structure

```
docs/
├── getting-started/       # New user guides
│   ├── what-is-pyvider.md
│   ├── installation.md
│   └── quick-start.md
│
├── core-concepts/         # Foundational concepts
│   ├── architecture.md
│   ├── component-model.md
│   └── schema-system.md
│
├── guides/                # How-to guides
│   ├── Developer Guides:
│   │   ├── creating-providers.md
│   │   ├── creating-resources.md
│   │   ├── creating-data-sources.md
│   │   ├── creating-functions.md
│   │   ├── testing.md
│   │   ├── best-practices.md
│   │   ├── provider-lifecycle.md
│   │   ├── error-handling.md
│   │   ├── logging.md
│   │   └── debugging.md
│   └── User Guides:
│       ├── configuration.md
│       ├── managing-resources.md
│       ├── using-data-sources.md
│       ├── using-functions.md
│       ├── advanced-examples.md
│       └── advanced-usage.md
│
├── tutorials/             # Step-by-step tutorials
│   ├── first-provider.md
│   ├── jq-components/     # JQ function/data source tutorial
│   ├── http-api/          # HTTP API provider tutorial
│   └── file-content/      # File content resource tutorial
│
├── schema/                # Schema system docs
│   ├── overview.md
│   ├── types.md
│   ├── attributes.md
│   ├── blocks.md
│   ├── validators.md
│   ├── computed-attributes.md
│   ├── sensitive-data.md
│   ├── schema-by-example.md
│   ├── common-patterns.md
│   └── best-practices.md
│
├── capabilities/          # Capabilities system
│   ├── overview.md
│   ├── using-capabilities.md
│   ├── creating-capabilities.md
│   ├── bundling-components.md
│   ├── capability-lifecycle.md
│   ├── capability-composition.md
│   └── capability-marketplace.md
│
├── api-reference/         # API documentation
│   ├── decorators.md      # @register_* decorators
│   ├── testing.md         # Testing utilities
│   ├── cli.md             # CLI reference (auto-generated)
│   ├── schema.md          # Schema API (auto-generated)
│   └── types.md           # Type system (auto-generated)
│
├── contributing/          # Contribution guides
│   ├── guidelines.md
│   └── code-of-conduct.md
│
└── development/           # Internal documentation
    └── roadmap.md         # Planned features
```

## 🚀 Quick Start

### Viewing Documentation Locally

```bash
# Install dependencies (if not already installed)
uv pip install mkdocs mkdocs-material mkdocstrings[python]

# Serve documentation locally (with auto-reload)
mkdocs serve

# Open http://127.0.0.1:8003 in your browser
```

### Building Documentation

```bash
# Build static site
mkdocs build

# Build in strict mode (fails on warnings/broken links)
mkdocs build --strict

# Check for broken links
python scripts/check_doc_links.py
```

## ✍️ Contributing to Documentation

### File Naming Conventions

- Use lowercase with hyphens: `creating-providers.md`
- Use descriptive names: `provider-lifecycle.md` not `08-lifecycle.md`
- **NO number prefixes**: ✅ `overview.md` ❌ `01-overview.md`

### Adding New Documentation

1. **Create your markdown file** in the appropriate directory
2. **Update `mkdocs.yml`** navigation to include your new page
3. **Follow the style guide**:
   - Use clear, concise headings
   - Include code examples
   - Add cross-references to related docs
4. **Test your changes**:
   ```bash
   python scripts/check_doc_links.py  # Check for broken links
   mkdocs build --strict               # Build in strict mode
   mkdocs serve                        # Preview locally
   ```
5. **Commit** and create a pull request

### Documentation Style Guide

#### Headings

```markdown
# Page Title (H1 - one per page)

## Major Section (H2)

### Subsection (H3)

#### Minor Section (H4)
```

#### Code Blocks

Use fenced code blocks with language specification:

````markdown
```python
from pyvider.providers import register_provider

@register_provider("mycloud")
class MyCloudProvider:
    pass
```
````

#### Links

- **Internal links**: Use relative paths
  ```markdown
  [Creating Providers](../guides/creating-providers.md)
  ```
- **External links**: Use full URLs
  ```markdown
  [Terraform](https://www.terraform.io/)
  ```

#### Admonitions

MkDocs Material supports admonitions:

```markdown
!!! note
    This is a note.

!!! warning
    This is a warning.

!!! tip
    This is a tip.
```

## 🔧 Auto-Generated Documentation

Some API documentation is auto-generated from Python docstrings using mkdocstrings.

### Files with Auto-Generation

These files use the `:::` directive to include generated docs:

- `api-reference/cli.md`
- `api-reference/schema.md`
- `api/` directory files

**Example:**

```markdown
# CLI

::: pyvider.cli
    options:
      show_source: true
      show_root_heading: true
```

This automatically generates API documentation from the `pyvider.cli` module.

## 🔍 Link Checking

We use a custom Python script to validate all internal links:

```bash
# Run link checker
python scripts/check_doc_links.py

# Output:
# ✅ All documentation links are valid!
# OR
# ❌ Found broken links:
#   file.md:42: Broken link to 'missing.md'
```

The link checker:
- Validates all `[text](url)` markdown links
- Checks file existence
- Validates anchor links (heading references)
- Runs automatically in CI/CD

## 🤖 Continuous Integration

Documentation is automatically validated on every pull request:

- ✅ Link checking (`python scripts/check_doc_links.py`)
- ✅ MkDocs build (`mkdocs build --strict`)
- ✅ Markdown linting (optional)
- ✅ Auto-deploy to GitHub Pages on main branch

See `.github/workflows/docs-check.yml` for details.

## 📖 Documentation Philosophy

### What Makes Good Documentation

1. **Clear and Concise**: Get to the point quickly
2. **Example-Driven**: Show, don't just tell
3. **Well-Organized**: Easy to find what you need
4. **Up-to-Date**: Reflects current APIs and practices
5. **Cross-Referenced**: Links to related topics

### Documentation Types

We follow the [Diátaxis framework](https://diataxis.fr/):

- **Tutorials** (`tutorials/`): Learning-oriented, step-by-step guides
- **How-To Guides** (`guides/`): Goal-oriented, problem-solving guides
- **Reference** (`api-reference/`): Information-oriented, technical descriptions
- **Explanation** (`core-concepts/`): Understanding-oriented, background knowledge

## 🆘 Getting Help

- **Documentation issues**: [Open an issue](https://github.com/provide-io/pyvider/issues)
- **Questions**: [GitHub Discussions](https://github.com/provide-io/pyvider/discussions)
- **Community**: [Discord](https://discord.gg/pyvider)

## 📝 Changelog

### Recent Updates

- **2025-10-24**: Complete documentation reorganization
  - Removed all numbered file prefixes
  - Created clean, named folder structure
  - Added decorators and testing API reference
  - Implemented automated link checking
  - Set up GitHub Actions CI/CD

---

**Thank you for contributing to Pyvider documentation!** 🎉
