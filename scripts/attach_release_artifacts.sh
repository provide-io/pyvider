#!/usr/bin/env bash
# Attach files to a GitHub release, surviving a transient API failure.
#
# `gh release upload` sends each file in turn and gives up on the first
# rejection, having already uploaded some. A single HTTP 502 from
# api.github.com therefore leaves the release holding part of the set -- and
# the part it holds is arbitrary, so a signature can outlive the artifact it
# signs. That is worse than an empty release: a `.sigstore.json` beside no
# file implies something was published and verified when nothing was.
#
# Uploading is idempotent (`--clobber` replaces), so the whole set is simply
# retried until it lands. The alternative, uploading each file in its own
# command, still leaves a partial set when the retries run out; this way the
# release either gets everything or the job fails with nothing half-done that
# a reader would mistake for a complete one.
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <tag> <file>..." >&2
  exit 2
fi

TAG="$1"
shift

ATTEMPTS="${RELEASE_UPLOAD_ATTEMPTS:-5}"
DELAY="${RELEASE_UPLOAD_DELAY_SECONDS:-5}"

for attempt in $(seq 1 "${ATTEMPTS}"); do
  if gh release upload "${TAG}" "$@" --repo "${GITHUB_REPOSITORY}" --clobber; then
    echo "==> attached $# files to ${TAG}"
    exit 0
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
