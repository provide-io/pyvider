# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Commands

### Task Runner (wrknv)
This project uses `wrknv` for task automation. All tasks can be run with `we run <task>`.

```bash
we tasks             # List all available tasks
we run test          # Run tests
we run test.coverage # Run with coverage report
we run test.parallel # Run tests in parallel
we run lint          # Check code quality
we run lint.fix      # Auto-fix linting issues
we run format        # Format code
we run format.check  # Check formatting without changes
we run typecheck     # Run type checker
we run build         # Build distribution
```

For complete task documentation, see [wrknv.toml](wrknv.toml) or run `we tasks`.

### Environment Setup
```bash
# Install dependencies
uv sync
```

### Pyvider CLI
```bash
# Core commands
pyvider --help                             # Show help
pyvider install                            # Install provider for Terraform
pyvider provide                            # Start provider server (default)

# Component management
pyvider components list                    # List all components
pyvider components show resource <name>    # Show component schema
pyvider components diagnostics             # Show discovery diagnostics

# Configuration & debugging
pyvider config show                        # Display current configuration
pyvider launch-context                     # Show how pyvider was launched
```

## Key Patterns

### Component Model
Pyvider uses a hub-based discovery system where components self-register via decorators:
- `@register_provider` - Provider configuration
- `@register_resource` - CRUD resources
- `@register_data_source` - Read-only data
- `@register_function` - Callable functions
- `@register_ephemeral_resource` - Short-lived resources

### Project Structure
- `protocols/tfprotov6/` - Terraform Plugin Protocol v6 implementation
- `schema/` - Type-safe data modeling
- `conversion/` - Data transformation between Terraform and Python
- `capabilities/` - Reusable, composable components

For detailed architecture documentation, see `docs/core-concepts/`.

### Development Patterns
- Components must use decorators to register with the hub
- Schema definitions use attrs-based models with type annotations
- Testing: Unit tests, integration tests, property-based testing (Hypothesis)
- TDD test files prefixed with `test_tdd_`

## Important Notes

- **Python 3.11+ required**
- Uses `uv` for fast dependency management
- Protocol buffer files (`*pb2*.py`) are auto-generated - do not edit directly
- Related projects: TofuSoup (testing), Flavor (packaging)

## Documentation

- Full documentation available in `docs/` directory
- Build docs: `mkdocs build`
- Serve locally: `mkdocs serve`
- Check links: `python scripts/check_doc_links.py`

## After Changes

Always run `we run test` to verify your changes work correctly.
