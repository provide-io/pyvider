# Pyvider Documentation Review & API Proposal

**Date:** 2025-10-24
**Version:** 0.0.1000 (Alpha)
**Author:** Claude Code Documentation Review

---

## Executive Summary

This document provides:
1. **Comprehensive documentation review** of all 62 Pyvider documentation files
2. **Current API analysis** based on actual codebase and pyvider-components usage
3. **Dual-tier API proposal** for improved developer experience while maintaining backward compatibility

**TL;DR:**
- Documentation is **well-structured and comprehensive** (⭐⭐⭐⭐/5)
- Critical issues: method naming inconsistencies, outdated examples need verification
- Proposal: Add simple CRUD API layer while keeping current `_hooks` for advanced use

---

## Table of Contents

1. [Documentation Review Findings](#documentation-review-findings)
2. [Current API Analysis](#current-api-analysis)
3. [Dual-Tier API Proposal](#dual-tier-api-proposal)
4. [Implementation Strategy](#implementation-strategy)
5. [Migration Guide](#migration-guide)
6. [Action Items](#action-items)

---

# Documentation Review Findings

## Overall Assessment

**Quality Score: ⭐⭐⭐⭐ (Very Good for an alpha project)**

### Strengths ✅

1. **Excellent Organization**
   - 62 documentation files across clean, logical structure
   - No numeric prefixes (clean folder names)
   - Clear hierarchy: Getting Started → Core Concepts → Guides → Schema → API
   - Well-configured mkdocs.yml with Material theme

2. **Comprehensive Coverage**
   - Getting Started: Installation, quick start, "what is Pyvider"
   - Core Concepts: Architecture, component model, schema system
   - Guides: 13+ covering providers, resources, data sources, functions, testing, debugging
   - Schema System: 10 dedicated docs with examples
   - Capabilities: 7 docs on capabilities system
   - Troubleshooting: Comprehensive guide with solutions

3. **Good Examples**
   - Quick start has complete working example (684 lines)
   - Code examples use async/await patterns
   - Schema examples demonstrate actual usage
   - Mermaid diagrams for architecture

4. **Accurate Versioning**
   - Correctly identifies as alpha (v0.0.1000)
   - Python 3.11+ requirement matches pyproject.toml
   - Proper API stability warnings

### Critical Issues ❌

#### 1. **Method Naming Inconsistency** (HIGHEST PRIORITY)

**Problem:** Documentation shows conflicting method names for resource lifecycle:

**Architecture docs show:**
```python
async def create(self, config):   # ❌ No underscore
async def update(self, config):   # ❌ No underscore
async def delete(self, state):    # ❌ No underscore
```

**Actual API requires:**
```python
async def _create_apply(self, ctx):   # ✅ With underscore
async def _update_apply(self, ctx):   # ✅ With underscore
async def _delete_apply(self, ctx):   # ✅ With underscore
async def read(self, ctx):            # ✅ No underscore (only one!)
```

**Affected Files:**
- `docs/core-concepts/architecture.md` (lines 140, 143, 176-178)
- `docs/core-concepts/component-model.md` (lines 124-179)
- Multiple guides showing simplified examples

**Impact:** New users will copy examples that won't work.

#### 2. **Quick Start Example Needs Verification** (HIGH PRIORITY)

**Issue:** The 684-line Quick Start example (`docs/getting-started/quick-start.md`) uses patterns that need verification:
- Uses `from pyvider.hub import ProviderHub`
- Uses `ProviderHub.get_provider()` pattern
- Return type: `tuple[State | None, None]` format

**Action Required:** Extract and test the complete example with current version 0.0.1000.

#### 3. **Broken Links Unknown** (HIGH PRIORITY)

**Issue:** Many internal references but link integrity unknown:
- Cross-references like `../guides/debugging.md`
- Link checker script exists: `scripts/check_doc_links.py`

**Action Required:** Run `python scripts/check_doc_links.py` and `mkdocs build --strict`

#### 4. **Missing Content Gaps** (MEDIUM PRIORITY)

**Ephemeral Resources:**
- Mentioned in core concepts
- API reference exists
- **Missing:** `guides/creating-ephemeral-resources.md`

**Functions Documentation:**
- `guides/creating-functions.md` exists but very brief
- Needs expansion with more examples

**Migration Guides:**
- No guide for upgrading between versions
- Alpha warns of breaking changes but no migration docs

**Tutorials Section:**
- mkdocs.yml references "Tutorials"
- No actual tutorial files (only points to external repo)

#### 5. **Schema Documentation Duplication** (MEDIUM PRIORITY)

**Problem:** Significant overlap between:
- `core-concepts/schema-system.md` (533 lines)
- `schema/overview.md` and 9 other schema docs

**Recommendation:**
- Core concepts should be high-level overview only (100 lines max)
- `schema/` directory should be definitive reference
- Add clear cross-references

### Python Version Consistency ✓

All documentation correctly states Python 3.11+ requirement:
- `docs/index.md`: "Python 3.11+"
- `docs/installation.md`: "Python: 3.11 or higher"
- `pyproject.toml`: `requires-python = ">=3.11"`

**Note:** CLAUDE.md mentions "(moving from 3.12+ to broaden compatibility)" - verify all examples work on 3.11.

---

# Current API Analysis

## Actual Resource API (Version 0.0.1000)

Based on `src/pyvider/resources/base.py` and pyvider-components implementations:

### Required Methods

| Method | Underscore | Phase | Required | Purpose |
|--------|-----------|-------|----------|---------|
| `read()` | ❌ NO | Refresh | ✅ Yes (abstract) | Read current resource state |
| `_validate_config()` | ✅ YES | Validation | ✅ Yes (abstract) | Validate configuration |
| `_delete_apply()` | ✅ YES | Apply | ✅ Yes (abstract) | Delete resource (apply phase) |

### Optional Hooks

| Method | Underscore | Phase | Default Behavior |
|--------|-----------|-------|------------------|
| `_create()` | ✅ YES | Plan | Returns `base_plan, None` |
| `_create_apply()` | ✅ YES | Apply | Returns `ctx.planned_state, ctx.private_state` |
| `_update()` | ✅ YES | Plan | Returns `base_plan, None` |
| `_update_apply()` | ✅ YES | Apply | Returns `ctx.planned_state, ctx.private_state` |
| `_delete_plan()` | ✅ YES | Plan | Returns `None, None` |

### Pattern Summary

**Only `read()` has NO underscore - all others have underscores.**

This signals:
- `read()` = public method (callable, part of protocol)
- `_create_apply()`, etc. = internal hooks (called by framework)

---

## What pyvider-components Actually Implements

Analyzed all 5 resource implementations in the official pyvider-components repository:

### Resources:
1. `file_content.py` - Manages file content
2. `local_directory.py` - Manages directories
3. `timed_token.py` - Token generation with private state
4. `private_state_verifier.py` - Tests private state encryption
5. `warning_example.py` - Demo resource with warnings

### Methods Used: ✅ ALL use the underscore pattern

```python
# Every resource implements:
async def read(self, ctx: ResourceContext) -> State | None
async def _validate_config(self, config: ConfigType) -> list[str]
async def _create(self, ctx, base_plan) -> tuple[dict, PrivateState | None]
async def _create_apply(self, ctx) -> tuple[State, PrivateState | None]
async def _update(self, ctx, base_plan) -> tuple[dict, PrivateState | None]
async def _update_apply(self, ctx) -> tuple[State, PrivateState | None]
async def _delete_apply(self, ctx) -> None
```

### Real-World Usage: Two-Phase Pattern

**Example from `file_content.py`:**

```python
async def _create(self, ctx, base_plan):
    """PLAN phase: Compute file hash"""
    if ctx.is_field_unknown("content"):
        base_plan["exists"] = True
        return base_plan, None

    # Compute hash during planning (no file I/O yet)
    base_plan["content_hash"] = hashlib.sha256(
        config.content.encode("utf-8")
    ).hexdigest()
    return base_plan, None

async def _create_apply(self, ctx):
    """APPLY phase: Actually write the file"""
    path = Path(planned_state.filename)
    ensure_dir(path.parent)
    atomic_write_text(path, planned_state.content)  # ← Actually writes
    return planned_state, None
```

**Example from `timed_token.py` (Private State):**

```python
async def _create(self, ctx, base_plan):
    """PLAN phase: Generate token in private state (encrypted)"""
    base_plan["id"] = a_unknown(a_str())
    base_plan["token"] = a_unknown(a_str())

    # Create sensitive data in private state
    private_state = TimedTokenPrivateState(
        token=f"token-{uuid.uuid4()}",
        expires_at=(datetime.now() + timedelta(hours=1)).isoformat()
    )
    return base_plan, private_state  # ← Private state created

async def _create_apply(self, ctx):
    """APPLY phase: Use private state from plan"""
    final_state = evolve(
        ctx.planned_state,
        id=f"timed-token-id-{uuid.uuid4()}",
        token=ctx.private_state.token,  # ← Use private state
        expires_at=ctx.private_state.expires_at
    )
    return final_state, ctx.private_state
```

### Key Finding

**The two-phase pattern (plan + apply) is actively used and necessary for:**
- Private state encryption (secrets, tokens)
- Computing unknown values during planning
- Separating "what will happen" from "do it now"

**Current API works but has DX issues:**
- ✅ Functional and correct
- ✅ Supports private state
- ✅ Properly separates plan/apply
- ❌ Verbose (7 methods minimum)
- ❌ Confusing naming (`_create` vs `_create_apply`)
- ❌ Not beginner-friendly

---

# Dual-Tier API Proposal

## Problem Statement

**Current API:**
```python
# Requires all these methods even for simple resources
async def _validate_config(self, config) -> list[str]
async def read(self, ctx) -> State | None
async def _create(self, ctx, base_plan) -> tuple[dict, None]
async def _create_apply(self, ctx) -> tuple[State, None]
async def _update(self, ctx, base_plan) -> tuple[dict, None]
async def _update_apply(self, ctx) -> tuple[State, None]
async def _delete_apply(self, ctx) -> None
```

**Issues:**
1. **Verbose**: 7 methods minimum
2. **Confusing**: Two create methods, two update methods
3. **Not intuitive**: Which one do I implement?
4. **Learning curve**: Plan vs apply separation is advanced

**But we NEED the current API for:**
- Private state encryption
- Unknown value handling during plan
- Terraform protocol compliance

## Solution: Dual-Tier API

Provide **two ways** to implement resources:

### Tier 1: Simple API (95% of resources)

```python
@register_resource("file")
class File(BaseResource):
    config_class = FileConfig
    state_class = FileState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            "path": a_str(required=True),
            "content": a_str(required=True),
            "id": a_str(computed=True),
        })

    # Simple CRUD - clean and obvious
    async def create(self, ctx: ResourceContext) -> FileState:
        """Create the file."""
        path = Path(ctx.config.path)
        path.write_text(ctx.config.content)
        return FileState(
            id=str(path.absolute()),
            path=str(path),
            content=ctx.config.content,
        )

    async def read(self, ctx: ResourceContext) -> FileState | None:
        """Read file state."""
        path = Path(ctx.state.path)
        if not path.exists():
            return None
        return FileState(
            id=ctx.state.id,
            path=str(path),
            content=path.read_text(),
        )

    async def update(self, ctx: ResourceContext) -> FileState:
        """Update the file."""
        path = Path(ctx.state.path)
        path.write_text(ctx.config.content)
        return FileState(
            id=ctx.state.id,
            path=str(path),
            content=ctx.config.content,
        )

    async def delete(self, ctx: ResourceContext) -> None:
        """Delete the file."""
        Path(ctx.state.path).unlink(missing_ok=True)
```

**Benefits:**
- ✅ Only 4 methods (create, read, update, delete)
- ✅ No underscores (clearly part of the interface)
- ✅ Matches Terraform Go SDK patterns
- ✅ Intuitive for beginners
- ✅ Framework handles plan/apply automatically

### Tier 2: Advanced Hooks (5% of resources)

```python
@register_resource("timed_token")
class TimedToken(BaseResource):
    config_class = TokenConfig
    state_class = TokenState
    private_state_class = TokenPrivateState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            "name": a_str(required=True),
            "id": a_str(computed=True),
            "token": a_str(computed=True, sensitive=True),
            "expires_at": a_str(computed=True, sensitive=True),
        })

    # Advanced: override plan/apply hooks for full control
    async def _create(
        self, ctx: ResourceContext, base_plan: dict
    ) -> tuple[dict, TokenPrivateState]:
        """Planning phase: generate token in private state."""
        private_state = TokenPrivateState(
            token=f"token-{uuid.uuid4()}",
            expires_at=(datetime.now() + timedelta(hours=1)).isoformat()
        )
        base_plan["id"] = a_unknown(a_str())
        base_plan["token"] = a_unknown(a_str())
        return base_plan, private_state

    async def _create_apply(
        self, ctx: ResourceContext
    ) -> tuple[TokenState, TokenPrivateState]:
        """Apply phase: use private state from plan."""
        state = evolve(
            ctx.planned_state,
            id=f"token-{uuid.uuid4()}",
            token=ctx.private_state.token,
            expires_at=ctx.private_state.expires_at,
        )
        return state, ctx.private_state

    async def read(self, ctx: ResourceContext) -> TokenState | None:
        """Read with private state."""
        if ctx.private_state:
            return evolve(
                ctx.state,
                token=ctx.private_state.token,
                expires_at=ctx.private_state.expires_at,
            )
        return ctx.state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete (no cleanup needed)."""
        pass
```

**Benefits:**
- ✅ Full control over plan/apply separation
- ✅ Private state support
- ✅ Unknown value handling
- ✅ Same API as current (backward compatible)

---

## How It Works

### Framework Dispatching Logic

```python
class BaseResource(ABC):
    """
    Two-tier resource API:
    - Simple: Implement create(), read(), update(), delete()
    - Advanced: Implement _create(), _create_apply(), etc.
    """

    # ========================================
    # TIER 1: Simple API
    # ========================================

    async def create(self, ctx: ResourceContext) -> StateType:
        """
        Simple create - implement this for basic resources.
        Framework handles planning automatically.
        """
        raise NotImplementedError(
            "Implement either create() OR _create_apply()"
        )

    async def read(self, ctx: ResourceContext) -> StateType | None:
        """Read current state - ALWAYS implement this."""
        raise NotImplementedError("read() is required")

    async def update(self, ctx: ResourceContext) -> StateType:
        """Simple update - implement this for basic resources."""
        raise NotImplementedError(
            "Implement either update() OR _update_apply()"
        )

    async def delete(self, ctx: ResourceContext) -> None:
        """Simple delete - implement this for basic resources."""
        raise NotImplementedError(
            "Implement either delete() OR _delete_apply()"
        )

    # ========================================
    # TIER 2: Advanced Hooks
    # ========================================

    async def _create(
        self, ctx: ResourceContext, base_plan: dict[str, Any]
    ) -> tuple[dict[str, Any], PrivateStateType | None]:
        """
        ADVANCED: Override for custom planning logic.
        Default: returns base_plan unchanged.
        """
        return base_plan, None

    async def _create_apply(
        self, ctx: ResourceContext
    ) -> tuple[StateType, PrivateStateType | None]:
        """
        ADVANCED: Override for custom apply logic.
        Default: calls simple create() method.

        Framework checks:
        1. Is _create_apply overridden? Use it.
        2. Otherwise, call simple create() and return (state, None)
        """
        # Check if user implemented simple create()
        if self._has_simple_create():
            state = await self.create(ctx)
            return state, None
        # Fallback to planned state
        return ctx.planned_state, ctx.private_state

    async def _update_apply(
        self, ctx: ResourceContext
    ) -> tuple[StateType, PrivateStateType | None]:
        """
        ADVANCED: Override for custom update logic.
        Default: calls simple update() method.
        """
        if self._has_simple_update():
            state = await self.update(ctx)
            return state, None
        return ctx.planned_state, ctx.private_state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """
        ADVANCED: Override for custom delete logic.
        Default: calls simple delete() method.
        """
        if self._has_simple_delete():
            await self.delete(ctx)

    # Helper methods
    def _has_simple_create(self) -> bool:
        """Check if user implemented create() (not the base class version)."""
        return (
            self.create.__func__ is not BaseResource.create.__func__
        )

    def _has_simple_update(self) -> bool:
        """Check if user implemented update()."""
        return (
            self.update.__func__ is not BaseResource.update.__func__
        )

    def _has_simple_delete(self) -> bool:
        """Check if user implemented delete()."""
        return (
            self.delete.__func__ is not BaseResource.delete.__func__
        )
```

### Decision Flow

```
User creates resource
    ↓
Did they override _create_apply()?
    YES → Use _create_apply() directly (ADVANCED)
    NO  → Did they implement create()?
            YES → Call create(), wrap result (SIMPLE)
            NO  → Error: "Must implement create() or _create_apply()"
```

---

## Benefits of Dual-Tier Approach

### 1. **Progressive Disclosure**
- Beginners learn simple CRUD first
- Advanced users discover hooks when needed
- Documentation can focus on simple API initially

### 2. **Backward Compatible**
- Current pyvider-components code keeps working (uses `_hooks`)
- New code can use simple API
- Migration is opt-in, not forced

### 3. **Clear Mental Model**

**Simple tier (most users):**
```
create() → Framework handles planning → _create_apply() internally
```

**Advanced tier (power users):**
```
You implement _create() and _create_apply() directly
```

### 4. **Type System Clarity**

```python
# Simple API - just return State
async def create(self, ctx: ResourceContext) -> StateType:
    return FileState(...)

# Advanced API - return (State, PrivateState)
async def _create_apply(
    self, ctx: ResourceContext
) -> tuple[StateType, PrivateStateType | None]:
    return state, private_state
```

### 5. **Documentation Hierarchy**

```markdown
Getting Started → Use simple create(), read(), update(), delete()
Advanced Guide  → Use _create(), _create_apply() for private state
```

---

## Comparison Table

| Approach | Simple Resource | Advanced Resource | Learning Curve | Backward Compat |
|----------|----------------|-------------------|----------------|-----------------|
| **Current (all `_hooks`)** | 7 methods | 7 methods | Steep | N/A |
| **Simple only (CRUD)** | 4 methods | ❌ Can't do private state | Easy | ❌ Breaking |
| **Dual-tier (PROPOSED)** | 4 methods | 7 methods | Gradual | ✅ Full |

**Dual-tier wins on all metrics.**

---

# Implementation Strategy

## Phase 1: Add Simple API (Non-Breaking)

### Step 1: Update `BaseResource`

```python
# src/pyvider/resources/base.py

class BaseResource(ABC, Generic[ResourceType, StateType, ConfigType]):
    """
    Two-tier resource API for maximum flexibility:

    SIMPLE (recommended for most resources):
        Implement create(), read(), update(), delete()
        Framework handles plan/apply separation automatically.

    ADVANCED (for private state, custom planning):
        Override _create(), _create_apply(), _update(), etc.
        Full control over Terraform protocol.
    """

    # Add simple API methods with clear documentation
    async def create(self, ctx: ResourceContext) -> StateType:
        """
        Create a new resource instance.

        This is the SIMPLE API for resource creation. Implement this method
        for straightforward resources that don't need plan/apply separation.

        Args:
            ctx: Resource context with config, state, and metadata

        Returns:
            StateType: The created resource state

        Example:
            async def create(self, ctx: ResourceContext) -> FileState:
                path = Path(ctx.config.path)
                path.write_text(ctx.config.content)
                return FileState(id=str(path), path=str(path), ...)

        Note:
            For advanced use cases (private state, unknown values),
            override _create_apply() instead. See Advanced Guide.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement either "
            f"create() or _create_apply()"
        )

    # Add other simple methods (update, delete) with similar docs
    # ...

    # Update _create_apply to use simple API as fallback
    async def _create_apply(
        self, ctx: ResourceContext
    ) -> tuple[StateType | None, PrivateStateType | None]:
        """
        ADVANCED: Apply resource creation with optional private state.

        Override this for:
        - Resources with sensitive data (private state)
        - Custom apply-time logic
        - Complex state transformations

        Default behavior:
            Calls simple create() if implemented, otherwise returns planned_state.
        """
        # Check if user implemented simple create()
        if self._is_method_overridden('create'):
            try:
                state = await self.create(ctx)
                return state, None
            except NotImplementedError:
                pass

        # Fallback: use planned state from plan phase
        return ctx.planned_state, ctx.private_state

    def _is_method_overridden(self, method_name: str) -> bool:
        """Check if a method was overridden by the subclass."""
        method = getattr(self, method_name)
        base_method = getattr(BaseResource, method_name)
        return method.__func__ is not base_method.__func__
```

### Step 2: Add Tests

```python
# tests/resources/test_simple_api.py

class TestSimpleAPI:
    """Test simple CRUD API for resources."""

    @pytest.mark.asyncio
    async def test_simple_create_is_called_by_create_apply(self):
        """Simple create() is called during _create_apply()."""

        class SimpleResource(BaseResource):
            config_class = SimpleConfig
            state_class = SimpleState

            async def create(self, ctx):
                return SimpleState(id="123", name=ctx.config.name)

            async def read(self, ctx):
                return ctx.state

            async def _validate_config(self, config):
                return []

        resource = SimpleResource()
        ctx = ResourceContext(
            config=SimpleConfig(name="test"),
            planned_state=SimpleState(id=None, name="test")
        )

        state, private_state = await resource._create_apply(ctx)

        assert state.id == "123"
        assert state.name == "test"
        assert private_state is None

    @pytest.mark.asyncio
    async def test_advanced_hooks_override_simple_api(self):
        """Advanced _create_apply() takes precedence over simple create()."""

        class AdvancedResource(BaseResource):
            config_class = AdvancedConfig
            state_class = AdvancedState
            private_state_class = AdvancedPrivateState

            async def _create_apply(self, ctx):
                # Advanced implementation with private state
                return (
                    AdvancedState(id="adv-123"),
                    AdvancedPrivateState(secret="token")
                )

            async def create(self, ctx):
                # This should NOT be called
                raise AssertionError("Simple create() should not be called")

            async def read(self, ctx):
                return ctx.state

            async def _validate_config(self, config):
                return []

        resource = AdvancedResource()
        ctx = ResourceContext(config=AdvancedConfig(), planned_state=None)

        state, private_state = await resource._create_apply(ctx)

        assert state.id == "adv-123"
        assert private_state.secret == "token"
```

### Step 3: Update Type Hints

```python
# src/pyvider/resources/base.py

from typing import TypeVar, Generic, Protocol, runtime_checkable

@runtime_checkable
class SimpleResourceProtocol(Protocol[StateType, ConfigType]):
    """Protocol for simple CRUD resources."""

    async def create(self, ctx: ResourceContext) -> StateType: ...
    async def read(self, ctx: ResourceContext) -> StateType | None: ...
    async def update(self, ctx: ResourceContext) -> StateType: ...
    async def delete(self, ctx: ResourceContext) -> None: ...

@runtime_checkable
class AdvancedResourceProtocol(Protocol[StateType, ConfigType, PrivateStateType]):
    """Protocol for advanced resources with plan/apply separation."""

    async def _create(self, ctx: ResourceContext, base_plan: dict) -> tuple[dict, PrivateStateType | None]: ...
    async def _create_apply(self, ctx: ResourceContext) -> tuple[StateType, PrivateStateType | None]: ...
    async def read(self, ctx: ResourceContext) -> StateType | None: ...
    # ... etc
```

---

## Phase 2: Update Documentation

### Step 1: Reorganize Guides

**New structure:**

```
guides/
├── creating-providers.md          (existing, update)
├── creating-resources.md          (REWRITE - simple API first)
├── creating-resources-advanced.md (NEW - advanced hooks)
├── creating-data-sources.md       (existing, update)
├── creating-functions.md          (existing, expand)
├── creating-ephemeral-resources.md (NEW)
```

### Step 2: Rewrite `creating-resources.md`

```markdown
# Creating Resources

Resources represent manageable infrastructure with full CRUD lifecycle.

## Simple Resources (Recommended)

Most resources can be implemented with simple CRUD methods:

### Minimal Example

\`\`\`python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, PvsSchema
import attrs

@attrs.define
class FileConfig:
    path: str
    content: str

@attrs.define
class FileState:
    id: str
    path: str
    content: str

@register_resource("file")
class File(BaseResource):
    config_class = FileConfig
    state_class = FileState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource({
            "path": a_str(required=True),
            "content": a_str(required=True),
            "id": a_str(computed=True),
        })

    async def create(self, ctx: ResourceContext) -> FileState:
        """Create a new file."""
        Path(ctx.config.path).write_text(ctx.config.content)
        return FileState(
            id=ctx.config.path,
            path=ctx.config.path,
            content=ctx.config.content,
        )

    async def read(self, ctx: ResourceContext) -> FileState | None:
        """Read file state."""
        path = Path(ctx.state.path)
        if not path.exists():
            return None  # Deleted outside Terraform
        return FileState(
            id=ctx.state.id,
            path=str(path),
            content=path.read_text(),
        )

    async def update(self, ctx: ResourceContext) -> FileState:
        """Update file content."""
        Path(ctx.state.path).write_text(ctx.config.content)
        return FileState(
            id=ctx.state.id,
            path=ctx.state.path,
            content=ctx.config.content,
        )

    async def delete(self, ctx: ResourceContext) -> None:
        """Delete the file."""
        Path(ctx.state.path).unlink(missing_ok=True)
\`\`\`

That's it! Four methods implement a complete resource.

## When to Use Advanced API

Use the advanced plan/apply hooks when you need:

1. **Private State** - Encrypted sensitive data (tokens, secrets)
2. **Unknown Values** - Handle Terraform's unknown values during plan
3. **Custom Planning** - Complex logic during plan phase

See [Advanced Resources Guide](creating-resources-advanced.md) for details.

## See Also

- [Advanced Resources](creating-resources-advanced.md) - Plan/apply separation
- [Schema System](../schema/overview.md) - Define resource schemas
- [Testing Resources](testing-providers.md) - Test strategies
\`\`\`
```

### Step 3: Create `creating-resources-advanced.md`

```markdown
# Advanced Resources

This guide covers advanced resource patterns using plan/apply separation.

## When to Use Advanced API

Use the `_create()`, `_create_apply()` hooks when you need:

### 1. Private State (Encrypted Secrets)

\`\`\`python
@register_resource("api_token")
class APIToken(BaseResource):
    config_class = TokenConfig
    state_class = TokenState
    private_state_class = TokenPrivateState

    async def _create(self, ctx, base_plan):
        """Generate token during plan, store in private state."""
        private_state = TokenPrivateState(
            token=generate_secure_token(),
            secret_key=generate_key()
        )
        base_plan["id"] = a_unknown(a_str())  # Unknown until apply
        return base_plan, private_state

    async def _create_apply(self, ctx):
        """Use private state to finalize resource."""
        state = TokenState(
            id=f"token-{uuid.uuid4()}",
            token=ctx.private_state.token,  # From plan phase
        )
        return state, ctx.private_state

    async def read(self, ctx):
        """Include private state in read."""
        if ctx.private_state:
            return TokenState(
                id=ctx.state.id,
                token=ctx.private_state.token,
            )
        return ctx.state
\`\`\`

### 2. Unknown Values During Plan

[More examples...]

## Migration from Simple API

Already using simple `create()`? Easy upgrade:

[Migration guide...]
\`\`\`
```

### Step 4: Update Quick Start

```markdown
# Quick Start

Build your first Terraform provider in 5 minutes!

[Use the SIMPLE API in the example]

\`\`\`python
async def create(self, ctx: ResourceContext) -> FileState:
    path = Path(ctx.config.path)
    path.write_text(ctx.config.content)
    return FileState(...)

async def read(self, ctx: ResourceContext) -> FileState | None:
    path = Path(ctx.state.path)
    if not path.exists():
        return None
    return FileState(...)

async def update(self, ctx: ResourceContext) -> FileState:
    path = Path(ctx.state.path)
    path.write_text(ctx.config.content)
    return FileState(...)

async def delete(self, ctx: ResourceContext) -> None:
    Path(ctx.state.path).unlink(missing_ok=True)
\`\`\`

[Rest of quick start...]

## Next Steps

- For advanced features, see [Advanced Resources](guides/creating-resources-advanced.md)
\`\`\`
```

---

## Phase 3: Migration Guide

### For Existing Code (pyvider-components)

**Good news: No changes required!**

Existing code using `_create_apply()`, `_update_apply()` continues to work:

```python
# This still works exactly as before
class ExistingResource(BaseResource):
    async def _create_apply(self, ctx):
        return state, private_state

    async def _update_apply(self, ctx):
        return state, private_state

    async def read(self, ctx):
        return state

    async def _delete_apply(self, ctx):
        pass
```

### Optional: Simplify to New API

For resources without private state, optionally simplify:

**Before:**
```python
async def _create_apply(self, ctx):
    planned_state = cast(FileContentState, ctx.planned_state)
    path = Path(planned_state.filename)
    ensure_dir(path.parent)
    atomic_write_text(path, planned_state.content)
    return planned_state, None

async def _update_apply(self, ctx):
    return await self._create_apply(ctx)

async def _delete_apply(self, ctx):
    state = cast(FileContentState, ctx.state)
    path = Path(state.filename)
    if path.is_file():
        safe_delete(path)
```

**After (simplified):**
```python
async def create(self, ctx):
    path = Path(ctx.config.filename)
    ensure_dir(path.parent)
    atomic_write_text(path, ctx.config.content)
    return FileContentState(
        filename=str(path),
        content=ctx.config.content,
        exists=True,
        content_hash=hashlib.sha256(ctx.config.content.encode()).hexdigest()
    )

async def update(self, ctx):
    return await self.create(ctx)  # Reuse create logic

async def delete(self, ctx):
    path = Path(ctx.state.filename)
    if path.is_file():
        safe_delete(path)
```

**Benefits of migration:**
- Cleaner, more readable code
- Less boilerplate
- Easier to understand for new contributors

**When NOT to migrate:**
- Resource uses private state
- Resource needs plan/apply separation
- Resource handles unknown values explicitly

---

# Action Items

## Priority 1: Critical Fixes (Do First)

### 1. Fix Method Naming in Documentation ⚠️

**Issue:** Docs show `create()`, `update()`, `delete()` but API requires `_create_apply()`, `_update_apply()`, `_delete_apply()`

**Files to update:**
- [ ] `docs/core-concepts/architecture.md` (lines 140, 143, 176-178)
- [ ] `docs/core-concepts/component-model.md` (lines 124-179)
- [ ] Search all docs for `async def create(` and verify context

**Quick fix (before implementing dual-tier):**
```markdown
# Change from:
async def create(self, config: Config) -> State:

# Change to:
async def _create_apply(self, ctx: ResourceContext) -> tuple[State, None]:
```

### 2. Verify Quick Start Example ⚠️

**Action:**
```bash
# Extract the 684-line example from docs/getting-started/quick-start.md
# Save to test_quickstart.py
# Run: uv run python test_quickstart.py
# Fix any issues found
```

**Files:**
- [ ] `docs/getting-started/quick-start.md` (lines 30-369)

### 3. Run Link Checker ⚠️

**Action:**
```bash
python scripts/check_doc_links.py
mkdocs build --strict
# Fix all broken links found
```

---

## Priority 2: Content Additions

### 4. Add Missing Guide: Ephemeral Resources

**Create:**
- [ ] `docs/guides/creating-ephemeral-resources.md`

**Template:**
```markdown
# Creating Ephemeral Resources

Ephemeral resources manage short-lived connections or sessions.

## What are Ephemeral Resources?

Unlike regular resources, ephemeral resources:
- Have open/renew/close lifecycle (not CRUD)
- Exist only during terraform apply
- Used for temporary credentials, connections, locks

## Example: Database Connection

[Complete example with open(), renew(), close()]
```

### 5. Expand Functions Documentation

**Update:**
- [ ] `docs/guides/creating-functions.md` - Add more examples
- [ ] Add section on function composition
- [ ] Add section on function testing

### 6. Add Example Tutorials

**Create:**
- [ ] `docs/examples/rest-api-provider.md` - Complete REST API example
- [ ] `docs/examples/database-provider.md` - Complete database example

---

## Priority 3: Organization & Polish

### 7. Reduce Schema Documentation Duplication

**Action:**
- [ ] Trim `docs/core-concepts/schema-system.md` to 100 lines (overview only)
- [ ] Ensure `docs/schema/overview.md` is comprehensive
- [ ] Add clear "See schema docs for details" links in core-concepts
- [ ] Remove duplicate examples

### 8. Create Migration Documentation

**Create:**
- [ ] `docs/migration/` directory
- [ ] `docs/migration/pre-1.0.md` - Placeholder for future migrations
- [ ] Document deprecation policy

---

## Priority 4: Dual-Tier API Implementation (Future)

### 9. Implement Simple API Layer

**Code changes:**
- [ ] Update `src/pyvider/resources/base.py` with simple CRUD methods
- [ ] Add `_is_method_overridden()` helper
- [ ] Update `_create_apply()` to use simple `create()` as fallback
- [ ] Add comprehensive tests

**Timeline:** After Priority 1-3 complete, before 1.0 release

### 10. Update All Documentation for Dual-Tier

**Documentation changes:**
- [ ] Rewrite `docs/guides/creating-resources.md` (simple API first)
- [ ] Create `docs/guides/creating-resources-advanced.md` (plan/apply hooks)
- [ ] Update `docs/getting-started/quick-start.md` (use simple API)
- [ ] Update all examples to use simple API
- [ ] Add migration guide for existing code

**Timeline:** After implementation complete

---

## Verification Checklist

Before marking documentation review complete:

- [ ] All broken links fixed
- [ ] Quick start example tested and verified working
- [ ] Method naming consistent across all docs
- [ ] Python 3.11 compatibility verified
- [ ] All Priority 1 items complete
- [ ] mkdocs builds without errors: `mkdocs build --strict`
- [ ] Documentation link checker passes: `python scripts/check_doc_links.py`

---

## Summary

### Current State
- **Documentation:** ⭐⭐⭐⭐/5 (Very good for alpha)
- **API:** Functional but verbose
- **DX:** Needs improvement for beginners

### Immediate Actions
1. Fix method naming inconsistencies in docs
2. Verify Quick Start example works
3. Run link checker and fix broken links

### Future Enhancement
- Implement dual-tier API (simple + advanced)
- Rewrite documentation to focus on simple API
- Maintain backward compatibility with current API

### Timeline
- **Priority 1 (Critical):** 1-2 days
- **Priority 2 (Content):** 1 week
- **Priority 3 (Polish):** 1 week
- **Priority 4 (Dual-tier):** 2-3 weeks

---

**Document Version:** 1.0
**Last Updated:** 2025-10-24
**Next Review:** After Priority 1 completion
