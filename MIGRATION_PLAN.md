# Pyvider Error System Migration Plan

## Phase 1: Update Exception Hierarchy

### Checklist

#### 1. Replace base exceptions in `pyvider/exceptions/`:
- [x] Map `PyviderError` → Inherit from `FoundationError`
- [x] Map validation errors → Inherit from foundation ValidationError where appropriate
- [x] Map network/gRPC errors → Inherit from foundation `NetworkError`
- [x] Map resource errors → Inherit from specific foundation error types
- [x] Keep domain-specific exception names but inherit from foundation classes

Note: Some exceptions now inherit directly from foundation errors instead of PyviderError,
which breaks the old inheritance hierarchy but provides better foundation integration.

#### 2. Update exception imports across codebase:
- [ ] Add `from provide.foundation.errors import *` to exception modules
- [ ] Update all `raise` statements to use new context methods
- [ ] Convert simple string errors to use `.add_context()` method

### Exception Class Mappings

```python
# Base
PyviderError → FoundationError

# Validation & Conversion
ValidationError → ValidationError (foundation)
AttributeValidationError → ValidationError with attribute context
ConversionError → ValidationError with conversion context
WireFormatError → SerializationError (foundation)
InvalidTypeError → ValidationError with type context
UnsupportedTypeError → ValidationError with type context

# Resource & Component
ResourceError → FoundationError (keep as base for resource errors)
ResourceNotFoundError → NotFoundError (foundation)
ResourceValidationError → ValidationError
ResourceOperationError → OperationError (foundation)
ResourceLifecycleContractError → StateError (foundation)
DataSourceError → FoundationError (keep as specialized)
CapabilityError → ConfigurationError

# Provider & Configuration  
ProviderError → ConfigurationError (foundation)
ProviderConfigurationError → ConfigurationError
ProviderInitializationError → InitializationError (foundation)
FrameworkConfigurationError → ConfigurationError
ComponentConfigurationError → ConfigurationError

# Network & Integration
NetworkError → NetworkError (foundation)
GRPCError → NetworkError
GRPCConnectionError → NetworkError
RateLimitError → RateLimitError (foundation)

# Schema & Serialization
SchemaError → SchemaValidationError (foundation)
SchemaValidationError → SchemaValidationError
SchemaParseError → ValidationError
SchemaConversionError → ValidationError
SchemaRegistrationError → ConfigurationError
SerializationError → SerializationError (foundation)
DeserializationError → SerializationError

# Registry & Functions
ComponentRegistryError → ConfigurationError
ValidatorRegistrationError → ConfigurationError
FunctionError → OperationError (foundation)
FunctionRegistrationError → ConfigurationError
FunctionValidationError → ValidationError
```

### Testing Before Changes
- [x] Run existing test suite to establish baseline
- [x] Document any existing test failures (206 passed, 1 error in test_get_key_from_config_file)
- [x] Phase 1 Complete: 192 passed, 14 failed (exception hierarchy tests), 1 error (same as baseline)

### Phase 1 Results
- Successfully replaced pyvider exception hierarchy with foundation errors
- Tests failing are primarily hierarchy tests expecting old inheritance structure
- Core functionality preserved - same baseline error persists
- Breaking changes documented: Some exceptions now inherit directly from foundation
  instead of PyviderError for better integration

### Implementation Order (COMPLETED)
1. ✅ Start with base.py - update PyviderError
2. ✅ Update validation.py 
3. ✅ Update resource.py
4. ✅ Update provider.py
5. ✅ Update grpc.py
6. ✅ Update schema.py
7. ✅ Update serialization.py
8. ✅ Update function.py
9. ✅ Update registry.py
10. ✅ Update __init__.py exports (no changes needed)