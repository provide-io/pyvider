# Documentation Fixes Handoff

**Date**: 2025-10-24
**Status**: Phase 1 Complete (Critical fixes), Phase 2 In Progress (High/Medium priority)

---

## Executive Summary

The Pyvider documentation had significant accuracy issues due to an API redesign that wasn't reflected in the docs. The schema system changed from a class-based `Attribute()` API to factory functions (`a_str()`, `a_num()`, etc.), and the resource lifecycle changed to use `ResourceContext` instead of simple CRUD methods.

**Impact**: Users following the old documentation would write non-functional code.

**Progress**:
- ✅ Phase 1 Complete: Critical files fixed (quick-start, schema-system, attributes, capabilities)
- 🔄 Phase 2 In Progress: Remaining guide files need updates
- ⏳ Phase 3 Pending: Testing and validation

---

## Phase 1: Completed Fixes

### 1. Quick Start Guide ✅
**File**: `docs/getting-started/quick-start.md`
**Status**: Completely rewritten
**Changes**:
- Updated imports to use factory functions: `s_resource`, `a_str`, `a_num`, `a_bool`
- Fixed all schema definitions to use `get_schema()` classmethod
- Updated resource lifecycle to use `ResourceContext` API
- Fixed methods: `_create_apply()`, `_update_apply()`, `_delete_apply()`, `read(ctx)`
- Separated attrs classes from schema definitions

### 2. Schema Attributes Documentation ✅
**File**: `docs/schema/attributes.md`
**Status**: Completely rewritten (467 lines)
**Changes**:
- Replaced entire file with correct factory function API
- Comprehensive coverage of all attribute types
- Working examples with Terraform HCL equivalents
- Validation patterns and best practices

### 3. Core Schema System ✅
**File**: `docs/core-concepts/schema-system.md`
**Status**: Completed from stub (523 lines)
**Changes**:
- Complete guide to schema system
- Factory functions philosophy
- ResourceContext integration
- Best practices and advanced topics

### 4. Capabilities Overview ✅
**File**: `docs/capabilities/overview.md`
**Status**: Completely rewritten
**Changes**:
- Professional technical tone (removed "hero"/"superpowers" language)
- Practical examples (OAuth2, Caching, Retry, Metrics)
- Capability composition patterns

### 5. Index Page ✅
**File**: `docs/index.md`
**Status**: Fixed broken link
**Changes**:
- Replaced link to non-existent `tutorials/first-provider.md`
- Now links to pyvider-components examples

---

## Phase 2: High Priority Fixes (In Progress)

These files need updates to use the correct schema API and ResourceContext patterns.

### Files Requiring Updates

1. **docs/guides/creating-providers.md** (773 lines)
2. **docs/guides/creating-resources.md** (57 lines)
3. **docs/guides/creating-data-sources.md** (45 lines)
4. **docs/guides/creating-functions.md** (37 lines)
5. **docs/guides/using-decorators.md** (383 lines)
6. **docs/core-concepts/component-model.md** (has Attribute() references)
7. **docs/core-concepts/architecture.md** (has Attribute() references)

### Medium Priority

8. **docs/schema/computed-attributes.md**
9. **docs/schema/blocks.md**
10. **docs/schema/schema-by-example.md**

---

## The Correct API Patterns

### ❌ OLD (Incorrect) Pattern

```python
from pyvider.schema import Attribute

@attrs.define
class Config:
    name: str = Attribute(required=True, description="Server name")
    port: int = Attribute(default=8080, description="Port number")

async def create(self, config: Config) -> State:
    # CRUD method (doesn't exist)
    pass
```

### ✅ NEW (Correct) Pattern

```python
from pyvider.schema import s_resource, a_str, a_num, PvsSchema
from pyvider.resources.context import ResourceContext

@attrs.define
class Config:
    """Runtime config class (separate from schema)."""
    name: str
    port: int = 8080

@classmethod
def get_schema(cls) -> PvsSchema:
    """Define Terraform schema."""
    return s_resource({
        "name": a_str(required=True, description="Server name"),
        "port": a_num(default=8080, description="Port number"),
        "id": a_str(computed=True, description="Unique ID"),
    })

async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
    # Use ResourceContext, not plain config
    if not ctx.config:
        return None, None
    # Implementation here
    pass

async def read(self, ctx: ResourceContext) -> State | None:
    # Use ResourceContext
    pass

async def _update_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
    # Use ResourceContext
    pass

async def _delete_apply(self, ctx: ResourceContext) -> None:
    # Use ResourceContext
    pass
```

---

## Search and Replace Patterns

### Pattern 1: Import Statements

**Find:**
```python
from pyvider.schema import Attribute
```

