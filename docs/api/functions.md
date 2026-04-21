# Functions API

Base classes and utilities for creating Terraform provider functions.

## Overview

Functions in Pyvider allow providers to expose callable logic for data transformation and computation within Terraform configurations.

### Key Components

- **`BaseFunction`** - Base class for all functions
- **`@register_function`** - Decorator for function registration
- **Function Adapters** - Type conversion and validation
- **Parameter Handling** - Type-safe parameter processing

### Usage

Functions implement a `call()` method that:
- Accepts typed parameters
- Performs pure computation (no side effects)
- Returns typed results
- Can be called from Terraform expressions

### Example Use Cases

- Password generation
- String manipulation
- Data transformation
- Hash computation
- Encoding/decoding

## Module Reference
