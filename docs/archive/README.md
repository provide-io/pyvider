# Archived Documentation

⚠️ **This directory contains ARCHIVED documentation for features no longer under active development.**

## Why Archived?

These documents describe experimental capabilities that were explored during pyvider's development but are not part of the current roadmap. They are preserved for:

- Historical reference
- Potential future revival
- Understanding past design decisions
- Context for contributors

---

## Current Status

| Document | Reason for Archival | Alternative |
|----------|---------------------|-------------|
| **bundling-components.md** | Superseded by simplified approach | See [Capabilities Overview](../capabilities/overview.md) |
| **capability-composition.md** | Superseded by simplified approach | See [Capabilities Overview](../capabilities/overview.md) |
| **capability-lifecycle.md** | Superseded by simplified approach | See [Capabilities Overview](../capabilities/overview.md) |
| **capability-marketplace.md** | Moved to future roadmap | See [Roadmap](../development/roadmap.md) |
| **creating-capabilities.md** | Superseded by simplified approach | See [Capabilities Overview](../capabilities/overview.md) |
| **using-capabilities.md** | Superseded by simplified approach | See [Capabilities Overview](../capabilities/overview.md) |

### Timeline

- **Deprecated:** October 24, 2025
- **Reason:** Created confusion about what features were actually available
- **Resolution:** Simplified to single overview page focusing on working alternatives

---

## Do Not Use for Current Development

⛔ **These documents are outdated and should not be used for current development.**

For current pyvider capabilities and patterns, see:

- **[Capabilities Overview](../capabilities/overview.md)** - Current experimental capabilities system
- **[Building Components](../guides/building-components/)** - Current component development guides
- **[Best Practices](../guides/production/best-practices.md)** - Recommended code reuse patterns
- **[Roadmap](../development/roadmap.md)** - Future planned features

---

## Background: The Capabilities Experiment

The capabilities system was envisioned as a powerful composition mechanism for sharing provider logic. However, during development we discovered:

1. **Complexity:** The system became too complex for the value it provided
2. **Confusion:** Documentation promised features that weren't fully implemented
3. **Better Alternatives:** Python's inheritance and composition patterns work well
4. **Focus:** Simplified approach allows focus on core provider functionality

The current simplified approach in `capabilities/overview.md` provides:
- Clear explanation of what's experimental vs. available
- Working code reuse patterns (inheritance, composition)
- Roadmap for future capability enhancements
- No promises of unimplemented features

---

## Note to Contributors

If you're considering reviving capability features:

1. Review the archived documents to understand the original vision
2. Consider why they were archived (complexity, incomplete implementation)
3. Propose a simpler, incremental approach
4. Ensure any new features are fully implemented before documentation
5. Get community feedback before major capability system changes

---

**This content is preserved for historical purposes only.**
**Last archived:** October 30, 2025
**For current documentation, see:** [Pyvider Documentation](../index.md)