**Replace with:**
```python
from pyvider.schema import s_resource, s_data_source, s_provider, a_str, a_num, a_bool, a_list, a_map, PvsSchema
from pyvider.resources.context import ResourceContext
```

### Pattern 2: Schema Definition in Attrs Class

**Find pattern:**
```python
@attrs.define
class Config:
    field_name: type = Attribute(...)
```

**Replace pattern:**
```python
# Two separate things:

# 1. Runtime attrs class (for Python type safety)
@attrs.define
class Config:
    field_name: type = default_value  # Just normal attrs

# 2. Schema definition (for Terraform)
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "field_name": a_str(...),  # Use factory functions
    })
```

### Pattern 3: Resource Lifecycle Methods

**Find:**
```python
async def create(self, config: Config) -> State:
async def read(self, state: State) -> State | None:
async def update(self, config: Config, state: State) -> State:
async def delete(self, state: State) -> None:
```

**Replace with:**
```python
async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
async def read(self, ctx: ResourceContext) -> State | None:
async def _update_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
async def _delete_apply(self, ctx: ResourceContext) -> None:
```

### Pattern 4: Data Source Read Method

**Find:**
```python
async def read(self, config: Config) -> Data:
```

**Replace with:**
```python
async def read(self, config: Config) -> Data:
    # Data sources still use config directly, not ResourceContext
```

### Pattern 5: Provider Configuration

**Find:**
```python
@attrs.define
class Config:
    api_key: str = Attribute(required=True, sensitive=True)
```

**Replace with:**
```python
@attrs.define
class ProviderConfig:
    """Runtime provider config."""
    api_key: str

def _build_schema(self) -> PvsSchema:
    """Define provider schema."""
    return s_provider({
        "api_key": a_str(required=True, sensitive=True, description="API key"),
    })
```

---

## Systematic Update Instructions

### For Each Guide File:

1. **Update imports** (top of file)
   - Remove: `from pyvider.schema import Attribute`
   - Add: Factory function imports + ResourceContext

2. **Find all code examples** with `@attrs.define` + `Attribute()`
   - Separate into: runtime attrs class + `get_schema()` method
   - Convert `Attribute()` calls to factory functions

3. **Update resource lifecycle examples**
   - Change method signatures to use `ResourceContext`
   - Update method names: `_create_apply`, `_update_apply`, `_delete_apply`

4. **Update provider configuration examples**
   - Add `_build_schema()` method
   - Separate config class from schema

5. **Test the examples** (if possible)
   - Verify imports are correct
   - Check that schemas are valid

### Verification Commands

```bash
# Find files still using old API
grep -r "Attribute(" docs/ --include="*.md"

# Find files missing get_schema
grep -L "get_schema" docs/guides/*.md

# Find files missing ResourceContext
grep -L "ResourceContext" docs/guides/creating-*.md
```

---

## Factory Function Reference

### Schema Factories
- `s_resource({...})` - Create resource schema
- `s_data_source({...})` - Create data source schema
- `s_provider({...})` - Create provider schema

### Simple Attribute Factories
- `a_str(description="...", required=True, default="...", sensitive=False)`
- `a_num(description="...", default=0)`
- `a_bool(description="...", default=True)`
- `a_dyn(description="...")` - Dynamic type

### Collection Attribute Factories
- `a_list(element_type, description="...", default=[])`
- `a_map(element_type, description="...", default={})`
- `a_set(element_type, description="...")`
- `a_tuple([type1, type2], description="...")`

### Complex Attribute Factories
- `a_obj({...}, description="...")` - Nested object

### Block Factories
- `b_main(attributes={...}, block_types=[...])` - Main block
- `b_list("name", attributes={...})` - List of blocks (0+)
- `b_single("name", attributes={...})` - Single block (0-1)
- `b_set("name", attributes={...})` - Set of blocks
- `b_map("name", attributes={...})` - Map of blocks
- `b_group("name", attributes={...})` - Group block

### Common Attribute Parameters
- `required: bool` - Must be provided
- `default: Any` - Default value if not provided
- `computed: bool` - Set by provider (not user)
- `sensitive: bool` - Masked in logs/UI
- `description: str` - Help text
- `validators: list[Callable]` - Validation functions

---

## ResourceContext API

### Properties
- `ctx.config` - Typed config attrs instance (or None if unknown values)
- `ctx.config_cty` - Raw CTY value from Terraform
- `ctx.state` - Current state attrs instance (or None)
- `ctx.state_cty` - Raw state CTY value
- `ctx.planned_state` - Planned state attrs instance
- `ctx.planned_state_cty` - Planned state CTY value
- `ctx.private_state` - Private (encrypted) state
- `ctx.provider_meta` - Provider metadata

