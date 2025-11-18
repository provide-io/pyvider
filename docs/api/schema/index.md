# Schema API

Type-safe schema definition system for Terraform resources, data sources, and providers.

## Overview

The schema system provides Python-first schema definition with full Terraform compatibility.

### Key Components

- **Schema Types** (`PvsSchema`, `PvsObjectType`) - Container types
- **Attributes** (`PvsAttribute`) - Schema fields with types and modifiers
- **Blocks** (`PvsNestedBlock`) - Nested configuration blocks
- **Validators** - Built-in and custom validation
- **Factory Functions** - Schema builders (s_provider, s_resource, etc.)

### Type System

Maps Python types to Terraform types:
- `str` → String
- `int` / `float` → Number
- `bool` → Boolean
- `list` → List
- `dict` → Map/Object
- `set` → Set

### Modifiers

Attributes support modifiers:
- `required=True` - Must be provided
- `optional=True` - May be omitted
- `computed=True` - Provider-calculated
- `sensitive=True` - Redacted in logs
- `default=value` - Default value

## Module Reference
