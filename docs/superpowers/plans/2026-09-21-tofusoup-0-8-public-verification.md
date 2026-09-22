# TofuSoup 0.8 Public Provider-Lint Verification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove that the published TofuSoup package—not its source worktree—processes the released provider's direct and OpenTofu lint lanes.

**Architecture:** Run `tofusoup==0.8.0` through `uvx` against the exact released terraform-provider-pyvider 0.6.0 binary and checked-in suite. Validate stable JSON output and the four-versus-seven boundary; if a genuine runner defect appears, stop the train and design a separate test-first patch instead of embedding a workaround downstream.

**Tech Stack:** TofuSoup 0.8.0 from PyPI, uvx, tfprotov6, OpenTofu 1.13.0-beta1, JSON, SHA-256.

---

**Reference worktree:** `/Volumes/data/pyv/tofusoup-lint-suite`
**Provider worktree:** `/Users/tim/.config/superpowers/worktrees/terraform-provider-pyvider/provider-linting`

This plan is verification-only when 0.8.0 behaves correctly. Do not modify or
re-release TofuSoup merely to change presentation in the tutorial or website.

### Task 1: Confirm the public package identity

**Files:**
- No source changes

- [ ] **Step 1: Prove the repository release coordinate.**

```bash
git -C /Volumes/data/pyv/tofusoup-lint-suite status --short --branch
git -C /Volumes/data/pyv/tofusoup-lint-suite show v0.8.0:VERSION
```

Expected: clean `codex/lint-suite` worktree and `0.8.0` from the tag. If the
tag is not present locally, fetch tags from `gh-origin` and repeat.

- [ ] **Step 2: Prove PyPI supplies the expected CLI.**

```bash
uvx --refresh --from tofusoup==0.8.0 soup --version
uvx --from tofusoup==0.8.0 soup lint --help
```

Expected: version 0.8.0; help lists `--provider`, `--opentofu`, `--lane`, and
`--json`.

- [ ] **Step 3: Integrate the already released branch into the default branch.**

`v0.8.0` is public from `codex/lint-suite`, but that branch is still ahead of
default `main`. Push if needed, open a PR containing exactly the 12 released
commits, require CI, and merge it without adding code changes. Confirm `main`
contains tag commit `d143941c8562424b3d38fe69de802f5f8a8655f2`.

### Task 2: Verify the released provider through both lanes

**Files:**
- Read from public `v0.6.0` source archive: `tests/e2e/provider-linting/lint.soup.toml`
- Read from public release assets: `provider-linting-proof.json`

- [ ] **Step 1: Resolve and validate explicit artifact paths.**

Set these shell variables from the provider 0.6.0 plan's downloaded release
artifact, released proof manifest, and pinned OpenTofu installer output. Run
this verification in the proof platform recorded by the manifest
(`linux_amd64`, on Ubuntu 24.04):

```bash
test -n "${PYVIDER_RELEASE_BIN:?set PYVIDER_RELEASE_BIN to the downloaded v0.6.0 executable}"
test -x "$PYVIDER_RELEASE_BIN"
test -n "${PROVIDER_RELEASE_PROOF:?set PROVIDER_RELEASE_PROOF to the downloaded v0.6.0 proof manifest}"
test -f "$PROVIDER_RELEASE_PROOF"
tofu_cache=$(mktemp -d /tmp/tofusoup-public-opentofu.XXXXXX)
tofu_install_log="$tofu_cache/install.log"
tofu_archive=tofu_1.13.0-beta1_linux_amd64.zip
curl --fail --location --silent --show-error \
  -o "$tofu_cache/SHA256SUMS" \
  https://github.com/opentofu/opentofu/releases/download/v1.13.0-beta1/tofu_1.13.0-beta1_SHA256SUMS
curl --fail --location --silent --show-error \
  -o "$tofu_cache/$tofu_archive" \
  "https://github.com/opentofu/opentofu/releases/download/v1.13.0-beta1/$tofu_archive"
awk -v name="$tofu_archive" '$2 == name {print}' "$tofu_cache/SHA256SUMS" \
  > "$tofu_cache/$tofu_archive.sha256"
(cd "$tofu_cache" && shasum -a 256 -c "$tofu_archive.sha256") 2>"$tofu_install_log"
OPENTOFU_ARCHIVE_SHA256=$(awk '{print $1}' "$tofu_cache/$tofu_archive.sha256")
unzip -q "$tofu_cache/$tofu_archive" tofu -d "$tofu_cache/bin"
OPENTOFU_BETA_BIN="$tofu_cache/bin/tofu"
chmod +x "$OPENTOFU_BETA_BIN"
test -x "$OPENTOFU_BETA_BIN"
test -n "$OPENTOFU_ARCHIVE_SHA256"
provider_expected=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["provider_binary"]["sha256"])' "$PROVIDER_RELEASE_PROOF")
provider_actual=$(shasum -a 256 "$PYVIDER_RELEASE_BIN" | awk '{print $1}')
test "$provider_actual" = "$provider_expected"
tofu_expected=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["opentofu"]["archive_sha256"])' "$PROVIDER_RELEASE_PROOF")
test "$OPENTOFU_ARCHIVE_SHA256" = "$tofu_expected"
"$OPENTOFU_BETA_BIN" version
```

