#!/bin/bash
#
# env.sh
#
# Standardized development environment setup script for all 'pyvider' packages.
#
# This script uses 'uv' for high-performance virtual environment creation
# and dependency management. It ensures that all related 'pyvider' sibling
# packages are installed in editable mode for a seamless development experience
# across a multi-package project.
#
# Usage: From the root of any pyvider package, run: ./env.sh
#

# --- Configuration and Setup ---

# Use colors for better readability in the terminal.
COLOR_BLUE='\033[0;34m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[0;33m'
COLOR_NC='\033[0m' # No Color

# A small helper function to print formatted section headers.
print_header() {
    echo -e "\n${COLOR_BLUE}--- ${1} ---${COLOR_NC}"
}

# Ensure the script is run from a project root containing pyproject.toml.
if [ ! -f "pyproject.toml" ]; then
    echo -e "${COLOR_YELLOW}⚠️  Warning: 'pyproject.toml' not found.${COLOR_NC}"
    echo "Please run this script from the root directory of a pyvider package."
    exit 1
fi

PROJECT_NAME=$(basename "$(pwd)")
print_header "Setting up environment for '${PROJECT_NAME}'"

# --- 'uv' Installation ---

# Check for 'uv' and install it if it's not present. 'uv' is a modern,
# extremely fast Python package manager from Astral.
if ! command -v uv &> /dev/null; then
    print_header "🚀 Installing 'uv' package manager"
    # The official installer from astral.sh
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # The uv installer places the binary in either ~/.local/bin or ~/.cargo/bin.
    # We must source the corresponding environment file to update the shell's PATH.
    # This logic robustly checks for the correct file before sourcing.
    UV_ENV_PATH_LOCAL="$HOME/.local/bin/env"
    UV_ENV_PATH_CARGO="$HOME/.cargo/env"

    if [ -f "$UV_ENV_PATH_LOCAL" ]; then
        echo "Sourcing environment from '$UV_ENV_PATH_LOCAL' to update PATH..."
        source "$UV_ENV_PATH_LOCAL"
    elif [ -f "$UV_ENV_PATH_CARGO" ]; then
        echo "Sourcing environment from '$UV_ENV_PATH_CARGO' to update PATH..."
        source "$UV_ENV_PATH_CARGO"
    else
        echo -e "${COLOR_YELLOW}⚠️  Warning: Could not find 'uv' environment file to source.${COLOR_NC}"
        echo "Please ensure '$HOME/.local/bin' or '$HOME/.cargo/bin' is in your PATH."
    fi

    echo -e "${COLOR_GREEN}✅ 'uv' installed successfully.${COLOR_NC}"
    uv --version
else
    echo -e "${COLOR_GREEN}✅ 'uv' is already installed.${COLOR_NC}"
    uv --version
fi

# --- Virtual Environment and Dependencies ---

# Detect OS and architecture for platform-specific venv directories
TFOS=$(uname -s | tr '[:upper:]' '[:lower:]')
TFARCH=$(uname -m)
case "$TFARCH" in
    x86_64) TFARCH="amd64" ;;
    aarch64) TFARCH="arm64" ;;
    arm64) TFARCH="arm64" ;;
esac

VENV_DIR=".venv_${TFOS}_${TFARCH}"

# Configure uv to use our platform-specific virtual environment
export UV_PROJECT_ENVIRONMENT="${VENV_DIR}"

print_header "🐍 Creating Python virtual environment with 'uv'"
echo "Using platform-specific venv directory: ${VENV_DIR}"

# Check if venv already exists and is functional
if [ -d "${VENV_DIR}" ] && [ -f "${VENV_DIR}/bin/activate" ] && [ -f "${VENV_DIR}/bin/python" ]; then
    echo -e "${COLOR_GREEN}✅ Virtual environment '${VENV_DIR}' already exists and appears functional.${COLOR_NC}"
else
    echo "Creating new virtual environment at '${VENV_DIR}'..."
    uv venv "${VENV_DIR}"
fi

print_header "🔗 Activating the virtual environment"
# Activation is done before installing dependencies so that any console
# scripts provided by those dependencies are immediately on the PATH.
source "${VENV_DIR}/bin/activate"
echo "Virtual environment activated at '$(pwd)/${VENV_DIR}'"

print_header "📦 Syncing base and development dependencies"
# 'uv sync' is the modern, fast way to install dependencies from pyproject.toml.
# Using --all-groups ensures that optional dependencies, like those for
# testing and linting, are also installed.
# UV_PROJECT_ENVIRONMENT ensures uv uses our platform-specific virtual environment
uv sync --all-groups

