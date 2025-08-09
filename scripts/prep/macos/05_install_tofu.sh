#!/bin/bash
set -e
echo "Checking and installing OpenTofu..."
if ! command -v tofu &> /dev/null; then
    brew install opentofu
fi
brew upgrade opentofu


# 🐍🏗️📄🪄
