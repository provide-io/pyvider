# Code Quality Improvement - Phases 2 & 3 Handoff Document

**Date:** 2025-10-24
**Branch:** `october-2025-tests`
**Status:** Phase 1 Complete ✅ | Phases 2-3 Ready to Start

---

## Phase 1 Complete - Summary

### ✅ Achievements

**All Code Quality Issues Fixed:**
- ✅ Fixed 9 broken `test_get_metadata.py` tests (updated mocks from `hub.registry.get()` to `hub.get_components()`)
- ✅ Fixed 3 ruff violations (unnecessary `.keys()` calls)
- ✅ Fixed 22 mypy type errors across 6 files
- ✅ Improved type safety: Used `object` instead of `Any` for `CtyType[T]` generics

**Test Results:**
```
1,187 tests passed
0 failures
0 ruff errors
0 mypy errors (in modified files)
```

**Files Modified:**
1. `tests/tfprotov6/handlers/test_get_metadata.py` - Updated test mocks
2. `src/pyvider/protocols/tfprotov6/handlers/get_metadata.py` - Ruff auto-fixes
3. `src/pyvider/capabilities/decorators.py` - Type annotations
4. `src/pyvider/functions/base.py` - `CtyType[object]` generics
5. `src/pyvider/functions/adapters.py` - `CtyType[object]` generics
6. `src/pyvider/conversion/utils.py` - `CtyType[object]` generics

**Key Design Decision:**
- **Used `object` instead of `Any`** for CtyType generic parameters
- **Why:** Better type safety (preserves checking), consistent with `CtyDynamic = CtyType[object]` from pyvider-cty
- **Pattern:** Changed all `CtyType` → `CtyType[object]` in validators and type inference functions
- **Result:** Strategic `# type: ignore[return-value]` comments for covariance issues with concrete types

---

## Phase 2: Enhanced Error Messages

### Objective
Add rich, actionable error messages with suggestions and context throughout the codebase.

### Current State Analysis

**Exception Hierarchy (Well-Structured):**
- ✅ Inherits from Foundation errors (`FoundationError`, `FoundationValidationError`, etc.)
- ✅ Foundation errors support `context: dict[str, Any]` parameter
- ✅ Existing errors include contextual info (schema_name, function_name, resource_type)
- ✅ 86 exception raises throughout codebase
- ❌ **Missing:** Actionable suggestions/remediation steps
- ❌ **Missing:** Consistent formatting pattern

**Foundation Error Signature:**
```python
def __init__(self, message: str, *,
             code: str | None = None,
             context: dict[str, Any] | None = None,
             cause: Exception | None = None,
             **extra_context: Any) -> None
```

### Enhancement Pattern

**Before:**
```python
raise ResourceError("Invalid configuration")
```

**After:**
```python
raise ResourceError(
    "Invalid configuration for resource 'mycloud_server'",
    context={
        "resource_type": "mycloud_server",
        "attribute": "port",
        "value": 70000,
        "valid_range": "1-65535",
        "suggestion": "Set 'port' to a value between 1 and 65535. Current value 70000 is outside the valid range.",
        "docs_url": "https://docs.pyvider.io/resources/mycloud_server#port"
    }
)
```

### Target Files (Priority Order)

#### 1. `src/pyvider/resources/base.py` (Highest Priority)
**Lines to enhance:**
- Line 98: `raise TypeError(f"Could not create '{target_cls.__name__}' from data: {e}")`
  - Add suggestion about checking required vs optional fields
  - Include field names that are missing
  - Link to resource schema documentation

**Enhancement example:**
```python
raise TypeError(
    f"Could not create '{target_cls.__name__}' instance from configuration data",
    context={
        "class_name": target_cls.__name__,
        "error": str(e),
        "suggestion": "Ensure all required fields are provided and have valid types. Check the resource schema for required vs optional fields.",
        "docs_url": f"https://docs.pyvider.io/resources/{target_cls.__name__.lower()}"
    }
) from e
```

#### 2. `src/pyvider/schema/types/attribute.py`
**What to enhance:**
- Attribute validation errors
- Type mismatch errors
- Required field errors

**Enhancement pattern:**
```python
raise AttributeValidationError(
    f"Invalid value for attribute '{attr_name}'",
    attribute_name=attr_name,
    context={
        "expected_type": expected_type,
        "received_type": type(value).__name__,
        "received_value": repr(value),
        "suggestion": f"Expected a {expected_type}, but received {type(value).__name__}. Convert the value to the correct type.",
        "example": f"{attr_name} = {example_value}"
    }
)
```