print_header "✏️ Installing '${PROJECT_NAME}' in editable mode"
# This allows local source code changes to be reflected immediately without
# needing to reinstall the package. The --no-deps flag prevents re-installing
# dependencies that `uv sync` just handled.
uv pip install --no-deps -e .

# --- Cross-Package Editable Installs ---

print_header "🤝 Installing sibling 'pyvider' packages in editable mode"
# This is the key logic for multi-package development. It ensures that local,
# unpublished changes in one pyvider package are used by others that depend on it.

# Correctly handle the case where we are in '/' and '..' is still '/'
PARENT_DIR=$(dirname "$(pwd)")
if [ "$PARENT_DIR" = "/" ] && [ "$(pwd)" = "/" ]; then
    echo "Running in root directory, skipping sibling search."
else
    for dir in "${PARENT_DIR}"/pyvider*; do
        # Check if the matched item is actually a directory.
        if [ -d "${dir}" ]; then
            SIBLING_PACKAGE_NAME=$(basename "${dir}")
            echo "Found sibling package: '${SIBLING_PACKAGE_NAME}'. Installing in editable mode..."
            # We use --no-deps here for a crucial reason: the main `uv sync` has
            # already resolved and installed the complete dependency graph.
            # This command's only job is to create a "link" (.pth file) to the
            # sibling's source code, effectively overriding the PyPI version.
            if ! uv pip install --no-deps -e "${dir}"; then
                echo -e "${COLOR_YELLOW}⚠️  Warning: Failed to install sibling package '${SIBLING_PACKAGE_NAME}' from '${dir}' in editable mode.${COLOR_NC}"
                echo "Attempting to continue with other packages..."
            fi
        fi
    done
    
    # Special handling for tofusoup - install with dependencies if it exists
    TOFUSOUP_DIR="${PARENT_DIR}/tofusoup"
    if [ -d "${TOFUSOUP_DIR}" ]; then
        echo "Found tofusoup package. Installing in editable mode with dependencies..."
        if ! uv pip install -e "${TOFUSOUP_DIR}"; then
            echo -e "${COLOR_YELLOW}⚠️  Warning: Failed to install tofusoup package from '${TOFUSOUP_DIR}' in editable mode.${COLOR_NC}"
            echo "Attempting to continue..."
        fi
    fi
fi


# --- Finalization ---

print_header "🔧 Configuring PYTHONPATH"
# Prepending the current directory's src and root to PYTHONPATH ensures
# that local modules are resolved correctly, supporting both 'src' and flat layouts.

# Function to deduplicate PATH entries while preserving order
# The first occurrence of each path is preserved, later duplicates are removed
deduplicate_path() {
    local path_to_dedupe="$1"
    local seen_paths=""
    local deduped_path=""
    local current_path=""
    
    # Handle empty input
    if [ -z "$path_to_dedupe" ]; then
        echo ""
        return
    fi
    
    # Split path by colon and process each entry
    # Use a more portable approach than read -ra
    local old_ifs="$IFS"
    IFS=':'
    for current_path in $path_to_dedupe; do
        # Skip empty paths
        if [ -n "$current_path" ]; then
            # Check if we've seen this path before
            case ":$seen_paths:" in
                *":$current_path:"*) 
                    # Already seen, skip (preserves first occurrence)
                    ;;
                *)
                    # Not seen before, add it
                    seen_paths="$seen_paths:$current_path"
                    if [ -z "$deduped_path" ]; then
                        deduped_path="$current_path"
                    else
                        deduped_path="$deduped_path:$current_path"
                    fi
                    ;;
            esac
        fi
    done
    IFS="$old_ifs"
    
    echo "$deduped_path"
}

# Build new PYTHONPATH with current directories first
NEW_PYTHONPATH="${PWD}/src:${PWD}${PYTHONPATH:+:${PYTHONPATH}}"

# Deduplicate the PYTHONPATH to prevent accumulation of duplicate entries
PYTHONPATH_DEDUPED=$(deduplicate_path "$NEW_PYTHONPATH")

export PYTHONPATH="$PYTHONPATH_DEDUPED"

# Also deduplicate PATH to prevent accumulation of duplicate entries
PATH_DEDUPED=$(deduplicate_path "$PATH")
export PATH="$PATH_DEDUPED"
echo "PYTHONPATH set to: ${PYTHONPATH}"

print_header "✅ Environment setup complete!"
echo -e "The '${COLOR_GREEN}${PROJECT_NAME}${COLOR_NC}' development environment is ready."
echo "The virtual environment is active in this shell."
echo "To exit, simply run 'deactivate'."
