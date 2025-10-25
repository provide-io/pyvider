# Pyvider Multi-Provider Architecture - Handoff Document

## Summary of Changes

Pyvider has been converted from a monolithic provider to a **pure framework** that supports multiple provider implementations. The framework is now ready for component packages like `pyvider-components` and third-party providers.

## What Was Completed

### 1. Pure Framework Architecture ✅

**Removed:**
- `[project.entry-points.pyvider]` from pyproject.toml
- `src/pyvider/providers/capabilities/` directory (CoreProviderCapability)
- `src/pyvider/providers/provider.py` (PyviderProvider class)

**Result:** pyvider package contains ZERO components by default

### 2. Provider Discovery System ✅

**Changes:**
- Added provider discovery to `src/pyvider/hub/discovery.py:98`
- Providers are discovered alongside resources/data sources/functions
- Discovery works via `@register_provider("name")` decorator

### 3. Dynamic Provider Instantiation ✅

**Changes in `src/pyvider/cli/provide_command.py`:**
- Removed hardcoded `PyviderProvider()` instantiation
- Now discovers all registered providers from hub
- Instantiates each provider dynamically
- Clear error when zero providers found

### 4. Auto-Discovery in BaseProvider ✅

**Enhanced `src/pyvider/providers/base.py`:**
- `BaseProvider.setup()` now auto-discovers capabilities
- Auto-composes provider schema from capability contributions
- Component packages get this for free - minimal boilerplate

### 5. Test Updates ✅

**Updated test files:**
- `tests/conftest.py` - Uses BaseProvider instead of PyviderProvider
- `tests/framework/test_schema_caching.py`
- `tests/tdd/test_tdd_capability_association.py`
- `tests/observability/test_handler_metrics.py`

**Test Results:** All 1230 tests pass ✅

---

## What Still Needs to Be Done

### Priority 1: Create pyvider-components Package Structure

The `pyvider-components` package exists but needs migration to the new architecture.

**Required Files to Create:**

#### 1. **Provider Registration**

Create `src/pyvider/components/provider.py`:
```python
from pyvider.providers import BaseProvider, ProviderMetadata, register_provider

@register_provider("pyvider")
class PyviderProvider(BaseProvider):
    """
    Reference implementation of a Pyvider provider.

    Manages standard components for local file manipulation,
    HTTP data sources, and utility functions.
    """

    def __init__(self):
        super().__init__(
            metadata=ProviderMetadata(
                name="pyvider",
                version="0.1.0"
            )
        )
```

#### 2. **Core Capability**

Create `src/pyvider/components/capabilities/core.py`:
```python
from typing import Any
from pyvider.capabilities import BaseCapability, register_capability
from pyvider.schema import PvsAttribute

@register_capability("core")
class CoreCapability(BaseCapability):
    """
    Core capability for pyvider provider.
    Provides base provider configuration (currently empty).
    """

    def __init__(self, config: Any | None = None):
        pass

    @staticmethod
    def get_schema_contribution() -> dict[str, PvsAttribute]:
        return {}
```

#### 3. **Entry Point Configuration**

Update `pyvider-components/pyproject.toml`:
```toml
[project.entry-points.pyvider]
pyvider-components = "pyvider.components"
```

#### 4. **Package __init__.py**

Update `src/pyvider/components/__init__.py` to import provider:
```python
# Ensure provider is registered on import
from pyvider.components.provider import PyviderProvider
from pyvider.components.capabilities.core import CoreCapability

__all__ = ["PyviderProvider", "CoreCapability"]
```

---

### Priority 2: Test the Integration

After creating the above files, test the complete workflow:

#### Test 1: Verify Framework is Pure
```bash
cd /Users/tim/code/gh/provide-io/pyvider

# Should show NO components
pyvider components list
# Expected: "No components found."
```

#### Test 2: Install pyvider-components in Editable Mode
```bash
cd /Users/tim/code/gh/provide-io/pyvider-components

# Install in editable mode
uv pip install -e .

# or if UV not available:
pip install -e .
```

#### Test 3: Verify Components Are Discovered
```bash
cd /Users/tim/code/gh/provide-io/pyvider

# Should now show components from pyvider-components
pyvider components list
```

**Expected Output:**
```
Provider:
  - pyvider

Capability:
  - core
  - api       (if exists in pyvider-components)
  - lens      (if exists in pyvider-components)

Resource:
  - file_content
  - local_directory
  - timed_token
  - (... other resources)

Data Source:
  - http_api
  - lens_jq
  - (... other data sources)

Function:
  - (... functions from pyvider-components)
```

#### Test 4: Verify Provider Can Start
```bash
# Should start without error
timeout 5 pyvider provide --force 2>&1 | head -20
```