#### 3. `src/pyvider/providers/base.py`
**What to enhance:**
- Provider configuration errors
- Provider initialization errors
- Missing required configuration

**Enhancement pattern:**
```python
raise ProviderConfigurationError(
    f"Missing required configuration for provider '{provider_name}'",
    context={
        "provider": provider_name,
        "missing_fields": ["api_key", "region"],
        "suggestion": "Set the required provider configuration in your Terraform configuration block. Example:\n\nprovider \"myprovider\" {\n  api_key = \"your-key\"\n  region  = \"us-west-2\"\n}",
        "docs_url": "https://docs.pyvider.io/providers/configuration"
    }
)
```

#### 4. `src/pyvider/cli/provide_command.py`
**What to enhance:**
- CLI argument errors
- Provider startup errors
- Plugin communication errors

**Current coverage:** 14% (54 lines uncovered)

**Enhancement pattern:**
```python
raise ProviderInitializationError(
    "Failed to start provider service",
    context={
        "command": " ".join(cmd),
        "error": str(e),
        "suggestion": "Check that the provider binary is executable and compatible with your platform. Run 'pyvider --version' to verify installation.",
        "troubleshooting_steps": [
            "Verify provider binary exists and has execute permissions",
            "Check Python version compatibility (requires 3.11+)",
            "Review logs for additional error details"
        ]
    }
) from e
```

#### 5. `src/pyvider/protocols/tfprotov6/handlers/*.py`
**What to enhance:**
- Protocol-level errors (GetMetadata, ValidateResourceConfig, etc.)
- gRPC communication errors
- Terraform compatibility errors

**Files to update:**
- `get_metadata.py`
- `validate_resource_config.py`
- `apply_resource_change.py`
- `plan_resource_change.py`

**Enhancement pattern:**
```python
return pb.GetMetadata.Response(
    diagnostics=[
        pb.Diagnostic(
            severity=pb.Diagnostic.ERROR,
            summary="GetMetadata error",
            detail=f"Failed to discover provider metadata: {str(e)}\n\nSuggestion: Ensure all resources and data sources are properly registered using @resource and @data_source decorators.\n\nContext: {context_info}"
        )
    ]
)
```

### Error Message Templates

Create standardized templates for common error scenarios:

**1. Validation Errors:**
```python
VALIDATION_ERROR_TEMPLATE = """
Invalid {entity_type} '{entity_name}': {error_message}

Expected: {expected}
Received: {received}

Suggestion: {suggestion}

Documentation: {docs_url}
"""
```

**2. Configuration Errors:**
```python
CONFIGURATION_ERROR_TEMPLATE = """
Configuration error in {component_type} '{component_name}': {error_message}

Missing: {missing_fields}
Invalid: {invalid_fields}

Suggestion: {suggestion}

Example:
{example_config}
"""
```

**3. Lifecycle Errors:**
```python
LIFECYCLE_ERROR_TEMPLATE = """
{operation} failed for resource '{resource_type}': {error_message}

Resource State: {current_state}
Attempted Operation: {operation}

Suggestion: {suggestion}

Troubleshooting:
{troubleshooting_steps}
"""
```

### Implementation Checklist

- [ ] Update `src/pyvider/resources/base.py` (5-10 error sites)
- [ ] Update `src/pyvider/schema/types/attribute.py` (10-15 error sites)
- [ ] Update `src/pyvider/providers/base.py` (5-10 error sites)
- [ ] Update `src/pyvider/cli/provide_command.py` (10-15 error sites)
- [ ] Update protocol handlers (15-20 error sites)
- [ ] Add error message templates module (optional)
- [ ] Update tests to verify enhanced error messages
- [ ] Update documentation with error handling guide

**Estimated Impact:** 50-70 enhanced error messages across 5 critical modules

---

## Phase 3: Improved Logging

### Objective
Add strategic logging with correlation IDs, performance metrics, and better context.

### Current State Analysis

**Logging Coverage:**
- ✅ 180 log statements across 43 files
- ✅ Using `provide.foundation.logger`
- ❌ **Missing:** Correlation IDs for operation tracking
- ❌ **Missing:** Performance metrics (duration_ms, operation counts)
- ❌ **Missing:** Strategic logging in provider lifecycle
- ❌ **Missing:** Consistent structured fields

**Foundation Logger Features:**
```python
from provide.foundation import logger

logger.debug("message", field1=value1, field2=value2)
logger.info("message", **context_dict)
logger.warning("message", error=exception)
logger.error("message", exc_info=True)
```

