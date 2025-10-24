# Component Hub

The component hub handles autodiscovery and registration of Pyvider components.

## Overview

The hub is responsible for:
- **Discovering components** via decorators
- **Validating** component definitions
- **Managing** component registry and lookup
- **Coordinating** component lifecycle

All components (providers, resources, data sources, functions) self-register with the hub using decorators.

## Module Reference

::: pyvider.hub
    options:
      show_source: true
      show_root_heading: true
      members_order: source
      show_if_no_docstring: false
      filters:
        - "!^_"
        - "^__init__$"
