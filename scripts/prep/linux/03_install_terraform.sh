#!/bin/bash
set -ex
echo "Checking and installing HashiCorp Terraform..."
if command -v terraform >/dev/null 2>&1; then
    echo "Terraform is already installed: $(terraform version)"
    exit 0
fi
echo "Installing Terraform..."
sudo rm -f /etc/apt/sources.list.d/hashicorp.list
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list > /dev/null
sudo apt-get update -y -qq
sudo apt-get install -y terraform


# 🐍🏗️📄🪄