### Enhancement Pattern

**Before:**
```python
logger.debug(f"Discovered resource: {resource_name}")
```

**After:**
```python
logger.debug(
    "Resource discovered during metadata collection",
    operation="get_metadata",
    resource_type=resource_name,
    correlation_id=ctx.correlation_id,
    discovery_source="hub_registry",
    total_resources=resource_count
)
```

### Structured Logging Standards

**Consistent Fields Across All Logs:**

```python
# Resource operations
logger.info(
    "Resource operation completed",
    operation="create",           # create/read/update/delete
    resource_type="mycloud_server",
    resource_id="i-abc123",
    correlation_id="req-xyz",
    duration_ms=250,
    success=True
)

# Provider lifecycle
logger.info(
    "Provider initialization started",
    operation="provider_init",
    provider_name="mycloud",
    correlation_id="init-xyz",
    timestamp=datetime.utcnow().isoformat()
)

# Errors
logger.error(
    "Resource operation failed",
    operation="create",
    resource_type="mycloud_server",
    correlation_id="req-xyz",
    error_code="INVALID_CONFIG",
    error_message=str(e),
    exc_info=True
)

# Performance
logger.debug(
    "API call completed",
    operation="api_call",
    api_endpoint="/servers/create",
    correlation_id="req-xyz",
    duration_ms=150,
    status_code=200
)
```

### Correlation ID Pattern

**Add correlation ID generation:**

```python
# In context/operation initialization
import uuid

correlation_id = str(uuid.uuid4())[:8]  # Short correlation ID

# Pass through context
ctx.correlation_id = correlation_id

# Use in all related logs
logger.info("Operation started", correlation_id=correlation_id)
logger.debug("Step 1", correlation_id=correlation_id)
logger.info("Operation completed", correlation_id=correlation_id)
```

**Files to update:**
1. `src/pyvider/resources/context.py` - Add correlation_id field
2. All handler files - Pass correlation_id through
3. All operation logs - Include correlation_id

### Target Areas for New Logs

#### 1. Provider Lifecycle (10-15 new logs)
**File:** `src/pyvider/cli/provide_command.py`

```python
logger.info("Provider service starting",
            provider_name=provider_name,
            correlation_id=startup_id)

logger.debug("gRPC server binding",
             host=host, port=port,
             correlation_id=startup_id)

logger.info("Provider service ready",
            correlation_id=startup_id,
            startup_duration_ms=duration)

logger.info("Provider service shutting down",
            correlation_id=shutdown_id)
```

#### 2. Schema Operations (15-20 new logs)
**Files:** `src/pyvider/schema/factory.py`, `src/pyvider/schema/types/attribute.py`

```python
logger.debug("Schema building started",
             operation="build_schema",
             resource_type=resource_type,
             correlation_id=correlation_id)

logger.debug("Attribute validation",
             operation="validate_attribute",
             attribute_name=name,
             attribute_type=type_name,
             correlation_id=correlation_id)

logger.info("Schema validation completed",
            operation="validate_schema",
            resource_type=resource_type,
            duration_ms=duration,
            success=True,
            correlation_id=correlation_id)
```

#### 3. State Management (10-15 new logs)
**Files:** `src/pyvider/resources/protocol.py`, `src/pyvider/resources/private_state.py`

```python
logger.debug("State transition",
             operation="state_change",
             resource_type=resource_type,
             from_state=old_state,
             to_state=new_state,
             correlation_id=correlation_id)

logger.debug("Private state encryption",
             operation="encrypt_state",
             resource_type=resource_type,
             state_size_bytes=len(data),
             correlation_id=correlation_id)
```

#### 4. Configuration Loading (10 new logs)
**Files:** Provider and resource initialization

```python
logger.debug("Configuration loaded",
             operation="load_config",
             config_keys=list(config.keys()),
             correlation_id=correlation_id)

logger.warning("Using default configuration",
               operation="load_config",
               missing_keys=missing,
               correlation_id=correlation_id)
```

#### 5. Error Recovery (5-10 new logs)
**Files:** Exception handlers throughout

```python
logger.warning("Recoverable error, retrying",
               operation="api_call",
               error=str(e),
               retry_count=retry,
               max_retries=max_retries,
               correlation_id=correlation_id)

logger.info("Recovery successful",
            operation="retry",
            attempts=retry_count,
            correlation_id=correlation_id)
```

#### 6. Performance Bottlenecks (15-20 new logs)
**Files:** Critical path operations

