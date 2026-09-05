#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Remove any .sigstore.json from a release whose subject file is not there.
#
# A signature beside no file reads as a verified artifact that is merely hard
# to find, so absent is the honest state.
#
# Every artifact is signed -- wheel, sdist and SBOM -- and a run that failed
# partway can orphan any of them, so this matches on the suffix rather than on
# one known name. The repair path additionally never rebuilds the SBOM (its
# dependency closure would be today's resolution rather than the release's),
# which orphans that signature by design.
#
# A release holding both a file and its signature is left alone.
set -euo pipefail

TAG="${1:?usage: $0 <tag>}"
REPO="${GITHUB_REPOSITORY:?GITHUB_REPOSITORY must be set}"

SUFFIX=".sigstore.json"

# --paginate, because a listing truncated at one page would report a present
# subject as absent and delete a signature that is not an orphan. This is
# irreversible and runs unattended, so it reads the whole set or nothing.
assets="$(gh api --paginate "repos/${REPO}/releases/tags/${TAG}" --jq '.assets[].name')"

if [ -z "${assets}" ]; then
  echo "==> ${TAG} lists no assets; nothing to drop"
  exit 0
fi

dropped=0
while IFS= read -r signature; do
  [ -n "${signature}" ] || continue
  case "${signature}" in
    *"${SUFFIX}") ;;
    *) continue ;;
  esac

  subject="${signature%"${SUFFIX}"}"
  if grep -qxF "${subject}" <<<"${assets}"; then
    continue
  fi

  echo "==> ${TAG} has ${signature} but no ${subject}; removing the orphan"
  gh release delete-asset "${TAG}" "${signature}" --repo "${REPO}" --yes
  dropped=$((dropped + 1))
done <<<"${assets}"

if [ "${dropped}" -eq 0 ]; then
  echo "==> ${TAG} carries no orphan signatures"
fi
