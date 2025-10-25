# Documentation Reorganization Plan

## Overview

This document outlines the proposed reorganization of Pyvider's documentation to improve navigation and discoverability.

## Current Structure Issues

The `guides/` directory currently contains 20 files covering disparate topics without clear grouping:
- Component creation guides
- Development tools (testing, debugging, logging)
- Production/operational guides
- User guides
- Advanced topics

This makes it difficult for users to find relevant documentation quickly.

## Proposed Changes

### 1. Reorganize `guides/` into Subdirectories

```
docs/guides/
├── building-components/      # NEW - Component creation
│   ├── creating-providers.md
│   ├── creating-resources.md
│   ├── creating-data-sources.md
│   ├── creating-functions.md
│   └── using-decorators.md
│
├── development/               # NEW - Development tools
│   ├── testing-providers.md
│   ├── debugging.md
│   ├── logging.md
│   └── error-handling.md
│
├── production/                # NEW - Operational guides
│   ├── best-practices.md
│   ├── production-readiness.md
│   ├── security-best-practices.md
│   └── performance-optimization.md
│
├── advanced/                  # NEW - Advanced topics
│   ├── provider-lifecycle.md
│   ├── advanced-patterns.md
│   └── advanced-provider-features.md
│
└── usage/                     # NEW - End-user guides
    ├── configuration.md
    ├── managing-resources.md
    ├── using-data-sources.md
    └── using-functions.md
```

### 2. File Movement Plan

#### Create New Directories
```bash
mkdir -p docs/guides/building-components
mkdir -p docs/guides/development
mkdir -p docs/guides/production
mkdir -p docs/guides/advanced
mkdir -p docs/guides/usage
```

#### Move Files

**To `building-components/`:**
```bash
git mv docs/guides/creating-providers.md docs/guides/building-components/
git mv docs/guides/creating-resources.md docs/guides/building-components/
git mv docs/guides/creating-data-sources.md docs/guides/building-components/
git mv docs/guides/creating-functions.md docs/guides/building-components/
git mv docs/guides/using-decorators.md docs/guides/building-components/
```

**To `development/`:**
```bash
git mv docs/guides/testing-providers.md docs/guides/development/
git mv docs/guides/debugging.md docs/guides/development/
git mv docs/guides/logging.md docs/guides/development/
git mv docs/guides/error-handling.md docs/guides/development/
```

**To `production/`:**
```bash
git mv docs/guides/best-practices.md docs/guides/production/
git mv docs/guides/production-readiness.md docs/guides/production/
git mv docs/guides/security-best-practices.md docs/guides/production/
git mv docs/guides/performance-optimization.md docs/guides/production/
```

**To `advanced/`:**
```bash
git mv docs/guides/provider-lifecycle.md docs/guides/advanced/
git mv docs/guides/advanced-patterns.md docs/guides/advanced/
git mv docs/guides/advanced-provider-features.md docs/guides/advanced/
```

**To `usage/`:**
```bash
git mv docs/guides/configuration.md docs/guides/usage/
git mv docs/guides/managing-resources.md docs/guides/usage/
git mv docs/guides/using-data-sources.md docs/guides/usage/
git mv docs/guides/using-functions.md docs/guides/usage/
```

### 3. Update Internal Links

After moving files, update all internal links in the documentation. Common patterns:

**Before:**
```markdown
[Creating Providers](../guides/creating-providers.md)
[Best Practices](guides/best-practices.md)
```

**After:**
```markdown
[Creating Providers](../guides/building-components/creating-providers.md)
[Best Practices](guides/production/best-practices.md)
```

### 4. Updated mkdocs.yml Navigation

See `mkdocs.yml.proposed` for the complete updated navigation structure.

## Benefits

1. **Clearer Navigation** - Users can quickly identify which section contains the information they need
2. **Better Grouping** - Related topics are co-located
3. **Scalability** - Easy to add new guides to appropriate sections
4. **Progressive Disclosure** - Beginners can focus on building-components, advanced users on advanced topics
5. **Better SEO** - More logical URL structure

## Implementation Steps

1. ✅ Create reorganization plan (this document)
2. ⏳ Update mkdocs.yml with new navigation
3. ⏳ Create new directories
4. ⏳ Move files using git mv
5. ⏳ Update internal links throughout documentation
6. ⏳ Test with `mkdocs serve`
7. ⏳ Run link checker: `python scripts/check_doc_links.py`
8. ⏳ Build in strict mode: `mkdocs build --strict`
9. ⏳ Commit changes

## Rollback Plan

If issues arise, the reorganization can be rolled back using:
```bash
git revert <commit-hash>
```

All file movements are tracked in git history.

## Notes

- Keep all filenames the same to minimize broken external links
- Update any external references (README.md, etc.)
- Consider adding redirects for old paths if needed
- Update CLAUDE.md if it references specific doc paths