```python
logger.debug("Schema conversion started",
             operation="convert_schema",
             correlation_id=correlation_id,
             start_time=time.perf_counter())

logger.debug("Schema conversion completed",
             operation="convert_schema",
             correlation_id=correlation_id,
             duration_ms=duration,
             attribute_count=len(attributes))
```

### Sensitive Data Masking

**Audit and mask sensitive data:**

```python
# Before
logger.debug(f"API key: {api_key}")  # ❌ NEVER LOG SECRETS

# After
logger.debug("Authentication configured",
             api_key_present=bool(api_key),  # ✅ Log presence, not value
             api_key_prefix=api_key[:4] if api_key else None)  # ✅ Safe prefix

# Patterns to mask
SENSITIVE_PATTERNS = [
    "api_key", "secret", "password", "token",
    "private_key", "credential", "auth"
]

def mask_sensitive(data: dict) -> dict:
    """Mask sensitive fields in log data."""
    masked = {}
    for key, value in data.items():
        if any(pattern in key.lower() for pattern in SENSITIVE_PATTERNS):
            masked[key] = "***REDACTED***"
        else:
            masked[key] = value
    return masked
```

### Log Levels Clarification

**DEBUG:** Implementation details, data flow
```python
logger.debug("Converting CTY value to native type",
             cty_type=type_name, native_type=target_type)
```

**INFO:** Important state changes, operations
```python
logger.info("Resource created successfully",
            resource_type=resource_type, resource_id=resource_id)
```

**WARNING:** Recoverable issues, deprecations
```python
logger.warning("Using deprecated field 'old_name', use 'new_name' instead",
               field="old_name", replacement="new_name")
```

**ERROR:** Failures requiring attention
```python
logger.error("Resource creation failed",
             resource_type=resource_type, error=str(e), exc_info=True)
```

### Implementation Checklist

- [ ] Add correlation_id to ResourceContext
- [ ] Add correlation_id generation in handlers
- [ ] Add 10-15 provider lifecycle logs
- [ ] Add 15-20 schema operation logs
- [ ] Add 10-15 state management logs
- [ ] Add 10 configuration loading logs
- [ ] Add 5-10 error recovery logs
- [ ] Add 15-20 performance tracking logs
- [ ] Implement sensitive data masking
- [ ] Audit all existing log statements
- [ ] Update log levels for consistency
- [ ] Add log aggregation documentation

**Estimated Impact:** 70+ new strategic log points (180 → 250+)

---

## Testing Strategy

### Phase 2 Testing (Error Messages)

**Verify enhanced errors:**
```python
def test_enhanced_resource_error():
    """Verify resource errors include suggestions."""
    with pytest.raises(ResourceError) as exc_info:
        # Trigger error condition
        resource.create(invalid_config)

    error = exc_info.value
    assert "suggestion" in error.context
    assert "docs_url" in error.context
    assert len(error.context["suggestion"]) > 0
```

**Test error message quality:**
- [ ] All errors include actionable suggestions
- [ ] Context dicts contain relevant debugging info
- [ ] Error messages are user-friendly (not just technical)
- [ ] Documentation links are valid

### Phase 3 Testing (Logging)

**Verify correlation IDs:**
```python
def test_correlation_id_propagation(caplog):
    """Verify correlation ID appears in all related logs."""
    with caplog.at_level(logging.DEBUG):
        resource.create(config)

    logs = [record for record in caplog.records]
    correlation_ids = [r.correlation_id for r in logs if hasattr(r, 'correlation_id')]

    # All logs should have same correlation ID
    assert len(set(correlation_ids)) == 1
    assert len(correlation_ids) > 5  # Multiple log points
```

**Verify structured logging:**
```python
def test_structured_log_fields(caplog):
    """Verify logs contain required structured fields."""
    with caplog.at_level(logging.INFO):
        resource.create(config)

    for record in caplog.records:
        if record.levelname == "INFO":
            assert hasattr(record, 'operation')
            assert hasattr(record, 'correlation_id')
            if 'duration' in record.message:
                assert hasattr(record, 'duration_ms')
```

**Verify sensitive data masking:**
```python
def test_no_secrets_in_logs(caplog):
    """Verify sensitive data never appears in logs."""
    config_with_secrets = {
        "api_key": "super-secret-key",
        "password": "my-password"
    }

    with caplog.at_level(logging.DEBUG):
        provider.configure(config_with_secrets)

    log_text = "\n".join(record.message for record in caplog.records)
    assert "super-secret-key" not in log_text
    assert "my-password" not in log_text
```

---

## Success Metrics

### Phase 2: Enhanced Error Messages

