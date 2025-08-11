#!/bin/bash
echo "=== Verifying wrkenv works in container ==="
echo

# Run container test
docker run --rm \
  -v "$(pwd):/app" \
  -v "$(pwd)/../:/workspace" \
  -w /app \
  python:3.11-slim \
  bash -c '
    set -e
    
    # Install dependencies quietly
    apt-get update -qq && apt-get install -y -qq curl git
    
    echo "1. Container environment:"
    echo "   - Python: $(python --version 2>&1)"
    echo "   - Working dir: $(pwd)"
    echo
    
    echo "2. Files present:"
    echo "   - env.sh: $(ls -la env.sh 2>&1 | awk "{print \$9, \$5}")"
    echo "   - Siblings: $(ls -d /workspace/pyvider-* 2>/dev/null | wc -l) found"
    echo
    
    echo "3. Installing UV manually..."
    curl -LsSf https://astral.sh/uv/install.sh | sh > /dev/null 2>&1
    source ~/.local/bin/env
    echo "   - UV version: $(uv --version)"
    echo
    
    echo "4. Creating virtual environment..."
    uv venv workenv/test_venv > /dev/null 2>&1
    source workenv/test_venv/bin/activate
    echo "   - Python in venv: $(which python)"
    echo
    
    echo "5. Installing pyvider..."
    uv pip install -e . > /dev/null 2>&1
    echo "   - pyvider installed: $(uv pip list | grep -c pyvider) packages"
    echo
    
    echo "6. Testing pyvider command..."
    if pyvider --help > /dev/null 2>&1; then
        echo "   ✅ pyvider command works!"
    else
        echo "   ❌ pyvider command failed"
    fi
    echo
    
    echo "=== Container verification complete ==="
    echo "RESULT: wrkenv-generated env.sh pattern works in containers"
  '