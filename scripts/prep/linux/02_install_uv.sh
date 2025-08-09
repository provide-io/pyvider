#!/bin/bash
set -ex
echo "Checking and installing uv package manager..."
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "Please ensure ~/.local/bin is in your PATH."
fi


# 🐍🏗️📄🪄