**Quantitative:**
- ✅ 50+ error sites enhanced with suggestions
- ✅ 100% of errors include context dict
- ✅ 95%+ of errors have actionable suggestions
- ✅ All errors link to documentation (where applicable)

**Qualitative:**
- ✅ Users can understand what went wrong
- ✅ Users know how to fix the issue
- ✅ Error messages guide users to correct solution

### Phase 3: Improved Logging

**Quantitative:**
- ✅ 250+ strategic log points (from 180)
- ✅ 100% correlation ID coverage for operations
- ✅ 0 sensitive data in logs
- ✅ All operations log duration_ms

**Qualitative:**
- ✅ Can trace operations across async calls
- ✅ Can identify performance bottlenecks
- ✅ Can debug issues from logs alone
- ✅ Logs provide operational visibility

---

## Command Reference

### Run Tests
```bash
# All tests
uv run pytest

# Specific test file
uv run pytest tests/tfprotov6/handlers/test_get_metadata.py

# With coverage
uv run pytest --cov=pyvider --cov-report=term-missing
```

### Code Quality
```bash
# Format code
uv run ruff format src/ tests/

# Lint code
uv run ruff check src/ tests/

# Auto-fix linting
uv run ruff check src/ tests/ --fix

# Type checking
uv run mypy src/pyvider
```

### Development
```bash
# Install dependencies
uv sync

# Run provider locally (for testing)
pyvider provide
```

---

## Notes & Context

### Important Constraints
- **Do NOT update files in virtual environments** (per CLAUDE.md)
- **Python 3.11+ required** (moving from 3.12+ for compatibility)
- **Use `uv` for all package management**
- **Auto-committer is enabled** - Changes are committed automatically

### Architecture Context
- **Hub-based discovery:** Components self-register via decorators (`@provider`, `@resource`, `@data_source`, `@function`)
- **Protocol layer:** `protocols/tfprotov6/` implements Terraform Plugin Protocol v6
- **Schema system:** `schema/` provides type-safe data modeling using attrs
- **State management:** Private state encrypted via `common/encryption.py`

### Key Files Reference
- Exception hierarchy: `src/pyvider/exceptions/`
- Resource base: `src/pyvider/resources/base.py`
- Schema types: `src/pyvider/schema/types/`
- Protocol handlers: `src/pyvider/protocols/tfprotov6/handlers/`
- Provider base: `src/pyvider/providers/base.py`

### Documentation
- Main docs: `docs/` (organized in clean named folders)
- Build docs: `mkdocs serve` or `mkdocs build`
- Check links: `python scripts/check_doc_links.py`

---

## Getting Started with Phases 2-3

### Quick Start
```bash
# 1. Verify Phase 1 is complete
uv run pytest  # Should show 1,187 passing
uv run ruff check src/pyvider  # Should show "All checks passed!"
uv run mypy src/pyvider/capabilities src/pyvider/functions src/pyvider/conversion  # Should show 0 errors

# 2. Start with Phase 2 - Enhanced Error Messages
# Begin with: src/pyvider/resources/base.py (highest priority)

# 3. Run tests after each file
uv run pytest tests/resources/ -v

# 4. Verify error enhancements
uv run pytest tests/ -k "error" -v
```

### Suggested Order
1. **Phase 2.1:** Enhance `resources/base.py` errors (1-2 hours)
2. **Phase 2.2:** Enhance `schema/types/attribute.py` errors (1 hour)
3. **Phase 2.3:** Enhance `providers/base.py` errors (1 hour)
4. **Phase 2.4:** Enhance `cli/provide_command.py` errors (1 hour)
5. **Phase 2.5:** Enhance protocol handler errors (1 hour)
6. **Phase 3.1:** Add correlation IDs to ResourceContext (30 min)
7. **Phase 3.2:** Add provider lifecycle logs (1 hour)
8. **Phase 3.3:** Add schema operation logs (1 hour)
9. **Phase 3.4:** Add state management logs (1 hour)
10. **Phase 3.5:** Add performance tracking logs (1 hour)

**Total Estimated Time:** 10-12 hours

---

## Questions or Blockers?

If you encounter issues:

1. **Check the tests:** `uv run pytest -xvs` for detailed output
2. **Check Foundation docs:** Foundation errors have rich features
3. **Review existing patterns:** Look at `exceptions/function.py` for good examples
4. **Use structured logging:** Foundation logger supports keyword arguments
5. **Ask for clarification:** Better to ask than assume

---

**This handoff document contains everything needed to continue Phases 2 and 3. Good luck! 🚀**
