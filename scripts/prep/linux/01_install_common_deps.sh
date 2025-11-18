#!/bin/bash
set -ex
echo "Checking and installing common dependencies..."

if ! command -v sudo &> /dev/null; then
    echo "Error: sudo command not found. Please run as root or ensure sudo is installed." >&2
    exit 1
fi

sudo apt-get update -y -qq
packages=("curl" "gnupg" "git" "python3" "python3-pip" "python3-venv" "build-essential" "lsb-release" "software-properties-common")
install_list=()
for pkg in "${packages[@]}"; do
    if ! dpkg -s "$pkg" >/dev/null 2>&1; then
        install_list+=("$pkg")
    fi
done

if [ ${#install_list[@]} -gt 0 ]; then
    echo "Installing missing dependencies: ${install_list[*]}"
    sudo apt-get install -y -qq "${install_list[@]}"
fi