**Expected:** Should see "Provider setup completed" logs, then timeout (that's ok)

**Should NOT see:** "No providers found" error

#### Test 5: Run Component Tests
```bash
cd /Users/tim/code/gh/provide-io/pyvider-components

# Run tests to verify components work
uv run pytest tests/ -v
```

---

### Priority 3: Fix Existing Components (If Needed)

The pyvider-components package currently has components that might use old patterns:

**Check for:**
- Old imports: `from pyvider.providers.provider import PyviderProvider`
- Old capability registration patterns
- Hard-coded provider references

**Files to potentially update:**
- `src/pyvider/components/capabilities/api.py`
- `src/pyvider/components/capabilities/lens.py`
- Any component that imports or references PyviderProvider

---

### Priority 4: Documentation Updates

**Files to update:**
- `pyvider-components/CLAUDE.md` - Update with new provider registration pattern
- `pyvider-components/README.md` - Document the provider structure
- `pyvider/docs/` - Update framework documentation

---

## Testing Checklist

- [ ] Framework shows no components when pyvider-components not installed
- [ ] `uv pip install -e .` in pyvider-components succeeds
- [ ] `pyvider components list` shows "pyvider" provider
- [ ] `pyvider components list` shows capabilities, resources, data sources, functions
- [ ] `pyvider provide --force` starts without "No providers found" error
- [ ] `pyvider-components` tests pass
- [ ] Can create a simple Terraform config using pyvider provider
- [ ] Terraform can run `terraform init` and `terraform plan`

---

## Known Issues / Gaps

### 1. Component-to-Provider Routing

**Current:** The first discovered provider is used for all operations
**TODO:** Implement routing based on resource type prefix

Example: `lens_deployment` should route to "lens" provider, not "pyvider" provider

**Code Location:** `src/pyvider/cli/provide_command.py:141-149`

**Future Enhancement:**
```python
# Instead of using first provider for everything
primary_provider = list(provider_instances.values())[0]

# Should route based on resource type:
def get_provider_for_resource(resource_type: str):
    prefix = resource_type.split('_')[0]  # e.g., "lens" from "lens_deployment"
    return provider_instances.get(prefix, primary_provider)
```

### 2. Multiple Provider Instance Support

**Current:** Only one provider instance runs
**TODO:** Support multiple provider instances with aliases

Terraform allows:
```hcl
provider "lens" {
  alias = "production"
  api_endpoint = "https://prod.lens.io"
}

provider "lens" {
  alias = "staging"
  api_endpoint = "https://staging.lens.io"
}
```

This requires protocol-level changes to track provider aliases.

### 3. Entry Point Group Naming

**Decision Made:** Using `"pyvider"` as entry point group name
**Alternative Considered:** `"pyvider.components"` (more explicit)

Current: `[project.entry-points.pyvider]`

Both are valid. Consider feedback from early adopters.

---

## Quick Reference

### For pyvider Framework

**Directory:** `/Users/tim/code/gh/provide-io/pyvider`

**Key Commands:**
```bash
# List components (should be empty without pyvider-components)
pyvider components list

# Try to start provider (should error: No providers found)
pyvider provide --force

# Run tests
uv run pytest tests/ -v
```

### For pyvider-components Package

**Directory:** `/Users/tim/code/gh/provide-io/pyvider-components`

**Key Files to Create/Update:**
- `src/pyvider/components/provider.py` (NEW)
- `src/pyvider/components/capabilities/core.py` (NEW)
- `pyproject.toml` (add entry point)
- `src/pyvider/components/__init__.py` (import provider)

**Key Commands:**
```bash
# Install in editable mode
uv pip install -e .

# Run tests
uv run pytest tests/ -v

# Check what's registered
cd ../pyvider
pyvider components list
```

---

## Success Criteria

### Minimum Viable Product (MVP)

✅ pyvider framework has zero components
✅ `pyvider components list` returns "No components found"
✅ `pyvider provide --force` errors with "No providers found"
⏳ pyvider-components installs successfully in editable mode
⏳ After installing pyvider-components, `pyvider components list` shows:
  - Provider: pyvider
  - Capabilities, resources, data sources, functions
⏳ `pyvider provide --force` starts successfully
⏳ All pyvider-components tests pass

### Stretch Goals

⏳ Create a minimal example provider (pyvider-lens or similar)
⏳ Document provider creation process
⏳ Test with Terraform/OpenTofu
⏳ Implement component-to-provider routing
⏳ Support multiple provider instances with aliases

---

## Next Steps

1. **Create the missing files** in pyvider-components (Priority 1)
2. **Test the installation flow** (Priority 2)
3. **Fix any broken components** (Priority 3)
4. **Update documentation** (Priority 4)
5. **Create example Terraform configs** using the pyvider provider
6. **Consider creating a minimal third-party provider** (e.g., pyvider-lens) to validate the pattern

---

## Questions / Decisions Needed

1. **Capability naming:** Should the core capability be called "core", "provider", or something else?
2. **Version synchronization:** Should pyvider-components version match pyvider version?
3. **Dependency specification:** How should pyvider-components specify pyvider dependency version?
4. **Provider naming:** Should pyvider-components register as "pyvider" or "pyvider-components"?
   - Recommendation: "pyvider" (cleaner in Terraform configs)

---

## Contact

If you have questions or hit issues:
- Framework architecture decisions are documented in `src/pyvider/providers/base.py`
- Discovery logic is in `src/pyvider/hub/discovery.py`
- All tests pass: `uv run pytest tests/` (1230 passed)

Last Updated: 2025-10-25
Created By: Claude Code (Assistant)
