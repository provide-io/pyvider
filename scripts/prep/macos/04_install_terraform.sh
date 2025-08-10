#!/bin/bash
set -e
echo "Checking and installing HashiCorp Terraform..."
if ! command -v terraform &> /dev/null; then
    brew tap hashicorp/tap
    brew install hashicorp/tap/terraform
fi
brew upgrade hashicorp/tap/terraform