### Methods
- `ctx.is_field_unknown(field_name)` - Check if field is unknown during planning
- `ctx.add_error(message)` - Add validation error
- `ctx.add_warning(message)` - Add warning diagnostic

### Lifecycle Methods
- `async def read(ctx: ResourceContext) -> State | None` - Refresh state
- `async def _create_apply(ctx: ResourceContext) -> tuple[State | None, PrivateState | None]` - Create resource
- `async def _update_apply(ctx: ResourceContext) -> tuple[State | None, PrivateState | None]` - Update resource
- `async def _delete_apply(ctx: ResourceContext) -> None` - Delete resource

### Planning Methods (Advanced)
- `async def _create(ctx: ResourceContext, base_plan: dict) -> tuple[dict | None, PrivateState | None]` - Plan create
- `async def _update(ctx: ResourceContext, base_plan: dict) -> tuple[dict | None, PrivateState | None]` - Plan update

---

## Example: Complete Resource with Correct API

```python
from pyvider.resources import register_resource, BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import s_resource, a_str, a_num, a_bool, PvsSchema
import attrs

# Runtime config class (Python type safety)
@attrs.define
class ServerConfig:
    name: str
    port: int = 8080
    enabled: bool = True

# Runtime state class (Python type safety)
@attrs.define
class ServerState:
    id: str
    name: str
    port: int
    enabled: bool
    ip_address: str
    created_at: str

@register_resource("server")
class Server(BaseResource):
    """Manages a server resource."""

    config_class = ServerConfig
    state_class = ServerState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        """Define Terraform schema (what users see in HCL)."""
        return s_resource({
            # User inputs
            "name": a_str(required=True, description="Server name"),
            "port": a_num(default=8080, description="Port number"),
            "enabled": a_bool(default=True, description="Whether enabled"),

            # Provider outputs (computed)
            "id": a_str(computed=True, description="Unique ID"),
            "ip_address": a_str(computed=True, description="Assigned IP"),
            "created_at": a_str(computed=True, description="Creation timestamp"),
        })

    async def _validate_config(self, config: ServerConfig) -> list[str]:
        """Validate configuration."""
        errors = []
        if config.port < 1 or config.port > 65535:
            errors.append("Port must be between 1 and 65535")
        return errors

    async def read(self, ctx: ResourceContext) -> ServerState | None:
        """Refresh state from remote system."""
        if not ctx.state:
            return None

        # Call your API to get current state
        response = await self.api_client.get_server(ctx.state.id)

        if response.status == 404:
            return None  # Resource deleted outside Terraform

        # Return updated state
        return ServerState(
            id=ctx.state.id,
            name=response.name,
            port=response.port,
            enabled=response.enabled,
            ip_address=response.ip_address,
            created_at=ctx.state.created_at,
        )

    async def _create_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        """Create resource (apply phase)."""
        if not ctx.config:
            return None, None

        # Call your API to create
        response = await self.api_client.create_server(
            name=ctx.config.name,
            port=ctx.config.port,
            enabled=ctx.config.enabled,
        )

        # Return new state
        return ServerState(
            id=response.id,
            name=response.name,
            port=response.port,
            enabled=response.enabled,
            ip_address=response.ip_address,
            created_at=response.created_at,
        ), None

    async def _update_apply(self, ctx: ResourceContext) -> tuple[ServerState | None, None]:
        """Update resource (apply phase)."""
        if not ctx.config or not ctx.state:
            return None, None

        # Call your API to update
        response = await self.api_client.update_server(
            id=ctx.state.id,
            name=ctx.config.name,
            port=ctx.config.port,
            enabled=ctx.config.enabled,
        )

        # Return updated state
        return ServerState(
            id=ctx.state.id,
            name=response.name,
            port=response.port,
            enabled=response.enabled,
            ip_address=response.ip_address,
            created_at=ctx.state.created_at,
        ), None

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        """Delete resource (apply phase)."""
        if not ctx.state:
            return

        # Call your API to delete
        await self.api_client.delete_server(ctx.state.id)
```

---

## File-by-File Update Plan

### High Priority (Do First)

| File | Lines | Complexity | Estimated Time |
|------|-------|------------|----------------|
| creating-resources.md | 57 | Low | 30 min |
| creating-data-sources.md | 45 | Low | 30 min |
| creating-functions.md | 37 | Low | 20 min |
| creating-providers.md | 773 | High | 2-3 hours |
| using-decorators.md | 383 | Medium | 1-2 hours |

### Medium Priority (Do Second)

