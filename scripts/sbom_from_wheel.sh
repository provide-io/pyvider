#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Generate a CycloneDX SBOM for the *built wheel and its dependencies*.
#
# `cyclonedx-py environment` describes whatever is installed in an interpreter,
# so run bare under `uvx` it described the ephemeral tool venv -- cyclonedx-bom
# and its own dependencies, nothing of this package. The wheel is installed into
# a fresh venv here and that venv's interpreter is the one described.
#
# That mistake published 77 SBOMs across this ecosystem, every one listing the
# same 34 packages and none of them the release they claimed to describe. It is
# worse than shipping nothing: a CVE sweep querying it gets a confident wrong
# answer. The checks at the end exist so it cannot happen quietly again.
#
# Usage: scripts/sbom_from_wheel.sh <dist-dir> <output-file> [pyproject.toml]
set -euo pipefail

# Pinned: this runs code fetched from PyPI inside the release workflow. Bump
# deliberately, and re-run the script locally against a fresh `uv build` first.
CYCLONEDX_BOM_VERSION="7.3.1"
# Same rule. Used only by the verification below, to evaluate the environment
# markers on the wheel's Requires-Dist.
PACKAGING_VERSION="26.3"

# CycloneDX type of the root component: `library` for a distribution other code
# imports, `application` for a CLI-first one. Only affects how consumers
# classify the subject, not what is recorded.
MC_TYPE="${SBOM_MC_TYPE:-library}"

DIST_DIR="${1:?usage: sbom_from_wheel.sh <dist-dir> <output-file> [pyproject.toml]}"
OUT="${2:?usage: sbom_from_wheel.sh <dist-dir> <output-file> [pyproject.toml]}"
PYPROJECT="${3:-pyproject.toml}"

VENV="$(mktemp -d)/sbom-venv"
uv venv --quiet "$VENV"
uv pip install --quiet --python "$VENV/bin/python" "$DIST_DIR"/*.whl

# --pyproject is what gives the document a root component -- a statement of
# what the SBOM is *about*, rather than 58 peers with the subject buried among
# them. Without it `metadata.component` is null and tooling that keys off the
# root subject finds nothing.
uvx --from "cyclonedx-bom==${CYCLONEDX_BOM_VERSION}" cyclonedx-py environment "$VENV/bin/python" \
  --pyproject "$PYPROJECT" \
  --mc-type "$MC_TYPE" \
  --output-format json -o "$OUT"

# Installed *after* the SBOM is generated, and that order is load-bearing: this
# venv is the environment the document describes, so anything added to it before
# the previous step would be published as a component of the release.
uv pip install --quiet --python "$VENV/bin/python" "packaging==${PACKAGING_VERSION}"

# Run under the venv's interpreter rather than the runner's. The check below
# evaluates environment markers, and the only environment whose answers mean
# anything here is the one the SBOM describes.
"$VENV/bin/python" - "$DIST_DIR" "$OUT" <<'PYEOF'
"""Complete the root component from the wheel, then verify the SBOM.

Every project here declares `dynamic = ["version"]`, so cyclonedx-py reads the
name out of pyproject.toml and leaves the version null -- it does not build the
project to resolve one. The wheel filename is the authority for both, and the
purl follows from them.
"""

import json
import pathlib
import re
import sys
import zipfile

from packaging.requirements import InvalidRequirement, Requirement

dist, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])


def fail(message: str) -> None:
    print(f"::error::{message}")
    raise SystemExit(1)


def normalize(name: str) -> str:
    # PEP 503 normalization: the wheel filename escapes the name, the SBOM does not.
    return re.sub(r"[-_.]+", "-", name).lower()


wheel = next(iter(sorted(dist.glob("*.whl"))), None)
if wheel is None:
    fail(f"no wheel in {dist}/ to check the SBOM against")

raw_name, version = wheel.name.split("-")[:2]
expected = normalize(raw_name)

# Requires-Dist from the wheel's own metadata, narrowed to what this
# environment should actually hold. A marker decides that, so a marker is what
# has to be evaluated -- not a substring of one.
#
# The `extra == "cli"` case used to be handled by a literal `"extra ==" in spec`
# test, which is a hand-rolled evaluation of one marker and blind to every
# other. It failed provide-foundation's v0.4.3 release, where
# `tzdata; sys_platform == "win32"` carries no extra and so was demanded on the
# Linux runner that builds the SBOM -- the one platform where the marker
# correctly keeps it uninstalled. This project declares no conditional
# dependency today; the check is fixed here so that the first one added does not
# break a release to discover it.
#
# An empty `extra` is what makes `extra == "cli"` false: no extra was requested
# when the wheel was installed above.
requires = set()
with zipfile.ZipFile(wheel) as zf:
    metadata_name = next((n for n in zf.namelist() if n.endswith(".dist-info/METADATA")), None)
    if metadata_name is None:
        fail(f"{wheel.name} has no .dist-info/METADATA")
    for line in zf.read(metadata_name).decode("utf-8", "replace").splitlines():
        if not line.startswith("Requires-Dist:"):
            continue
        spec = line.split(":", 1)[1].strip()
        try:
            req = Requirement(spec)
        except InvalidRequirement as exc:
            fail(f"{wheel.name} has an unparsable Requires-Dist {spec!r}: {exc}")
        if req.marker is not None and not req.marker.evaluate({"extra": ""}):
            continue
        requires.add(normalize(req.name))

bom = json.loads(out.read_text())
components = bom.get("components") or []
present = {normalize(c["name"]) for c in components}

root = bom.setdefault("metadata", {}).get("component")
if root is None:
    fail("SBOM has no metadata.component -- it does not declare what it describes")
if normalize(root.get("name", "")) != expected:
    fail(f"SBOM root component is {root.get('name')!r}, expected {expected!r}")

if not root.get("version"):
    root["version"] = version
elif root["version"] != version:
    fail(f"SBOM root version {root['version']!r} disagrees with the wheel's {version!r}")
if not root.get("purl"):
    root["purl"] = f"pkg:pypi/{expected}@{version}"

# The root component alone does not prove the right environment was described:
# it comes from pyproject.toml and would be correct even if the venv install
# had silently produced nothing. The dependency closure is what proves it.
missing = sorted(requires - present)
if missing:
    fail(
        f"SBOM lists {len(components)} components but is missing {len(missing)} of "
        f"{expected}'s dependencies ({', '.join(missing[:5])}) -- wrong environment"
    )

out.write_text(json.dumps(bom, indent=2) + "\n")
print(f"SBOM describes {expected} {version} with {len(components)} dependencies")
PYEOF

echo "SBOM written to $OUT"
