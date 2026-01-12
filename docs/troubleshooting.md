# Troubleshooting Common Issues

This guide provides solutions to common problems you may encounter when developing or using Pyvider providers. Each issue includes symptoms, root causes, and step-by-step solutions.

## Quick Problem Finder

| Symptom | Likely Cause | Jump To |
|---------|--------------|---------|
| Provider binary not found | Installation or PATH issue | [Provider Not Found](#provider-not-found-error) |
| Schema validation errors | Config/schema mismatch | [Invalid Configuration](#invalid-provider-configuration-error) |
| Resource not created | Logic error in _create | [Resource Not Created](#resource-not-created) |
| State drift not detected | read() not implemented correctly | [State Drift Issues](#state-drift-not-detected) |
| Provider crashes | Unhandled exception | [Provider Crashes](#provider-crashes-on-apply) |
| Slow performance | Blocking I/O | [Performance Issues](#slow-performance) |
| Import fails | Import ID format wrong | [Import Failures](#import-failures) |
| "Plugin did not respond" | Timeout or crash | [Plugin Timeout](#plugin-did-not-respond) |

## Installation and Setup Issues

### Provider Not Found Error

**Symptom:**
```
Error: Could not load plugin

Plugin reinitialization required. Please run "terraform init".
```

**Root Causes:**
1. Provider not installed
2. Provider not in correct directory
3. Provider not executable
4. Wrong provider name in configuration

**Solutions:**

**1. Verify installation:**
```bash
# Check if provider is installed
uv run python -c "import importlib.metadata as m; print(m.version('pyvider'))"

# Reinstall if needed
uv pip install -e .
```

**2. Check Terraform plugin directory:**
```bash
# List installed providers
ls -la ~/.terraform.d/plugins/

# Or check local .terraform directory
ls -la .terraform/providers/
```

**3. Verify provider is executable:**
```bash
# Make provider executable
chmod +x ~/.terraform.d/plugins/terraform-provider-pyvider

# Test provider directly
./terraform-provider-pyvider --help
```

**4. Check Terraform configuration:**
```hcl
terraform {
  required_providers {
    my_provider = {
      source  = "example.com/acme/my-provider"  # Match your package namespace
      version = "~> 0.1"
    }
  }
}
```

**5. Run terraform init:**
```bash
terraform init
```

### Invalid Provider Configuration Error

**Symptom:**
```
Error: Invalid provider configuration

Provider "pyvider" requires configuration.
```

**Root Causes:**
1. Missing required provider configuration
2. Schema mismatch between config and provider
3. Invalid attribute values
4. Type mismatch

**Solutions:**

**1. Check provider schema:**
```bash
# See what configuration is required
terraform providers schema -json | jq '.provider_schemas."example.com/acme/my-provider"'
```

**2. Verify provider configuration block:**
```hcl
provider "my_provider" {
  # Add any required configuration your provider expects
  api_endpoint = "https://api.example.com"
  api_key      = var.api_key
}
```

**3. Check attribute types:**
```hcl
# Wrong: String instead of number
provider "my_provider" {
  timeout = "30"  # Should be: timeout = 30
}

# Correct: Number
provider "my_provider" {
  timeout = 30
}
```

**4. Enable debug logging to see details:**
```bash
export TF_LOG=DEBUG
terraform plan
```

### Python Version Mismatch

**Symptom:**
```
Error: Plugin exited before it could be initialized
```

**Root Cause:**
Provider requires Python 3.11+ but wrong version installed

**Solution:**

```bash
# Check Python version
python --version

# Should be 3.11 or higher
# If not, install correct version:
brew install python@3.11  # macOS
apt-get install python3.11  # Ubuntu

# Recreate virtual environment
uv venv --python 3.11
source .venv/bin/activate
uv pip install -e .
```

## Resource Lifecycle Issues

### Resource Not Created

**Symptom:**
- `terraform apply` succeeds without errors
- Resource doesn't actually exist
- State shows resource as created

**Root Causes:**
1. _create() returns success but doesn't actually create
2. Exception is swallowed
3. Async operation not awaited
4. API call fails silently

**Solutions:**

**1. Add logging to _create_apply:**
```python
async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
    logger.debug("_create_apply called", config=ctx.config)

    try:
        result = await self.api.create_resource(ctx.config)
        logger.info("Resource created", resource_id=result.id)
        return State(id=result.id, **ctx.config.__dict__), None
    except Exception as e:
        logger.error("Create failed", error=str(e))
        raise  # Don't swallow the exception!
```

**2. Verify the operation is actually called:**
```bash
export PYVIDER_LOG_LEVEL=DEBUG
terraform apply
# Look for "_create called" in logs
```

**3. Check for missing await:**
```python
# Wrong: Not awaiting async operation
async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
    result = self.api.create_resource(ctx.config)  # Missing await!
    return result, None

# Correct: Await the operation
async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
    result = await self.api.create_resource(ctx.config)
    return result, None
```

**4. Verify resource actually exists:**
```python
async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
    # Create the resource
    result = await self.api.create_resource(ctx.config)

    # Verify it was created
    verification = await self.api.get_resource(result.id)
    if not verification:
        raise ResourceError(f"Resource {result.id} not found after creation")

    return State(id=result.id, **ctx.config.__dict__), None
```

### State Drift Not Detected

**Symptom:**
- Manually change resource outside Terraform
- `terraform plan` shows no changes
- Drift is not detected

**Root Causes:**
1. read() not implemented
2. read() returns cached state instead of current state
3. read() returns wrong values
4. Computed attributes not updated

**Solutions:**

**1. Implement read() correctly:**
```python
async def read(self, ctx: ResourceContext) -> State | None:
    """Must fetch CURRENT state, not return cached state."""

    # Get the resource ID from state
    resource_id = ctx.state.id

    # Fetch CURRENT state from actual resource
    current = await self.api.get_resource(resource_id)

    # Return None if resource doesn't exist (was deleted)
    if not current:
        logger.debug("Resource not found, returning None", resource_id=resource_id)
        return None

    # Return CURRENT state, not ctx.state!
    return State(
        id=current.id,
        name=current.name,
        value=current.value,
        # Update all attributes from current state
    )
```

**2. Don't return cached state:**
```python
# Wrong: Returning stored state
async def read(self, ctx: ResourceContext):
    return ctx.state  # This is cached, not current!

# Correct: Fetch current state
async def read(self, ctx: ResourceContext):
    current = await self._fetch_current_state(ctx.state.id)
    return current
```

**3. Test drift detection manually:**
```bash
# Create resource
terraform apply

# Modify resource outside Terraform
# (Edit file, change API value, etc.)

# Should show drift
terraform plan
```

**4. Add logging to compare states:**
```python
async def read(self, ctx: ResourceContext):
    current = await self._fetch_current_state()

    logger.debug(
        "State comparison",
        stored_state=ctx.state.__dict__,
        current_state=current.__dict__
    )

    return current
```

### Resource Update Not Applied

**Symptom:**
- Change configuration in Terraform
- `terraform apply` succeeds
- Resource not actually updated

**Root Cause:**
_update() not implemented or not working correctly

**Solution:**

**1. Implement _update_apply():**
```python
async def _update_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
    """Update must modify the actual resource."""

    logger.debug(
        "Updating resource",
        resource_id=ctx.state.id,
        changes=ctx.config
    )

    # Actually update the resource
    await self.api.update_resource(ctx.state.id, ctx.config)

    # Return updated state
    return State(id=ctx.state.id, **ctx.config.__dict__), None
```

**2. Verify update is called:**
```bash
export PYVIDER_LOG_LEVEL=DEBUG
terraform apply
# Look for "Updating resource" in logs
```

**3. Check which attributes can be updated:**
```python
async def _update_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
    # Determine what changed
    changes = {}
    for key in ctx.config.__dict__:
        new_value = getattr(ctx.config, key, None)
        old_value = getattr(ctx.state, key, None)
        if old_value != new_value:
            changes[key] = {"old": old_value, "new": new_value}

    logger.debug("Detected changes", changes=changes)

    # Some attributes might require resource replacement
    if "immutable_field" in changes:
        raise ResourceError(
            "Cannot update immutable_field, resource must be recreated"
        )

    await self.api.update_resource(ctx.state.id, ctx.config)
    return State(id=ctx.state.id, **ctx.config.__dict__), None
```

### Resource Delete Fails

**Symptom:**
```
Error: Error deleting resource
```

**Root Causes:**
1. Resource already deleted
2. Permission denied
3. Resource has dependencies
4. API error

**Solutions:**

**1. Handle already-deleted resources:**
```python
async def _delete_apply(self, ctx: ResourceContext) -> None:
    """Delete should be idempotent."""

    try:
        await self.api.delete_resource(ctx.state.id)
        logger.info("Resource deleted", resource_id=ctx.state.id)
    except ResourceNotFoundError:
        # Already deleted - this is OK
        logger.debug("Resource already deleted", resource_id=ctx.state.id)
        return
    except PermissionError as e:
        raise ResourceError(f"Permission denied deleting resource: {e}")
    except Exception as e:
        logger.error("Delete failed", error=str(e))
        raise
```

**2. Check for dependencies:**
```python
async def _delete_apply(self, ctx: ResourceContext) -> None:
    # Check if resource has dependencies
    dependencies = await self.api.get_dependencies(ctx.state.id)

    if dependencies:
        raise ResourceError(
            f"Cannot delete resource {ctx.state.id}, it has dependencies: "
            f"{', '.join(d.id for d in dependencies)}. "
            f"Delete dependent resources first."
        )

    await self.api.delete_resource(ctx.state.id)
```

## Schema and Validation Issues

### Schema Validation Errors

**Symptom:**
```
Error: Missing required argument

The argument "filename" is required, but no definition was found.
```

**Root Causes:**
1. Missing required attribute in configuration
2. Schema mismatch between provider and Terraform config
3. Attribute name typo

**Solutions:**

**1. Check schema definition:**
```python
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "filename": a_str(required=True),  # This MUST be in config
        "content": a_str(required=True),
    })
```

**2. Verify Terraform configuration has all required attributes:**
```hcl
resource "pyvider_file_content" "example" {
  filename = "/tmp/test.txt"  # Required
  content  = "test content"    # Required
}
```

**3. Check attribute names match exactly:**
```python
# Schema says "filename"
"filename": a_str(required=True)

# Config must use "filename" (not "file_name" or "file")
resource "pyvider_file_content" "example" {
  filename = "/tmp/test.txt"  # Must match schema exactly
}
```

### Type Mismatch Errors

**Symptom:**
```
Error: Incorrect attribute value type

Inappropriate value for attribute "port": a number is required.
```

**Root Cause:**
Wrong type in Terraform configuration

**Solution:**

```hcl
# Wrong: String instead of number
resource "pyvider_example" "test" {
  port = "8080"  # Wrong type
}

# Correct: Number
resource "pyvider_example" "test" {
  port = 8080  # Correct type
}

# Wrong: Number instead of boolean
resource "pyvider_example" "test" {
  enabled = 1  # Wrong type
}

# Correct: Boolean
resource "pyvider_example" "test" {
  enabled = true  # Correct type
}
```

### Computed Attribute Errors

**Symptom:**
```
Error: Computed attributes cannot be set
```

**Root Cause:**
Trying to set a computed attribute in configuration

**Solution:**

```python
# In schema, mark attribute as computed
@classmethod
def get_schema(cls) -> PvsSchema:
    return s_resource({
        "filename": a_str(required=True),
        "content": a_str(required=True),
        "content_hash": a_str(computed=True),  # Computed, not set by user
    })
```

```hcl
# Wrong: Setting computed attribute
resource "pyvider_file_content" "example" {
  filename     = "/tmp/test.txt"
  content      = "test"
  content_hash = "abc123"  # Error! This is computed
}

# Correct: Don't set computed attributes
resource "pyvider_file_content" "example" {
  filename = "/tmp/test.txt"
  content  = "test"
  # content_hash will be computed by provider
}
```

## Performance Issues

### Slow Performance

**Symptom:**
- Operations take very long
- Terraform appears to hang
- Resources timeout

**Root Causes:**
1. Blocking I/O in async code
2. No timeout on HTTP requests
3. Inefficient API calls (N+1 problem)
4. Large state data

**Solutions:**

**1. Find blocking operations:**
```python
# Wrong: Blocking I/O
async def read(self, ctx: ResourceContext):
    import time
    time.sleep(10)  # BLOCKS entire event loop!

    import requests
    response = requests.get(url)  # BLOCKS!

# Correct: Async I/O
async def read(self, ctx: ResourceContext):
    await asyncio.sleep(10)  # Non-blocking

    async with httpx.AsyncClient() as client:
        response = await client.get(url)  # Non-blocking
```

**2. Add timeouts:**
```python
class MyProvider(BaseProvider):
    async def configure(self, config: ProviderConfig):
        self.http_client = httpx.AsyncClient(
            timeout=30.0  # 30 second timeout
        )
```

**3. Batch API calls:**
```python
# Wrong: N+1 query problem
async def read_multiple(self, resource_ids: list):
    results = []
    for rid in resource_ids:
        result = await self.api.get_resource(rid)  # N API calls!
        results.append(result)
    return results

# Correct: Single batch call
async def read_multiple(self, resource_ids: list):
    return await self.api.batch_get_resources(resource_ids)  # 1 API call
```

**4. Profile to find bottlenecks:**
```bash
# Install py-spy
uv tool install py-spy

# Profile provider
py-spy top --pid $(pgrep -f terraform-provider-pyvider)
```

### Memory Issues

**Symptom:**
- Provider consumes excessive memory
- Out of memory errors

**Root Causes:**
1. Loading large files into memory
2. Memory leaks
3. Caching too much data

**Solutions:**

**1. Stream large files:**
```python
# Wrong: Load entire file
async def process_file(self, path: Path):
    content = path.read_bytes()  # Entire file in memory!
    return hashlib.sha256(content).hexdigest()

# Correct: Stream the file
async def process_file(self, path: Path):
    hash_obj = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()
```

**2. Check for memory leaks:**
```python
import tracemalloc

tracemalloc.start()

# ... run operations ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:
    print(stat)
```

## Import Failures

### Import Not Working

**Symptom:**
```
Error: Import not found

Resource pyvider_file_content.example was not found.
```

**Root Causes:**
1. Import ID format incorrect
2. Import not implemented
3. Resource doesn't exist

**Solutions:**

**1. Implement import in resource:**
```python
@register_resource("pyvider_file_content")
class FileContentResource(BaseResource):

    async def import_resource(self, import_id: str) -> tuple[dict, None]:
        """
        Import existing resource by ID.

        Args:
            import_id: Resource identifier (e.g., file path)

        Returns:
            (state_dict, None)
        """
        path = Path(import_id)

        if not path.is_file():
            raise ResourceNotFoundError(f"File not found: {import_id}")

        content = path.read_text()
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        return {
            "filename": import_id,
            "content": content,
            "exists": True,
            "content_hash": content_hash,
        }, None
```

**2. Use correct import ID format:**
```bash
# Import with correct ID format
terraform import pyvider_file_content.example /path/to/file.txt
```

**3. Check import ID in Terraform:**
```hcl
# Configuration-based import
import {
  to = pyvider_file_content.example
  id = "/path/to/file.txt"  # Must match import_resource expectations
}

resource "pyvider_file_content" "example" {
  filename = "/path/to/file.txt"
  content  = file("/path/to/file.txt")
}
```

## Error Messages and Crashes

### Plugin Did Not Respond

**Symptom:**
```
Error: Plugin did not respond

The plugin encountered an error, and failed to respond to the
plugin.(*GRPCProvider).ApplyResourceChange call.
```

**Root Causes:**
1. Provider crashed
2. Operation timeout
3. Deadlock or infinite loop

**Solutions:**

**1. Check logs for stack trace:**
```bash
export TF_LOG=DEBUG
export PYVIDER_LOG_LEVEL=DEBUG
terraform apply 2>&1 | tee debug.log

# Look for "Traceback" in logs
grep -A 20 "Traceback" debug.log
```

**2. Add error handling:**
```python
async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
    try:
        result = await self.api.create_resource(ctx.config)
        return State(**result.__dict__), None
    except Exception as e:
        logger.error(
            "Create failed with exception",
            error=str(e),
            error_type=type(e).__name__,
            traceback=traceback.format_exc()
        )
        raise
```

**3. Check for infinite loops:**
```python
# Wrong: Infinite loop
async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
    while True:
        await self.api.check_status()  # Never exits!

# Correct: With timeout/limit
async def _create_apply(self, ctx: ResourceContext) -> tuple[State | None, None]:
    max_attempts = 10
    for attempt in range(max_attempts):
        if await self.api.check_status():
            break
        await asyncio.sleep(1)
    else:
        raise TimeoutError("Operation timed out after 10 attempts")

    result = await self.api.create_resource(ctx.config)
    return State(**result.__dict__), None
```

### Provider Crashes on Apply

**Symptom:**
Provider process exits unexpectedly

**Solutions:**

See [Debugging Guide - Provider Crashes](guides/development/debugging.md#scenario-3-provider-crashes-on-apply) for detailed workflow.

## Getting Help

If you're still experiencing issues after trying these solutions:

### 1. Enable Full Debug Logging

```bash
export TF_LOG=TRACE
export TF_LOG_PATH=./terraform-debug.log
export PYVIDER_LOG_LEVEL=DEBUG
terraform apply
```

### 2. Gather Information

When creating an issue, include:

- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Pyvider version**: `uv run python -c "import importlib.metadata as m; print(m.version('pyvider'))"`
- **Terraform version**: `terraform version`
- **Python version**: `python --version`
- **Relevant logs** from debug output
- **Minimal config** that reproduces the issue

### 3. Create a GitHub Issue

Visit [https://github.com/provide-io/pyvider/issues](https://github.com/provide-io/pyvider/issues) and create a new issue with the information above.

### 4. Search Existing Issues

Before creating a new issue:
- Search [existing issues](https://github.com/provide-io/pyvider/issues)
- Check [GitHub Discussions](https://github.com/provide-io/pyvider/discussions)
- Review the [Debugging Guide](guides/development/debugging.md)
- Check [Best Practices](guides/production/best-practices.md) for common patterns
- Look at [Pyvider Components](https://github.com/provide-io/pyvider-components) for working examples

## Related Documentation

- [Debugging Guide](guides/development/debugging.md) - Interactive debugging techniques
- [Best Practices](guides/production/best-practices.md) - Patterns that prevent issues
- [Error Handling](guides/development/error-handling.md) - Exception handling
- [Security Best Practices](guides/production/security-best-practices.md) - Security troubleshooting
- [Performance Optimization](guides/production/performance-optimization.md) - Performance troubleshooting
- [Logging](guides/development/logging.md) - Structured logging
- [Testing Providers](guides/development/testing-providers.md) - Testing strategies

---

**Remember**: Most issues can be quickly diagnosed with debug logging enabled. Start with `TF_LOG=DEBUG` and `PYVIDER_LOG_LEVEL=DEBUG` to see what's actually happening.

**See Also**:
- For security-related issues, consult the [Security Best Practices Guide](guides/production/security-best-practices.md)
- For performance problems, see the [Performance Optimization Guide](guides/production/performance-optimization.md)
- For general provider patterns, check [Best Practices](guides/production/best-practices.md)
