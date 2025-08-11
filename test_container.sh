#!/bin/bash
set -e

echo "=== Testing wrkenv in container ==="
echo

# Create a temporary directory structure similar to our workspace
TEMP_DIR=$(mktemp -d)
echo "Creating workspace in: $TEMP_DIR"

# Copy projects
cp -r /Users/tim/code/gh/provide-io/pyvider "$TEMP_DIR/"
cp -r /Users/tim/code/gh/provide-io/pyvider-* "$TEMP_DIR/"
cp -r /Users/tim/code/gh/provide-io/wrkenv "$TEMP_DIR/"

# Run a docker container with Python 3.11
docker run --rm -it \
  -v "$TEMP_DIR:/workspace" \
  -w /workspace/pyvider \
  python:3.11-slim \
  bash -c '
    echo "=== Container Test Starting ==="
    
    # Install system dependencies
    apt-get update && apt-get install -y git curl > /dev/null 2>&1
    
    # Source env.sh
    echo "Sourcing env.sh..."
    source env.sh
    
    # Test commands
    echo
    echo "Testing pyvider command:"
    pyvider --help | head -5
    
    echo
    echo "Testing pytest:"
    pytest --version
    
    echo
    echo "Running a simple test:"
    pytest tests/common/test_encryption_unit.py::TestEncryptionCore::test_encrypt_decrypt_roundtrip -v
    
    echo
    echo "=== Container Test Complete ==="
  '

# Cleanup
rm -rf "$TEMP_DIR"
echo "Temporary directory cleaned up"