#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Attach files to a GitHub release, surviving a transient API failure.
#
# `gh release upload` sends each file in turn and gives up on the first
# rejection, having already uploaded some. A single HTTP 502 from
# api.github.com therefore leaves the release holding part of the set -- and
# the part it holds is arbitrary, so a signature can outlive the artifact it
# signs. That is worse than an empty release: a `.sigstore.json` beside no
# file implies something was published and verified when nothing was.
#
# Uploading is idempotent (`--clobber` replaces), so the whole set is retried
# until it lands. This narrows the window rather than closing it: when the
# retries run out, the release keeps whatever earlier attempts attached. That
# state is reported loudly and repaired by re-running with `release_tag`, and
# `drop_orphan_signatures.sh` removes any signature left without its subject.
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <tag> <file>..." >&2
  exit 2
fi

TAG="$1"
shift

REPO="${GITHUB_REPOSITORY:?GITHUB_REPOSITORY must be set}"

# Fail fast on anything retrying cannot fix. The caller passes globs that the
# workflow shell expands, so an unmatched pattern arrives as its literal self;
# retrying that spends the whole backoff and buries the real cause under five
# identical failures.
missing=0
for file in "$@"; do
  if [ ! -f "${file}" ]; then
    echo "::error::not a file: ${file}" >&2
    missing=1
  fi
done
if [ "${missing}" -ne 0 ]; then
  echo "refusing to attach: the set above is incomplete before any upload" >&2
  exit 2
fi

ATTEMPTS="${RELEASE_UPLOAD_ATTEMPTS:-5}"
DELAY="${RELEASE_UPLOAD_DELAY_SECONDS:-5}"

captured="$(mktemp)"
trap 'rm -f "${captured}"' EXIT

for attempt in $(seq 1 "${ATTEMPTS}"); do
  if gh release upload "${TAG}" "$@" --repo "${REPO}" --clobber 2>&1 | tee "${captured}"; then
    echo "==> attached $# files to ${TAG}"
    exit 0
  fi

  # Authentication, authorisation and a wrong tag are settled answers. Retrying
  # them changes nothing and delays the report.
  if grep -qiE 'HTTP 40[0134]|release not found|could not resolve to a Release|Bad credentials' "${captured}"; then
    echo "::error::attach failed for a reason retrying cannot fix; see above" >&2
    exit 1
  fi

  if [ "${attempt}" -eq "${ATTEMPTS}" ]; then
    break
  fi
  echo "attach failed (attempt ${attempt}/${ATTEMPTS}); retrying in ${DELAY}s" >&2
  sleep "${DELAY}"
  DELAY=$((DELAY * 2))
done

echo "could not attach the release artifacts after ${ATTEMPTS} attempts" >&2
echo "the release may hold an incomplete set; re-run this workflow with" >&2
echo "release_tag=${TAG} to repair it" >&2
exit 1
