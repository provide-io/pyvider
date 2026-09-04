#!/usr/bin/env bash
# Drive this checkout of pyvider through OpenTofu with tofusoup's `stir`.
#
# The unit suite exercises pyvider in-process, where a provider that never
# registers a component and a provider that registers it correctly look the
# same. Only a real host asks for one by name. Two defects reached a green PR
# that way: a keyword-only capability parameter that unregistered every
# `component_of=` function, and a plan that Terraform refuses.
#
# `stir` runs each example directory through init -> apply -> plan -> destroy.
# The re-plan is the part worth having: an apply proves the plan could be
# carried out, not that the provider planned everything it then wrote, and a
# value invented during apply leaves a diff that `apply` alone reports as
# success.
#
# No PSP is built. Terraform needs an executable that speaks the plugin
# protocol, and the console script in a venv is one, so this tests the protocol
# without also testing flavorpack's packaging -- which terraform-provider-pyvider
# already covers in its own conformance workflow.
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CORPUS="${TERRAFORM_GATE_CORPUS:-${PROJECT_ROOT}/.terraform-gate/provider/examples}"
VENV="${PROJECT_ROOT}/.terraform-gate/venv"

case "$(uname -s)/$(uname -m)" in
  Linux/x86_64) PLATFORM="linux_amd64" ;;
  Linux/aarch64) PLATFORM="linux_arm64" ;;
  Darwin/arm64) PLATFORM="darwin_arm64" ;;
  Darwin/x86_64) PLATFORM="darwin_amd64" ;;
  *) echo "unsupported platform: $(uname -s)/$(uname -m)" >&2; exit 1 ;;
esac

echo "==> Installing this pyvider plus the components the corpus configures"
uv venv --clear "${VENV}"
# pyvider comes from this checkout so the gate tests the change under review;
# everything else comes from the registry, so a corpus failure is attributable.
VIRTUAL_ENV="${VENV}" uv pip install \
  --editable "${PROJECT_ROOT}" \
  pyvider-components \
  "tofusoup[all]"

echo "==> Publishing the provider where Terraform will look for it"
# `pyvider install` writes a wrapper around whichever venv it detects from the
# project root, which is not this one. Copying the console script is equivalent
# and explicit: its shebang already points at this venv's interpreter, so the
# components installed above are importable, and the name carries the
# "terraform-provider" that pyvider requires in argv[0] before it will serve
# rather than report a detection error (provide_command.py:449-463).
PLUGIN_VERSION="$("${VENV}/bin/python" -c 'import importlib.metadata as m; print(m.version("pyvider"))')"
PLUGIN_DIR="${HOME}/.terraform.d/plugins/local/providers/pyvider/${PLUGIN_VERSION}/${PLATFORM}"
mkdir -p "${PLUGIN_DIR}"
cp "${VENV}/bin/pyvider" "${PLUGIN_DIR}/terraform-provider-pyvider"
chmod +x "${PLUGIN_DIR}/terraform-provider-pyvider"

echo "==> Running the corpus: ${CORPUS}"
# PYVIDER_TESTMODE publishes the components registered `test_only`, which a
# large part of the corpus configures and would otherwise skip.
PYVIDER_TESTMODE=true "${VENV}/bin/soup" stir --recursive "${CORPUS}"
