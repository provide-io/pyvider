# Mutmut Usage Guide

## Overview
Mutmut is configured to work **without stats collection**, which means:
- ✅ Generates 1944+ mutations successfully
- ❌ Can't auto-detect which tests to run per mutant
- ✅ Still useful for manual code quality spot-checking

## Manual Workflow

### 1. Browse Available Mutants
```bash
# See all mutants
python run_mutmut.py results

# Count by status
python run_mutmut.py results | wc -l
```

### 2. Inspect Specific Mutant
```bash
# View what changed in a mutant
python run_mutmut.py show <mutant-id>

# Example:
python run_mutmut.py show pyvider.protocols.tfprotov6.handlers.validate_data_resource_config.x__validate_data_resource_config_impl__mutmut_1
```

### 3. Apply Mutant & Test Manually
```bash
# Apply a specific mutant to your code
python run_mutmut.py apply <mutant-id>

# Run tests to see if they catch it
uv run pytest tests/tfprotov6/handlers/

# Revert the change
git checkout src/pyvider/protocols/tfprotov6/handlers/
```

### 4. Find Mutants in Specific Files
```bash
# Filter by file
python run_mutmut.py results | grep "handlers.validate"

# Show mutations for a specific handler
python run_mutmut.py results | grep "read_data_source"
```

## Common Patterns

### Spot-Check New Code
When you write new code, manually check a few mutants:

1. Find mutants for your new file
2. Apply 3-5 interesting mutations
3. Run tests to verify they fail
4. If tests pass → write better tests!

### Review Critical Code
For security/critical paths:

1. List all mutants for that file
2. Apply each mutation one by one
3. Ensure tests catch every mutation
4. Document any intentionally untested mutations

### Example Session
```bash
# 1. Find mutants in a critical file
python run_mutmut.py results | grep "configure_provider"

# 2. Pick an interesting one (like changing response = X to None)
python run_mutmut.py show pyvider.protocols.tfprotov6.handlers.configure_provider.x__configure_provider_impl__mutmut_5

# 3. Apply it
python run_mutmut.py apply pyvider.protocols.tfprotov6.handlers.configure_provider.x__configure_provider_impl__mutmut_5

# 4. Run tests
uv run pytest tests/tfprotov6/handlers/test_configure_provider.py -v

# 5. Revert
git checkout src/pyvider/protocols/tfprotov6/handlers/configure_provider.py
```

## Tips

- **Focus on critical paths** - authentication, validation, error handling
- **Look for "None" mutations** - these often reveal missing null checks
- **Check boundary conditions** - mutations changing `<` to `<=`, `+` to `-`
- **Review error handling** - mutations removing try/except or raising different errors

## Files Location

- Wrapper script: `run_mutmut.py`
- Config: `.mutmut-config.py` and `pyproject.toml`
- Mutants directory: `mutants/` (symlinked to `/tmp/pyvider-mutants/`)
- Cache: `.mutmut-cache` (database of mutation results)

## Limitations

- No automatic "killed vs survived" detection per mutant
- Must manually apply and test each mutation
- Stats collection disabled (avoids import conflicts)
- All mutants show as "no tests" in results

## Re-running Mutation Generation

To regenerate all mutants (if you change code):

```bash
# Clear cache and regenerate
rm -rf .mutmut-cache mutants/
python run_mutmut.py run
```

This will regenerate the mutation list but won't auto-test them.