| File | Lines | Complexity | Estimated Time |
|------|-------|------------|----------------|
| component-model.md | ? | Medium | 1 hour |
| architecture.md | ? | Low | 30 min |
| computed-attributes.md | ? | Low | 30 min |
| blocks.md | ? | Medium | 1 hour |
| schema-by-example.md | ? | Medium | 1 hour |

### Lower Priority (Nice to Have)

| File | Notes |
|------|-------|
| testing-providers.md | Update to test ResourceContext API |
| best-practices.md | Update examples to use factory functions |
| debugging.md | Update debugging examples |

---

## Testing Recommendations

After updating documentation:

1. **Extract Code Examples**
   ```bash
   # Extract Python code blocks from markdown
   python scripts/extract_examples.py docs/guides/
   ```

2. **Syntax Check**
   ```bash
   # Check Python syntax of examples
   python -m py_compile extracted_examples/*.py
   ```

3. **Import Check**
   ```bash
   # Verify imports are valid
   python -c "from pyvider.schema import s_resource, a_str, a_num"
   ```

4. **Link Check**
   ```bash
   # Check for broken links
   python scripts/check_doc_links.py
   ```

5. **Build Docs**
   ```bash
   # Build with strict mode (fails on warnings)
   mkdocs build --strict
   ```

---

## Common Pitfalls to Avoid

### ❌ Don't: Mix old and new APIs

```python
# BAD: Mixing Attribute() with factory functions
from pyvider.schema import Attribute, s_resource, a_str

@attrs.define
class Config:
    name: str = Attribute(required=True)  # OLD API

@classmethod
def get_schema(cls):
    return s_resource({
        "name": a_str(required=True)  # NEW API
    })
```

### ✅ Do: Use factory functions consistently

```python
# GOOD: Consistent use of factory functions
from pyvider.schema import s_resource, a_str

@attrs.define
class Config:
    name: str  # Plain attrs

@classmethod
def get_schema(cls):
    return s_resource({
        "name": a_str(required=True)
    })
```

### ❌ Don't: Use old CRUD methods

```python
# BAD: These methods don't exist
async def create(self, config: Config) -> State:
async def update(self, config: Config, state: State) -> State:
async def delete(self, state: State) -> None:
```

### ✅ Do: Use ResourceContext methods

```python
# GOOD: Correct ResourceContext API
async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
async def _update_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
async def _delete_apply(self, ctx: ResourceContext) -> None:
async def read(self, ctx: ResourceContext) -> State | None:
```

---

## Questions & Answers

### Q: Do data sources use ResourceContext?
**A**: No, data sources use `async def read(self, config: ConfigType) -> DataType` with plain config.

### Q: What about provider configuration?
**A**: Providers use `async def configure(self, config: dict[str, CtyType])` and define schema with `def _build_schema(self) -> PvsSchema`.

### Q: Can I still use Attribute()?
**A**: No, the `Attribute` class doesn't exist in the codebase. Use factory functions.

### Q: What's the relationship between attrs classes and schemas?
**A**: They're separate:
- **Attrs classes**: Runtime Python objects for type safety
- **Schemas**: Terraform interface definition (what users see in HCL)
- The framework converts between them automatically

### Q: How do I handle unknown values during planning?
**A**: Use `ctx.is_field_unknown("field_name")` to check. Unknown values occur when a field depends on another resource that doesn't exist yet.

---

## Contact & Support

If you encounter issues while updating the documentation:

1. Check the completed files for reference:
   - `docs/getting-started/quick-start.md`
   - `docs/schema/attributes.md`
   - `docs/core-concepts/schema-system.md`

2. Verify against actual codebase:
   - `src/pyvider/schema/factory.py` - Factory functions
   - `src/pyvider/resources/base.py` - BaseResource API
   - `src/pyvider/resources/context.py` - ResourceContext

3. Run tests to verify examples:
   ```bash
   uv run pytest tests/
   ```

---

## Completion Checklist

### Phase 1: Critical Fixes ✅
- [x] Quick start guide
- [x] Schema attributes documentation
- [x] Core schema system documentation
- [x] Capabilities overview
- [x] Index page broken links

### Phase 2: High Priority 🔄
- [ ] creating-providers.md
- [ ] creating-resources.md
- [ ] creating-data-sources.md
- [ ] creating-functions.md
- [ ] using-decorators.md

### Phase 3: Medium Priority ⏳
- [ ] component-model.md
- [ ] architecture.md
- [ ] computed-attributes.md
- [ ] blocks.md
- [ ] schema-by-example.md

### Phase 4: Verification ⏳
- [ ] Extract all code examples
- [ ] Run syntax checks
- [ ] Build docs in strict mode
- [ ] Run link checker
- [ ] User testing with quick-start

---

**Last Updated**: 2025-10-24
**Next Review**: After Phase 2 completion