Expected: the provider checksum equals the released proof manifest and OpenTofu
prints 1.13.0-beta1.

- [ ] **Step 2: Extract the public provider source archive.**

```bash
verify_tmp=$(mktemp -d /tmp/tofusoup-0.8-provider-lint.XXXXXX)
gh release download v0.6.0 --repo provide-io/terraform-provider-pyvider \
  --archive=tar.gz --dir "$verify_tmp"
source_archive=$(find "$verify_tmp" -maxdepth 1 -name '*.tar.gz' -print -quit)
test -n "$source_archive"
tar -xzf "$source_archive" -C "$verify_tmp"
released_source=$(find "$verify_tmp" -maxdepth 1 -type d -name 'terraform-provider-pyvider-*' -print -quit)
test -f "$released_source/tests/e2e/provider-linting/lint.soup.toml"
```

Expected: the suite comes from the public tag archive, not a development
worktree, and declares provider version 0.6.0.

- [ ] **Step 3: Run the direct lane with the published CLI.**

```bash
uvx --from tofusoup==0.8.0 soup lint \
  "$released_source/tests/e2e/provider-linting/lint.soup.toml" \
  --provider "$PYVIDER_RELEASE_BIN" \
  --lane direct --json > "$verify_tmp/direct.json"
```

Expected: exit zero.

- [ ] **Step 4: Assert all seven direct cases from JSON.**

```bash
python3 - "$verify_tmp/direct.json" <<'PY'
import json, sys
payload = json.load(open(sys.argv[1], encoding="utf-8"))
assert payload["version"] == 1
assert payload["opentofu"] is None
cases = payload["direct"]["cases"]
assert [case["kind"] for case in cases] == [
    "provider", "resource", "data-source", "ephemeral", "list", "action", "state-store"
]
assert all(case["diagnostics"] for case in cases)
PY
```

Expected: exit zero. This helper verifies output after the public command; it
is not shown in the tutorial recording.

- [ ] **Step 5: Run the OpenTofu lane with the published CLI.**

```bash
uvx --from tofusoup==0.8.0 soup lint \
  "$released_source/tests/e2e/provider-linting/lint.soup.toml" \
  --provider "$PYVIDER_RELEASE_BIN" \
  --opentofu "$OPENTOFU_BETA_BIN" \
  --lane opentofu --json > "$verify_tmp/opentofu.json"
```

Expected: exit zero.

- [ ] **Step 6: Assert the OpenTofu lane remains separately labelled.**

```bash
python3 - "$verify_tmp/opentofu.json" <<'PY'
import json, sys
payload = json.load(open(sys.argv[1], encoding="utf-8"))
assert payload["version"] == 1
assert payload["direct"] is None
assert payload["opentofu"]["valid"] is True
summaries = {item["summary"] for item in payload["opentofu"]["diagnostics"]}
expected = {
    "TLS certificate verification is disabled (provide-io/pyvider:insecure-tls)",
    "Directory permissions are world-writable (provide-io/pyvider:world-writable-directory)",
    "HTTP API uses an unencrypted connection (provide-io/pyvider:insecure-http)",
    "Lease lifetime exceeds one hour (provide-io/pyvider:long-lived-lease)",
}
assert expected <= summaries
assert not any("include-hidden-files" in value for value in summaries)
assert not any("long-action-timeout" in value for value in summaries)
assert not any("relative-state-store-path" in value for value in summaries)
PY
```

Expected: exit zero; provider/resource/data-source/ephemeral are present while
list/action/state-store are absent.

### Task 3: Decide the runner outcome

**Files:**
- No source changes for a passing result

- [ ] **Step 1: Record passing evidence.**

Record the TofuSoup version, `uvx` resolution output, provider binary checksum,
OpenTofu version/checksum, two command lines, and JSON checksums in the release
coordinate ledger.

- [ ] **Step 2: Apply the no-workaround rule on failure.**

If either public command fails while the same fixture passes from the TofuSoup
source worktree, stop the release train. Preserve stdout/stderr and reduce the
failure into a new failing test in a dedicated TofuSoup bug design. Do not:

- call TofuSoup internals from a Python script;
- copy TofuSoup source into the provider or tutorial;
- weaken suite expectations;
- claim the source-worktree result as released-package proof.

Resume this plan only after the tested patch release is on PyPI, replacing
`0.8.0` in the commands with that exact patch version.
