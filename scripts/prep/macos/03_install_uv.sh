#!/bin/bash
set -e
echo "Checking and installing uv package manager..."
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi


# 🐍🏗️📄🪄
