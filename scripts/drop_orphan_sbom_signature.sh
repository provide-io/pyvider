#!/usr/bin/env bash
# Remove an SBOM signature from a release that no longer carries the SBOM.
#
# The repair path deliberately does not rebuild an SBOM: its dependency
# closure would be today's resolution rather than the release's, and an SBOM
# confidently wrong about what shipped is worse than none. But a run that
# failed partway can leave `sbom-python.cdx.json.sigstore.json` attached
# without `sbom-python.cdx.json`, and a signature beside no file reads as a
# verified artifact that is merely hard to find.
#
# Absent is the honest state, so the orphan is removed. A release holding both
# is left alone.
set -euo pipefail

TAG="${1:?usage: $0 <tag>}"
SBOM="sbom-python.cdx.json"
SIGNATURE="${SBOM}.sigstore.json"

assets="$(gh release view "${TAG}" --repo "${GITHUB_REPOSITORY}" --json assets --jq '.assets[].name')"

if ! grep -qxF "${SIGNATURE}" <<<"${assets}"; then
  echo "==> no ${SIGNATURE} on ${TAG}; nothing to drop"
  exit 0
fi

if grep -qxF "${SBOM}" <<<"${assets}"; then
  echo "==> ${TAG} carries both the SBOM and its signature; leaving them"
  exit 0
fi

echo "==> ${TAG} has ${SIGNATURE} but no ${SBOM}; removing the orphan signature"
gh release delete-asset "${TAG}" "${SIGNATURE}" --repo "${GITHUB_REPOSITORY}" --yes
