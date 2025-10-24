# Conversion API

Bidirectional type conversion between Python objects and Terraform's type system (CTY).

## Overview

The conversion layer handles all data transformation between:
- **Python types** ↔ **CTY values** (Terraform's type system)
- **Protocol buffers** ↔ **Python objects**
- **Schema definitions** ↔ **Protocol schema**

### Key Components

- **Adapter** - High-level conversion interface
- **Marshaler** - Protocol buffer serialization
- **Schema Adapter** - Schema format conversion
- **CTY Integration** - Terraform type system support

### Conversion Features

- Type-safe conversions with validation
- Unknown value handling
- Null value support
- Complex nested structures
- Collection types (list, map, set)

### Usage

Most conversion is automatic, but utilities are available for:
- Custom type converters
- Complex data structures
- Direct CTY manipulation
- Protocol buffer handling

## Module Reference

::: pyvider.conversion
    options:
      show_source: true
      show_root_heading: true
      members_order: source
      show_if_no_docstring: false
      filters:
        - "!^_"
        - "^__init__$"
