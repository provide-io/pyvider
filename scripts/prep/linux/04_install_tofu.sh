#!/bin/bash
set -ex
echo "Checking and installing OpenTofu..."
if command -v tofu >/dev/null 2>&1; then
    echo "OpenTofu is already installed: $(tofu version)"
    exit 0
fi
echo "Installing OpenTofu..."
curl --proto '=https' --tlsv1.2 -fsSL https://get.opentofu.org/install-opentofu.sh -o /tmp/install-opentofu.sh
sh /tmp/install-opentofu.sh --install-method deb
rm /tmp/install-opentofu.sh


# 🐍🏗️📄🪄
