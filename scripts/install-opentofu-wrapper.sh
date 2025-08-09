#!/bin/bash
#
# OpenTofu Installation Wrapper Script
# Downloads and runs the official installer from https://get.opentofu.org/install-opentofu.sh
#

set -e

# Detect OS
OS=$(uname -s | tr '[:upper:]' '[:lower:]')

# Download and run the official OpenTofu installer
echo "Installing OpenTofu..."
curl --proto '=https' --tlsv1.2 -fsSL https://get.opentofu.org/install-opentofu.sh -o /tmp/install-opentofu.sh

# Make executable
chmod +x /tmp/install-opentofu.sh

# Install based on OS
case "$OS" in
    linux)
        echo "Installing OpenTofu for Linux (deb method)..."
        /tmp/install-opentofu.sh --install-method deb
        ;;
    darwin)
        echo "Installing OpenTofu for macOS (standalone method)..." 
        /tmp/install-opentofu.sh --install-method standalone
        ;;
    *)
        echo "Installing OpenTofu with default method..."
        /tmp/install-opentofu.sh
        ;;
esac

# Clean up
rm -f /tmp/install-opentofu.sh

echo "OpenTofu installation complete!"


# 🐍🏗️📄🪄
