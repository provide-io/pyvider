#!/usr/bin/env bash
# Drive this checkout of pyvider through a real Terraform or OpenTofu with
# tofusoup's `stir`. `TOFUSOUP_TF_COMMAND` picks which; stir's own search order
# prefers OpenTofu, so the engine is named rather than inferred.
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
CORPUS="${TERRAFORM_GATE_CORPUS:-${PROJECT_ROOT}/terraform-gate/provider/examples}"
VENV="${PROJECT_ROOT}/terraform-gate/venv"

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
# PYVIDER_COMPONENTS lets a developer point the gate at a local components
# checkout; CI takes the released package, so a corpus failure is attributable
# to the pyvider under review rather than to unreleased components.
# TOFUSOUP does the same for stir itself, which is what a developer needs to
# try a lifecycle phase before it is released.
VIRTUAL_ENV="${VENV}" uv pip install \
  --editable "${PROJECT_ROOT}" \
  "${PYVIDER_COMPONENTS:-pyvider-components}" \
  "${TOFUSOUP:-tofusoup[all]}"

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

# An empty corpus is the one way this gate can pass while proving nothing, so
# it is checked rather than assumed. stir discovers no directory whose name
# begins with a dot (stir/discovery.py:229), and reports finding nothing by
# exiting 0.
if [ ! -d "${CORPUS}" ]; then
  echo "corpus directory does not exist: ${CORPUS}" >&2
  exit 1
fi
CONFIGURATIONS="$(find "${CORPUS}" -name '*.tf' | wc -l | tr -d ' ')"
if [ "${CONFIGURATIONS}" -eq 0 ]; then
  echo "no .tf configurations under ${CORPUS}; the gate would prove nothing" >&2
  exit 1
fi

TF_BIN="${TOFUSOUP_TF_COMMAND:-$(command -v tofu || command -v terraform || echo tofu)}"

# A list resource is reached only through `terraform query`: no other phase
# evaluates a `list` block, so a provider can ship one Terraform refuses and
# still pass init, apply, plan and destroy. OpenTofu has no query command at
# any version, so this guard binds only on the engine that has one -- where a
# corpus with no query files would prove exactly what the OpenTofu run already
# proved, at twice the cost.
if "${TF_BIN}" query -help >/dev/null 2>&1; then
  QUERIES="$(find "${CORPUS}" -name '*.tfquery.hcl' | wc -l | tr -d ' ')"
  if [ "${QUERIES}" -eq 0 ]; then
    echo "${TF_BIN} can query, but no *.tfquery.hcl under ${CORPUS};" >&2
    echo "no list resource would be exercised and the run would add nothing" >&2
    exit 1
  fi
  echo "==> ${TF_BIN} can query: ${QUERIES} query configurations to exercise"
else
  echo "==> ${TF_BIN} has no query command; list resources are not exercised"
fi

echo "==> Running the corpus: ${CORPUS} (${CONFIGURATIONS} configurations)"
# PYVIDER_TESTMODE publishes the components registered `test_only`, which a
# large part of the corpus configures and would otherwise skip.
set +e
PYVIDER_TESTMODE=true "${VENV}/bin/soup" stir --recursive "${CORPUS}" 2>&1 | tee "${PROJECT_ROOT}/terraform-gate/stir.log"
STIR_STATUS="${PIPESTATUS[0]}"
set -e

if grep -q "No directories found" "${PROJECT_ROOT}/terraform-gate/stir.log"; then
  echo "stir discovered no example directories; the gate proved nothing" >&2
  exit 1
fi
PASSED="$(sed 's/\x1b\[[0-9;]*m//g' "${PROJECT_ROOT}/terraform-gate/stir.log" \
  | grep -oE 'Passed:[[:space:]]+[0-9]+' | grep -oE '[0-9]+' | head -1)"
if [ -z "${PASSED}" ] || [ "${PASSED}" -eq 0 ]; then
  echo "stir reported no passing examples; the gate proved nothing" >&2
  exit 1
fi

echo "==> ${PASSED} example directories passed"
exit "${STIR_STATUS}"
