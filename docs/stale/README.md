# Stale Documentation

This directory contains documentation that has been deprecated or removed from the main documentation but is preserved for historical reference.

## Contents

### `/experimental/capabilities/`

**Status:** Deprecated (2025-10-24)
**Reason:** These detailed experimental capability docs were removed in favor of a simpler, more focused approach in `docs/capabilities/overview.md`

The capabilities system is still in development, and these detailed guides described features that:
- Were not fully implemented yet
- Created confusion about what was actually available
- Are better covered by showing working alternatives (inheritance, composition)

**Files preserved:**
- `bundling-components.md` - Component bundling (now covered in capabilities/overview.md)
- `capability-composition.md` - Composition patterns (now covered in capabilities/overview.md)
- `capability-lifecycle.md` - Lifecycle hooks (now covered in capabilities/overview.md)
- `capability-marketplace.md` - Marketplace concept (moved to roadmap)
- `creating-capabilities.md` - Creating capabilities (basic version in capabilities/overview.md)
- `using-capabilities.md` - Using capabilities (basic version in capabilities/overview.md)

**Current documentation:** See `docs/capabilities/overview.md` for the simplified, accurate documentation.

---

## Why Keep Stale Docs?

Stale docs are preserved to:
1. Maintain historical record of design decisions
2. Allow recovery of content if needed
3. Provide context for why certain approaches were abandoned
4. Help contributors understand evolution of the project

**Note:** Content in this directory is NOT built into the published documentation site.
