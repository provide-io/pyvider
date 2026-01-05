# Debugging Pyvider Providers

This guide provides comprehensive debugging techniques and workflows for troubleshooting Pyvider providers. Whether you're tracking down a subtle bug or dealing with a complete failure, these strategies will help you identify and fix issues quickly.

## Table of Contents

- [Why Provider Debugging is Different](#why-provider-debugging-is-different)
- [Quick Reference](#quick-reference)
- [Setting Up Your Debug Environment](#setting-up-your-debug-environment)
- [Log-Based Debugging](#log-based-debugging)

---

## Why Provider Debugging is Different

Debugging Terraform providers presents unique challenges:

- **Process separation**: Provider runs as a separate process from Terraform
- **gRPC communication**: Terraform communicates with providers via gRPC protocol
- **Async operations**: Most provider code is async, requiring special debugging techniques
- **State management**: Issues can involve complex state transitions
- **Limited feedback**: Terraform's output may not show full provider errors

## Quick Reference

| Problem | Best Debugging Approach | Section |
|---------|------------------------|---------|
| Logic errors, wrong behavior | Python debugger (`breakpoint()`) | [Interactive Debugging](#interactive-debugging-with-python-debugger) |
| Provider crashes | Terraform logs (`TF_LOG=DEBUG`) | [Debugging with Terraform](#debugging-with-terraform) |
| API/HTTP issues | httpx logging | [Network Debugging](#network-and-api-debugging) |
| Slow performance | Logging with timing, py-spy | [Performance Debugging](#performance-debugging) |
| Schema errors | Minimal config testing | [Schema Debugging](#debugging-schema-problems) |
| State inconsistencies | State inspection, logs | [State Debugging](#debugging-state-issues) |

## Setting Up Your Debug Environment

### Development Environment

Set up your environment for effective debugging:

```bash
# Install in editable mode
cd /path/to/pyvider-provider
uv pip install -e .

# Set debug environment variables
export PYVIDER_LOG_LEVEL=DEBUG
export TF_LOG=DEBUG
export TF_LOG_PATH=./terraform-debug.log
```

### IDE Configuration

**VS Code** (`launch.json`):
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Provider",
      "type": "python",
      "request": "launch",
      "module": "pyvider.cli",
      "args": ["provide"],
      "env": {
        "PYVIDER_LOG_LEVEL": "DEBUG",
        "TF_LOG": "DEBUG"
      },
      "justMyCode": false
    }
  ]
}
```

**PyCharm**:
1. Run → Edit Configurations → Add Python configuration
2. Module: `pyvider.cli`
3. Parameters: `provide`
4. Environment variables: `PYVIDER_LOG_LEVEL=DEBUG;TF_LOG=DEBUG`

### Required Tools

```bash
# Debugging tools
uv add ipdb # Enhanced debugger
uv add # Performance profiler
uv tool install py-spy

# System tools (macOS)
brew install httpie  # HTTP testing

# System tools (Linux)
apt-get install strace  # System call tracing
```

## Log-Based Debugging

### Understanding Log Levels

Pyvider uses structured logging with multiple levels:

```python
# In your provider code
from provide.foundation import logger

logger.debug("Detailed debugging information")  # Development
logger.info("Important state changes")  # Normal operations
logger.warning("Recoverable issues")  # Potential problems
logger.error("Failures requiring attention")  # Errors
```

### Setting Log Levels

```bash
# Provider log level
export PYVIDER_LOG_LEVEL=DEBUG

# Terraform log level
export TF_LOG=TRACE  # Most verbose
export TF_LOG=DEBUG  # Detailed
export TF_LOG=INFO   # Normal
```

### Reading Structured Logs

Pyvider logs are structured with key-value pairs:

```
2025-10-24 10:30:15 DEBUG Read file content filename=/tmp/test.txt content_length=42 content_hash=a1b2c3d4
```

**Key fields to look for:**
- `filename`, `path` - What file is being accessed
- `resource_type`, `resource_id` - Which resource
- `operation` - What operation (create, read, update, delete)
- `error` - Error messages
- `content_hash`, `content_length` - Data verification

### Filtering Logs

```bash
# Show only ERROR logs
grep "ERROR" terraform-debug.log

# Show logs for specific resource
grep "pyvider_file_content" terraform-debug.log

# Show specific operation
grep "operation=create" terraform-debug.log

# Show logs with timing
grep "duration" terraform-debug.log
```

### Example: Debugging with Logs

```python
@register_resource("pyvider_example")
class ExampleResource(BaseResource):

    async def _create(self, ctx: ResourceContext, base_plan: dict):
        logger.debug(
            "Create operation starting",
            resource_class=self.__class__.__name__,
            config=base_plan
        )

        try:
            result = await self.api.create_resource(base_plan)

            logger.debug(
                "Resource created successfully",
                resource_id=result.id,
                duration_ms=result.duration
            )

            return {**base_plan, "id": result.id}, None

        except Exception as e:
            logger.error(
                "Failed to create resource",
                error=str(e),
                error_type=type(e).__name__,
                config=base_plan
            )
            raise
```

## Interactive Debugging with Python Debugger

### Using breakpoint()

The simplest way to debug is using Python's built-in `breakpoint()`:

```python
async def _create(self, ctx: ResourceContext, base_plan: dict):
    # Pause execution here
    breakpoint()

    # Inspect variables
    # (Pdb) print(base_plan)
    # (Pdb) print(ctx.config)
    # (Pdb) print(ctx.state)

    result = await self.api.create_resource(base_plan)
    return result, None
```

### Debugger Commands

When paused at a breakpoint:

```python
# Navigation
n  # Next line
s  # Step into function
c  # Continue execution
r  # Return from current function

# Inspection
p variable_name  # Print variable
pp variable_name  # Pretty-print variable
l  # List code around current line
w  # Show stack trace

# Breakpoints
b line_number  # Set breakpoint at line
b function_name  # Set breakpoint at function
cl  # Clear all breakpoints

# Other
h  # Help
q  # Quit debugger
```

### Debugging Async Code

Special considerations for async debugging:

```python
async def _create(self, ctx: ResourceContext, base_plan: dict):
    # Set breakpoint before await
    breakpoint()

    # When you hit this breakpoint, you can:
    # - Step over the await with 'n'
    # - Step into the async function with 's'
    result = await self.api.create_resource(base_plan)

    # Set another breakpoint to inspect result
    breakpoint()
    return result, None
```

### Conditional Breakpoints

Break only when a condition is met:

```python
async def read(self, ctx: ResourceContext):
    filename = ctx.state.filename

    # Only break for specific files
    if filename == "/tmp/debug-this.txt":
        breakpoint()

    content = safe_read_text(Path(filename))
    return FileContentState(...)
```

### Inspecting Context

When debugging, inspect the resource context:

```python
# At breakpoint
breakpoint()

# Inspect configuration
(Pdb) pp ctx.config.__dict__
{'filename': '/tmp/test.txt', 'content': 'Hello'}

# Inspect state (if exists)
(Pdb) pp ctx.state.__dict__ if ctx.state else "No state"
{'filename': '/tmp/test.txt', 'content': 'Hello', 'exists': True}

# Check if field is unknown during planning
(Pdb) print(ctx.is_field_unknown('content'))
False

# Check private state
(Pdb) print(ctx.private_state)
None
```

## Debugging with Terraform

### Terraform Log Levels

```bash
# TRACE: Maximum verbosity (includes gRPC)
export TF_LOG=TRACE

# DEBUG: Detailed information
export TF_LOG=DEBUG

# INFO: High-level information
export TF_LOG=INFO

# Save logs to file
export TF_LOG_PATH=./terraform.log

# Run Terraform
terraform apply
```

### Understanding Terraform Debug Output

Key patterns to look for:

```
# Provider startup
[DEBUG] plugin: starting plugin: path=.terraform/plugins/...

# gRPC communication
[TRACE] provider.terraform-provider-pyvider: Received request: ...

# Schema retrieval
[DEBUG] plugin: plugin process exited: ...

# Resource operations
[DEBUG] pyvider_file_content.example: apply started
[DEBUG] pyvider_file_content.example: apply complete
```

### Common Terraform Errors

**"Plugin did not respond"**
```
Error: Failed to instantiate provider

The plugin encountered an error, and failed to respond to the plugin.(*GRPCProvider).ReadResource call.
```

**Cause**: Provider crashed or hung

**Debug steps:**
1. Check provider logs for stack trace
2. Verify async operations aren't blocking
3. Add `breakpoint()` before failure point

**"Schema inconsistency"**
```
Error: Inconsistent result after apply

When applying changes to pyvider_file_content.example, provider produced an unexpected new value
```

**Cause**: State returned doesn't match schema

**Debug steps:**
1. Log the state being returned
2. Verify all computed attributes are set
3. Check for type mismatches

### Debugging Provider Communication

Watch gRPC communication:

```bash
# Maximum verbosity for gRPC
export TF_LOG=TRACE
export GRPC_GO_LOG_VERBOSITY_LEVEL=99
export GRPC_GO_LOG_SEVERITY_LEVEL=info

terraform apply 2>&1 | grep -i "grpc"
```

## Common Debugging Scenarios

### Scenario 1: "My resource isn't being created"

**Symptoms**: `terraform apply` completes but resource doesn't exist

**Debug workflow:**

1. **Check Terraform output for errors**
   ```bash
   terraform apply 2>&1 | grep -i error
   ```

2. **Enable debug logging**
   ```bash
   export TF_LOG=DEBUG
   export PYVIDER_LOG_LEVEL=DEBUG
   terraform apply
   ```

3. **Add logging to _create method**
   ```python
   async def _create(self, ctx: ResourceContext, base_plan: dict):
       logger.debug("_create called", config=base_plan)
       breakpoint()  # Pause to inspect
       # ... rest of method
   ```

4. **Verify the operation is called**
   - Check logs for "_create called"
   - If not called, check schema/config

5. **Test with minimal config**
   ```hcl
   resource "pyvider_file_content" "test" {
     filename = "/tmp/test.txt"
     content  = "test"
   }
   ```

6. **Check for swallowed exceptions**
   ```python
   try:
       result = await self.api.create(...)
   except Exception as e:
       logger.error("Create failed", error=str(e))
       raise  # Don't swallow!
   ```

### Scenario 2: "State drift isn't detected"

**Symptoms**: Manual changes not detected by `terraform plan`

**Debug workflow:**

1. **Check read() implementation**
   ```python
   async def read(self, ctx: ResourceContext):
       logger.debug("read() called", state=ctx.state.__dict__)
       # Should return None if resource doesn't exist
       # Should return updated state if changed
   ```

2. **Verify read() returns correct state**
   ```python
   async def read(self, ctx: ResourceContext):
       current = await self.fetch_current_state()

       logger.debug(
           "Comparing states",
           terraform_state=ctx.state.__dict__,
           current_state=current.__dict__
       )

       return current
   ```

3. **Test manually**
   ```bash
   # Create resource
   terraform apply

   # Modify manually
   echo "changed" > /tmp/test.txt

   # Should show drift
   terraform plan
   ```

### Scenario 3: "Provider crashes on apply"

**Symptoms**: Provider process exits unexpectedly

**Debug workflow:**

1. **Find the stack trace**
   ```bash
   # Check Terraform logs
   cat terraform.log | grep -A 20 "Traceback"

   # Check provider logs
   export PYVIDER_LOG_LEVEL=DEBUG
   terraform apply 2>&1 | grep -B 5 -A 20 "Error"
   ```

2. **Identify the failing method**
   ```python
   # Add try/except with logging
   async def _create(self, ctx: ResourceContext, base_plan: dict):
       try:
           logger.debug("Starting create")
           result = await self.api.create(...)
           logger.debug("Create succeeded")
           return result, None
       except Exception as e:
           logger.error("Create failed", error=str(e), traceback=True)
           raise
   ```

3. **Use debugger to catch exception**
   ```python
   import sys
   sys.settrace(lambda *args: None)  # Enable full tracebacks

   async def _create(self, ctx: ResourceContext, base_plan: dict):
       breakpoint()  # Will stop before crash
       result = await self.api.create(...)
       return result, None
   ```

### Scenario 4: "Slow performance / hangs"

**Symptoms**: Operations take very long or hang indefinitely

**Debug workflow:**

1. **Add timing logs**
   ```python
   import time

   async def _create(self, ctx: ResourceContext, base_plan: dict):
       start = time.time()
       logger.debug("Create starting")

       result = await self.api.create(...)

       duration = time.time() - start
       logger.debug("Create completed", duration_seconds=duration)
       return result, None
   ```

2. **Check for blocking operations**
   ```python
   # Bad: Blocking in async function
   async def read(self, ctx: ResourceContext):
       import time
       time.sleep(10)  # BLOCKS entire event loop!

   # Good: Use async sleep
   async def read(self, ctx: ResourceContext):
       await asyncio.sleep(10)
   ```

3. **Profile with py-spy**
   ```bash
   # Find provider process
   ps aux | grep terraform-provider-pyvider

   # Profile it
   py-spy top --pid <provider_pid>

   # Generate flamegraph
   py-spy record --pid <provider_pid> --output profile.svg
   ```

4. **Check for connection issues**
   ```python
   # Add timeout to HTTP clients
   self.http_client = httpx.AsyncClient(timeout=30.0)
   ```

### Scenario 5: "Schema validation errors"

**Symptoms**: "Attribute not found" or type errors

**Debug workflow:**

1. **Compare schema to config**
   ```python
   @classmethod
   def get_schema(cls) -> PvsSchema:
       schema = s_resource({
           "filename": a_str(required=True),  # Must match Terraform
           "content": a_str(required=True),
       })
       logger.debug("Schema defined", attributes=list(schema.attributes.keys()))
       return schema
   ```

2. **Test with minimal config**
   ```hcl
   # Start simple
   resource "pyvider_file_content" "test" {
     filename = "/tmp/test.txt"
     content  = "test"
   }

   # Add attributes one at a time
   ```

3. **Validate attribute names match**
   ```python
   # In _create, log what you received
   async def _create(self, ctx: ResourceContext, base_plan: dict):
       logger.debug("Received attributes", attributes=list(base_plan.keys()))
       # Should match schema exactly
   ```

## Debugging State Issues

### Inspecting Terraform State

```bash
# Show entire state
terraform show

# Show specific resource
terraform show -json | jq '.values.root_module.resources[] | select(.address=="pyvider_file_content.test")'

# Show state file directly
cat terraform.tfstate | jq '.resources[]'
```

### Understanding State Transitions

```python
async def _update(self, ctx: ResourceContext, base_plan: dict):
    logger.debug(
        "State transition",
        old_state=ctx.state.__dict__ if ctx.state else None,
        new_plan=base_plan,
        differences=self._compute_diff(ctx.state, base_plan)
    )

    result = await self.api.update(...)
    return result, None

def _compute_diff(self, old, new):
    """Helper to show what changed."""
    if not old:
        return "creating"
    changes = {}
    for key in new:
        if getattr(old, key, None) != new[key]:
            changes[key] = {"old": getattr(old, key), "new": new[key]}
    return changes
```

### Debugging Private State

```python
from pyvider.resources import PrivateState

async def read(self, ctx: ResourceContext):
    # Decrypt and inspect private state
    if ctx.private_state:
        try:
            decrypted = PrivateState.decrypt(ctx.private_state)
            logger.debug("Private state contents", data=decrypted)
        except Exception as e:
            logger.error("Failed to decrypt private state", error=str(e))

    return current_state
```

### State Inconsistency Debugging

```python
async def _create(self, ctx: ResourceContext, base_plan: dict):
    result = await self.api.create(...)

    # Return state must include ALL attributes from schema
    state = {
        **base_plan,  # Include all config
        "id": result.id,
        "exists": True,  # Computed attribute
        "content_hash": self._compute_hash(base_plan["content"]),  # Computed
    }

    # Log for verification
    logger.debug(
        "Returning state",
        state_keys=list(state.keys()),
        schema_attrs=list(self.get_schema().attributes.keys())
    )

    return state, None
```

## Debugging Schema Problems

### Validating Schema Definition

```python
@classmethod
def get_schema(cls) -> PvsSchema:
    schema = s_resource({
        "filename": a_str(
            required=True,
            description="Path to the file",
            validators=[
                lambda x: not x.startswith("/") or "Use relative paths"
            ]
        ),
        "content": a_str(required=True),
        "exists": a_bool(computed=True),
    })

    # Debug: Print schema
    logger.debug("Schema created", attributes={
        k: {"required": v.required, "computed": v.computed}
        for k, v in schema.attributes.items()
    })

    return schema
```

### Testing Schema with Terraform

```hcl
# Test required attributes
resource "pyvider_file_content" "test_required" {
  # Missing required attribute - should error
  filename = "/tmp/test.txt"
  # content missing!
}

# Test computed attributes
resource "pyvider_file_content" "test_computed" {
  filename = "/tmp/test.txt"
  content  = "test"
  # Don't set computed attributes
  # exists = true  # This should error
}
```

### Type Conversion Debugging

```python
async def _create(self, ctx: ResourceContext, base_plan: dict):
    # Log types received
    logger.debug("Received types", types={
        k: type(v).__name__ for k, v in base_plan.items()
    })

    # Verify types match schema
    if not isinstance(base_plan.get("filename"), str):
        logger.error("filename is not string!", type=type(base_plan["filename"]))

    return base_plan, None
```

## Performance Debugging

### Measuring Operation Times

```python
import time
from functools import wraps

def timed(operation_name):
    """Decorator to time operations."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start
                logger.debug(
                    f"{operation_name} completed",
                    duration_ms=int(duration * 1000)
                )
                return result
            except Exception as e:
                duration = time.time() - start
                logger.error(
                    f"{operation_name} failed",
                    duration_ms=int(duration * 1000),
                    error=str(e)
                )
                raise
        return wrapper
    return decorator

@register_resource("pyvider_example")
class ExampleResource(BaseResource):

    @timed("read")
    async def read(self, ctx: ResourceContext):
        return await self._fetch_state()

    @timed("create")
    async def _create(self, ctx: ResourceContext, base_plan: dict):
        return await self._do_create(base_plan)
```

### Profiling with py-spy

```bash
# Real-time profiling
py-spy top --pid $(pgrep -f terraform-provider-pyvider)

# Generate flame graph
py-spy record -o profile.svg --pid $(pgrep -f terraform-provider-pyvider)

# Record for specific duration
py-spy record -o profile.svg --duration 60 --pid <pid>
```

### Finding Memory Leaks

```python
import tracemalloc

class MyProvider(BaseProvider):

    async def configure(self, config: ProviderConfig):
        # Start tracking
        tracemalloc.start()

    async def cleanup(self):
        # Get memory statistics
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')

        logger.debug("Memory usage top 10:")
        for stat in top_stats[:10]:
            logger.debug(f"{stat}")
```

## Network and API Debugging

### HTTP Request Logging

```python
import httpx

class MyProvider(BaseProvider):

    async def configure(self, config: ProviderConfig):
        # Enable HTTP logging
        self.http_client = httpx.AsyncClient(
            event_hooks={
                "request": [self._log_request],
                "response": [self._log_response],
            }
        )

    async def _log_request(self, request):
        logger.debug(
            "HTTP request",
            method=request.method,
            url=str(request.url),
            headers=dict(request.headers)
        )

    async def _log_response(self, response):
        logger.debug(
            "HTTP response",
            status=response.status_code,
            duration_ms=response.elapsed.total_seconds() * 1000
        )
```

### Capturing HTTP Traffic

```bash
# Using mitmproxy
mitmproxy --mode transparent

# Or charles proxy
charles-proxy

# Configure provider to use proxy
export HTTP_PROXY=http://localhost:8080
export HTTPS_PROXY=http://localhost:8080
```

### Testing API Calls Separately

```python
# Test API calls outside Terraform
import asyncio
import httpx

async def test_api():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.example.com/resource",
            json={"name": "test"}
        )
        print(response.status_code)
        print(response.json())

asyncio.run(test_api())
```

## Debugging Tests

### Running Tests in Debug Mode

```bash
# Run with debugger
pytest tests/test_my_resource.py --pdb

# Stop at first failure
pytest tests/ -x --pdb

# Verbose output
pytest tests/ -vv

# Show print statements
pytest tests/ -s
```

### Debugging Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_create():
    resource = FileContentResource()

    # Add breakpoint
    breakpoint()

    # Step through async code
    result = await resource._create(ctx, plan)

    assert result is not None
```

### Using pytest Fixtures for Debugging

```python
@pytest.fixture
def debug_ctx(capsys):
    """Fixture that prints context for debugging."""
    def _debug(ctx):
        print(f"\nContext: {ctx.__dict__}")
        print(f"Config: {ctx.config.__dict__ if ctx.config else None}")
        print(f"State: {ctx.state.__dict__ if ctx.state else None}")
    return _debug

async def test_with_debug(debug_ctx):
    ctx = make_context(...)
    debug_ctx(ctx)  # Print for inspection

    result = await resource.read(ctx)
    assert result is not None
```

## Advanced Debugging Techniques

### System Call Tracing

```bash
# macOS
sudo dtruss -p $(pgrep -f terraform-provider-pyvider)

# Linux
strace -p $(pgrep -f terraform-provider-pyvider)

# Follow child processes
strace -f -p <pid>

# Filter for file operations
strace -e trace=open,read,write -p <pid>
```

### gRPC Inspection

```bash
# Install grpcurl
brew install grpcurl  # macOS
apt-get install grpcurl  # Linux

# List services
grpcurl -plaintext localhost:50051 list

# Call method directly
grpcurl -plaintext -d '{"resource_type":"pyvider_file_content"}' \
  localhost:50051 tfplugin6.Provider/GetSchema
```

### Thread Debugging

```python
import threading

def debug_threads():
    """Print all active threads."""
    for thread in threading.enumerate():
        logger.debug(
            "Active thread",
            name=thread.name,
            daemon=thread.daemon,
            alive=thread.is_alive()
        )

# Call when debugging hangs
debug_threads()
```

## Debugging Tools Reference

| Problem Type | Tool | Command/Usage |
|--------------|------|---------------|
| Logic errors | Python debugger | `breakpoint()` in code |
| Async issues | ipdb | `import ipdb; ipdb.set_trace()` |
| Terraform communication | TF_LOG | `export TF_LOG=DEBUG` |
| HTTP/API issues | httpx logging | Enable event hooks |
| Performance | py-spy | `py-spy top --pid <pid>` |
| Memory leaks | tracemalloc | `tracemalloc.start()` |
| System calls | strace/dtruss | `strace -p <pid>` |
| gRPC inspection | grpcurl | `grpcurl localhost:50051 list` |
| Network traffic | mitmproxy | `mitmproxy` |
| Test failures | pytest --pdb | `pytest --pdb -x` |

## Common Error Messages Decoded

### "Plugin did not respond"
**Meaning**: Provider process crashed or hung
**Check**: Stack traces in logs, blocking operations, infinite loops

### "Schema inconsistency"
**Meaning**: State doesn't match schema definition
**Check**: All computed attributes set, types match, no extra fields

### "Attribute not found in schema"
**Meaning**: Config references undefined attribute
**Check**: Attribute names in schema vs Terraform config

### "Context deadline exceeded"
**Meaning**: Operation timed out
**Check**: Blocking I/O, slow API calls, infinite loops

### "Could not load plugin"
**Meaning**: Provider binary not found or not executable
**Check**: Installation, file permissions, PATH

## Debugging Checklist

When troubleshooting an issue, work through this checklist systematically:

- [ ] **Enable debug logging**: `export TF_LOG=DEBUG PYVIDER_LOG_LEVEL=DEBUG`
- [ ] **Check Terraform output**: Look for obvious errors
- [ ] **Review provider logs**: Check for exceptions and warnings
- [ ] **Verify schema**: Ensure schema matches Terraform config
- [ ] **Test with minimal config**: Simplify to isolate the issue
- [ ] **Add logging**: Instrument the failing operation
- [ ] **Use breakpoints**: Step through the code if needed
- [ ] **Check async operations**: Ensure no blocking I/O
- [ ] **Verify state handling**: Check state transitions
- [ ] **Test lifecycle individually**: Test create/read/update/delete separately
- [ ] **Check external dependencies**: Test API calls independently
- [ ] **Review test coverage**: Ensure scenario is tested

## Related Documentation

- [Logging Guide](../development/logging.md) - Structured logging details
- [Error Handling](../development/error-handling.md) - Exception handling patterns
- [Testing Providers](../development/testing-providers.md) - Testing strategies
- [Best Practices](../production/best-practices.md) - Avoiding common issues
- [Troubleshooting](../../troubleshooting.md) - Common problems and solutions

## Learn by Debugging

The best way to learn debugging is to practice. Try these exercises:

1. **Add intentional bugs** to pyvider-components examples and practice finding them
2. **Debug existing tests** - Run tests with `--pdb` and explore
3. **Profile operations** - Use py-spy on working code to understand performance
4. **Trace system calls** - Use strace/dtruss to see what your provider actually does

Check out [pyvider-components](https://github.com/provide-io/pyvider-components) for working code to practice with!

---

**Remember**: Debugging is a skill that improves with practice. Start with simple logging, escalate to interactive debugging when needed, and always work systematically from symptoms to root cause.
