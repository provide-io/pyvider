# terraform-provider-pyvider 0.6.0 Lint Proof Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Release terraform-provider-pyvider 0.6.0 with artifact-bound proof of seven direct lint paths and four OpenTofu-reached paths using released dependencies only.

**Architecture:** Replace development source injection with public PyPI inputs, recording both release-tag commits and exact wheel bytes. The proof job consumes the `linux_amd64` release-candidate artifact from the same numeric workflow run instead of rebuilding a second provider. Cross-platform conformance remains separate; the proof binds one named platform, provider commit, archive, and binary checksum.

**Tech Stack:** Python 3.11+, uv, Flavorpack, pytest, TofuSoup 0.8.0, OpenTofu 1.13.0-beta1, GitHub Actions/Releases, JSON provenance, asciinema casts.

---

**Repository:** `/Users/tim/.config/superpowers/worktrees/terraform-provider-pyvider/provider-linting`
**Starting branch:** `codex/provider-linting`

### Task 1: Preserve the user-owned proof checkpoint

**Files:**
- Preserve without staging: `provider-linting-direct.cast`
- Preserve without staging: `provider-linting-opentofu.cast`
- Preserve without staging: `provider-linting-walkthrough.cast`
- Preserve without staging: `provider-linting-proof.json`

- [ ] **Step 1: Verify the current dirty artifacts before copying them.**

```bash
uv run python ci/verify-provider-linting-proof.py \
  provider-linting-proof.json provider-linting-opentofu.cast \
  provider-linting-direct.cast provider-linting-walkthrough.cast
uv run pytest tests/proof -q
shasum -a 256 provider-linting-direct.cast provider-linting-opentofu.cast \
  provider-linting-walkthrough.cast provider-linting-proof.json
```

Expected: verifier passes, 124 proof tests pass, and four hashes are printed.

- [ ] **Step 2: Copy the checkpoint outside the repository.**

```bash
proof_backup=$(mktemp -d /tmp/provider-lint-proof-checkpoint.XXXXXX)
cp provider-linting-direct.cast provider-linting-opentofu.cast \
  provider-linting-walkthrough.cast provider-linting-proof.json "$proof_backup/"
shasum -a 256 provider-linting-direct.cast provider-linting-opentofu.cast \
  provider-linting-walkthrough.cast provider-linting-proof.json \
  > "$proof_backup/SHA256SUMS"
git diff --binary -- provider-linting-direct.cast provider-linting-opentofu.cast \
  provider-linting-walkthrough.cast provider-linting-proof.json \
  > "$proof_backup/checkpoint.patch"
for name in provider-linting-direct.cast provider-linting-opentofu.cast \
  provider-linting-walkthrough.cast provider-linting-proof.json; do
  cmp "$name" "$proof_backup/$name"
done
python3 - "$proof_backup" /tmp/pyvider-provider-lint-release-coordinates.json <<'PY'
import json, sys
path = sys.argv[2]
data = json.load(open(path, encoding="utf-8"))
data["terraform_provider_pyvider"]["proof_checkpoint"] = sys.argv[1]
open(path, "w", encoding="utf-8").write(json.dumps(data, indent=2) + "\n")
PY
```

Expected: all four copies exist. Record `proof_backup` and hashes in the release
ledger. The ledger carries the literal backup path across executor shells. Do
not reset or stage the originals.

### Task 2: Convert the coordinated build to public release artifacts

**Files:**
- Modify: `tests/test_linting_stack_build.py`
- Modify: `tests/conformance/test_provider_linting.py`
- Modify: `tests/proof/test_provider_linting_proof.py`
- Create: `tests/test_release_contract.py`
- Modify: `ci/build-provider-linting-stack.py`
- Modify: `Makefile`
- Modify: `.github/workflows/build-provider.yml`
- Modify: `docs/guides/provider-linting-proof.md`

- [ ] **Step 1: Replace source-checkout expectations with public-wheel expectations.**

Delete tests requiring `--pyvider-source`, `--components-source`, Git archive
hashes for those repositories, `.stack/` paths, or injected local
`[tool.uv.sources]`. Add focused tests for this contract:

```python
def test_pin_public_lint_dependencies_removes_sources(tmp_path: Path) -> None:
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\ndependencies=["pyvider>=0.7.0", "pyvider-components>=0.7.2"]\n'
        '[tool.uv.sources]\npyvider={path="../pyvider"}\n',
        encoding="utf-8",
    )
    module.pin_public_lint_dependencies(project, pyvider="0.8.0", components="0.8.0")
    parsed = tomllib.loads(project.read_text(encoding="utf-8"))
    assert "pyvider==0.8.0" in parsed["project"]["dependencies"]
    assert "pyvider-components==0.8.0" in parsed["project"]["dependencies"]
    assert "sources" not in parsed.get("tool", {}).get("uv", {})


def test_provenance_records_public_wheel_hashes(tmp_path: Path) -> None:
    provenance = successful_public_build(tmp_path)
    assert provenance["dependencies"]["pyvider"] == {
        "version": "0.8.0", "tag": "v0.8.0", "commit": PYVIDER_TAG_SHA,
        "registry": "https://pypi.org/simple",
        "wheel": "pyvider-0.8.0-py3-none-any.whl", "sha256": PYVIDER_SHA,
    }
    assert provenance["dependencies"]["pyvider-components"] == {
        "version": "0.8.0", "tag": "v0.8.0", "commit": COMPONENTS_TAG_SHA,
        "registry": "https://pypi.org/simple",
        "wheel": "pyvider_components-0.8.0-py3-none-any.whl", "sha256": COMPONENTS_SHA,
    }
    assert provenance["artifacts"]["binary"]["platform"] == "linux_amd64"
    assert provenance["artifacts"]["binary"]["path"].endswith("terraform-provider-pyvider_v0.6.0")
    assert provenance["artifacts"]["psp"]["path"].endswith("terraform-provider-pyvider.psp")
    assert provenance["release_candidate"] == {
        "github_artifact": "provider-linux-amd64",
        "archive": "terraform-provider-pyvider_0.6.0_linux_amd64.zip",
        "platform": "linux_amd64",
        "sha256": RELEASE_ARCHIVE_SHA,
    }
```

Also assert the build commands contain no editable/path/git dependency and the
workflow contains neither `pyvider_ref`, `components_ref`, `.stack/pyvider`, nor
`.stack/pyvider-components`.
Parse the disposable `uv.lock` and require both dependency records to use
`source = { registry = "https://pypi.org/simple" }`; reject Git, path, URL, and
editable sources. Add a cleanliness test that permits exactly the four known
proof-output files while rejecting any other dirty tracked or untracked path.

- [ ] **Step 2: Run the focused tests red.**

```bash
uv run pytest tests/test_linting_stack_build.py tests/test_release_contract.py -q
```

Expected: failures name missing `pin_public_lint_dependencies`, old source CLI,
and absent public wheel hashes.

- [ ] **Step 3: Implement public dependency pinning.**

In the disposable archived provider project, implement:

```python
def pin_public_lint_dependencies(path: Path, *, pyvider: str, components: str) -> None:
    project: dict[str, Any] = tomllib.loads(path.read_text(encoding="utf-8"))
    replacements = {
        "pyvider": f"pyvider=={pyvider}",
        "pyvider-components": f"pyvider-components=={components}",
    }
    dependencies = []
    seen: set[str] = set()
    for requirement in project["project"]["dependencies"]:
        name = requirement.split("[", 1)[0].split("<", 1)[0].split(">", 1)[0].split("=", 1)[0]
        if name in replacements:
            dependencies.append(replacements[name])
            seen.add(name)
        else:
            dependencies.append(requirement)
    if seen != replacements.keys():
        raise ValueError("provider project does not declare both lint dependencies")
    project["project"]["dependencies"] = dependencies
    uv = project.get("tool", {}).get("uv", {})
    uv.pop("sources", None)
    path.write_text(tomli_w.dumps(project), encoding="utf-8")
```

Change the CLI to require `--pyvider-version 0.8.0` and
`--components-version 0.8.0`, retain only the provider repository as a Git
source, and run `uv lock --refresh` followed by Flavorpack. Construct the
disposable source tree from `git archive HEAD`. Validate dirtiness separately:
the four preserved proof outputs are allowed because they are not build inputs;
every other dirty path fails closed.

- [ ] **Step 4: Record hashes from the wheels actually packed.**

After extracting Flavorpack's wheels slot, locate exactly one wheel for each
coordinate, hash its bytes, and write schema version 2 provenance:

```json
{
  "schema_version": 2,
  "provider_repository_head": "$PROVIDER_GIT_SHA",
  "provider_repository_archive_sha256": "$PROVIDER_ARCHIVE_SHA256",
  "dependencies": {
    "pyvider": {"version": "0.8.0", "tag": "v0.8.0", "commit": "$PYVIDER_TAG_COMMIT", "registry": "https://pypi.org/simple", "wheel": "pyvider-0.8.0-py3-none-any.whl", "sha256": "$PYVIDER_WHEEL_SHA256"},
    "pyvider-components": {"version": "0.8.0", "tag": "v0.8.0", "commit": "$COMPONENTS_TAG_COMMIT", "registry": "https://pypi.org/simple", "wheel": "pyvider_components-0.8.0-py3-none-any.whl", "sha256": "$COMPONENTS_WHEEL_SHA256"}
  },
  "release_candidate": {
    "github_artifact": "provider-linux-amd64",
    "archive": "terraform-provider-pyvider_0.6.0_linux_amd64.zip",
    "platform": "linux_amd64",
    "sha256": "$RELEASE_ARCHIVE_SHA256"
  },
  "artifacts": {
    "psp": {"path": "dist/linux_amd64/terraform-provider-pyvider.psp", "sha256": "$PSP_SHA256"},
    "binary": {"path": "dist/linux_amd64/terraform-provider-pyvider_v0.6.0", "platform": "linux_amd64", "sha256": "$BINARY_SHA256"}
  }
}
```

The dollar-prefixed fields above describe the schema; the builder writes the
actual hashes computed from downloaded and packed bytes.

Resolve each public tag commit through the GitHub API and record it alongside
the registry, wheel name, and wheel hash. Reject missing, duplicate,
version-mismatched, non-registry, editable, or direct-URL wheels.
The `path` values are manifest-relative so the recorder resolves each as
`provenance.parent / path`.

- [ ] **Step 5: Update Make and CI interfaces.**

The Make target becomes:

```make
build-linting-stack:
	uv run python ci/build-provider-linting-stack.py --provider-repository . \
	  --pyvider-version 0.8.0 --components-version 0.8.0 --output-dir dist
```

Remove the two source-ref workflow inputs/checkouts/environment variables. The
build matrix creates the public-dependency package once. The proof job downloads
that run's `linux_amd64` release-candidate artifact and provenance, extracts the
binary, and supplies it to all proof commands. It asserts the platform and two
wheel hashes. It must not invoke Flavorpack a second time.
After the matrix job creates the final ZIP, a finalization step computes its
SHA-256 and writes the archive/artifact identity plus the PSP/binary paths and
hashes into provenance before uploading both together. The proof job restores
the same `dist/linux_amd64/...` layout so manifest-relative resolution is exact.

- [ ] **Step 6: Update proof contracts and docs.**

Change conformance/proof assertions and the guide from dependency source
archives to public versions, release-tag commits, registry URLs, wheel names,
and wheel hashes. Retain provider source SHA/archive hash, proof platform,
release-candidate artifact identity, binary hash, OpenTofu checksum, exact
commands, and lane observations.

- [ ] **Step 7: Run the focused suite and commit.**

```bash
uv run pytest tests/test_linting_stack_build.py tests/conformance/test_provider_linting.py tests/proof/test_provider_linting_proof.py tests/test_release_contract.py -q
uv run ruff check ci tests
uv run ruff format --check ci tests
git add ci/build-provider-linting-stack.py Makefile .github/workflows/build-provider.yml \
  docs/guides/provider-linting-proof.md tests/test_linting_stack_build.py \
  tests/conformance/test_provider_linting.py tests/proof/test_provider_linting_proof.py \
  tests/test_release_contract.py
git commit -m "build: prove linting from public release artifacts"
```

Expected: all pass; the four dirty proof artifacts remain unstaged.

### Task 3: Bind default CI and release identity to the proof

**Files:**
- Modify: `tests/test_release_contract.py`
- Modify: `.github/workflows/ci.yml`
- Modify: `.github/workflows/build-provider.yml`
- Modify: `.github/workflows/release.yml`
- Modify: `ci/publish-release.sh` if asset collection is implemented there

- [ ] **Step 1: Add failing workflow DAG tests.**

Parse the YAML and assert:

```python
assert ci_inputs["run-tests"] is True
assert "provider-linting-proof" in release_required_jobs
assert release_build_run_is_numeric_and_explicit
assert release_build_head_sha_equals_release_target
for name in (
    "provider-linting-proof.json",
    "provider-linting-opentofu.cast",
    "provider-linting-direct.cast",
    "provider-linting-walkthrough.cast",
    "provider-linting-build-provenance.json",
):
    assert name in release_assets
assert "verify-release-proof" in release_required_jobs
```

Also assert no branch accepts an arbitrary “latest successful” build.
Assert the publisher invokes `gh release create ... --target "$RELEASE_TARGET_SHA"`
and that `RELEASE_TARGET_SHA` is the workflow's validated `github.sha`.

- [ ] **Step 2: Run them red.**

```bash
uv run pytest tests/test_release_contract.py -q
```

Expected: failures for disabled default tests, unbound build selection, and
missing proof assets.

- [ ] **Step 3: Make tests a default PR gate.**

Set `run-tests: true` in `.github/workflows/ci.yml` and remove the stale comment
claiming there is no repository-local pytest suite.

- [ ] **Step 4: Bind release input to one build run.**

Require a numeric `build_run_id`. If the release workflow dispatches a build,
pass `provider_linting_proof=true`, capture that new run's ID, and wait for it.
Before downloading, query the Actions API and require:

```text
workflow name == build-provider.yml
conclusion == success
headSha == release target SHA
provider-linting-proof artifact present and unexpired
all platform build artifacts present
```

Never reuse an older run merely because it is the latest success.
Pass the validated workflow SHA to `ci/publish-release.sh` as
`RELEASE_TARGET_SHA`. The script must require a full 40-character SHA and pass
`--target "$RELEASE_TARGET_SHA"` when it creates the release/tag, preventing a
moving default branch from selecting the tag commit.

- [ ] **Step 5: Include proof in checksum/signature/release assets.**

Download the proof artifact from that numeric run, add all five files to the
release staging directory, include them in `SHA256SUMS` and the separately
named proof/build provenance manifest—not `terraform-registry-manifest.json`—
sign through the existing release path, and attach them to the GitHub release.

Add `verify-release-proof` after publication. On Ubuntu it downloads the
release's `linux_amd64` archive, `SHA256SUMS`, build provenance, schema-v3 proof
manifest, and three casts from GitHub Releases into a fresh directory; verifies
all checksums/signatures; extracts the binary into the manifest-relative layout;
installs OpenTofu 1.13.0-beta1 and TofuSoup 0.8.0; and reruns conformance,
OpenTofu, and the proof verifier with absolute downloaded paths. This job must
compare the run head SHA, release tag target, proof source SHA, platform, and
binary hash before it can pass.

- [ ] **Step 6: Verify workflow tests and commit.**

```bash
uv run pytest tests/test_release_contract.py -q
uv run python -c 'import pathlib, yaml; [yaml.safe_load(path.read_text()) for path in pathlib.Path(".github/workflows").glob("*.yml")]'
git add tests/test_release_contract.py .github/workflows/ci.yml \
  .github/workflows/build-provider.yml .github/workflows/release.yml ci/publish-release.sh
git commit -m "ci: bind provider release to verified proof"
```

Stage `ci/publish-release.sh` only if it changed.

### Task 4: Prepare provider 0.6.0 metadata and fixtures

**Files:**
- Modify: `VERSION`
- Modify: `CHANGELOG.md`
- Modify: `pyproject.toml`
- Modify: `uv.lock`
- Modify: `tests/e2e/provider-linting/main.tf`
- Modify: `tests/e2e/provider-linting/lint.soup.toml`
- Modify: `tests/proof/fixtures/provider-linting/main.tf`
- Modify: `tests/test_release_contract.py`
- Modify: `tests/proof/test_provider_linting_proof.py`
- Modify: `docs/guides/provider-linting-proof.md`
- Modify: `ci/provider-linting-demo.sh`
- Modify: `ci/provider-linting-walkthrough.sh`
- Modify: `ci/provider_linting_proof.py`
- Delete: `provider-linting.cast`
- Delete: `provider-linting-direct-rpc.cast`

- [ ] **Step 1: Add failing 0.6.0 coordinate assertions.**

Assert `VERSION == 0.6.0`, public floors are `pyvider>=0.8.0` and
`pyvider-components>=0.8.0`, the proof dependency is exactly
`tofusoup==0.8.0`, the lock resolves all three registry releases without
path/git sources, all three provider fixtures name 0.6.0, and the 0.6.0
changelog section names seven direct paths, four OpenTofu paths, selectors,
proof artifacts, and released-dependency provenance. Assert the proof runner's
CLI version and imported `tofusoup.__version__` both equal `0.8.0`.

- [ ] **Step 2: Run them red.**

```bash
uv run pytest tests/test_release_contract.py -q
```

Expected: failures on the current 0.5.0/0.7.x coordinates.

- [ ] **Step 3: Update coordinates and lock.**

Set provider version 0.6.0, raise both dependency floors, pin the proof/dev
dependency to `tofusoup==0.8.0`, update fixture provider versions, and run:

```bash
uv lock --upgrade-package pyvider --upgrade-package pyvider-components --upgrade-package tofusoup
uv lock --check
```

Reject any non-registry source.

- [ ] **Step 4: Write the 0.6.0 changelog and guide.**

Document the seven rules and selectors, public release provenance, separate
direct/OpenTofu reachability, TofuSoup 0.8 public commands, three casts, proof
manifest, and release asset attachment. Do not describe source checkout builds
as final proof.

Replace every claim such as “OpenTofu native linting”, “OpenTofu-native
validation”, or “OpenTofu demonstrates native validation” in scripts, tests,
docs, and expected cast text. Use “OpenTofu beta validation lane” and explain
that OpenTofu executes ordinary validation RPCs. Reserve “provider-native” for
Pyvider's author-facing lint API; do not imply an OpenTofu provider-lint
transport exists.

Delete the tracked `provider-linting.cast` and
`provider-linting-direct-rpc.cast`; the schema-v3 walkthrough, direct, and
OpenTofu set supersedes them.

- [ ] **Step 5: Verify and commit without the dirty artifacts.**

```bash
uv run pytest tests/test_release_contract.py tests/proof/test_provider_linting_docs.py \
  tests/proof/test_provider_linting_proof.py -q
git add VERSION CHANGELOG.md pyproject.toml uv.lock tests/e2e/provider-linting/main.tf \
  tests/e2e/provider-linting/lint.soup.toml tests/proof/fixtures/provider-linting/main.tf \
  tests/test_release_contract.py tests/proof/test_provider_linting_proof.py \
  docs/guides/provider-linting-proof.md \
  ci/provider-linting-demo.sh ci/provider-linting-walkthrough.sh ci/provider_linting_proof.py
git add -u provider-linting.cast provider-linting-direct-rpc.cast
git commit -m "release: prepare terraform-provider-pyvider 0.6.0"
```

Expected: only the four proof artifacts remain dirty.

### Task 5: Build and record final public-artifact proof

**Files:**
- Replace after verification: the four preserved proof artifacts

- [ ] **Step 1: Run all source gates.**

```bash
uv sync --frozen --all-groups
uv run pytest -q
uv run ruff check ci tests
uv run ruff format --check ci tests
we run lint
git diff --check gh-origin/main...HEAD
```

Expected: all pass.

- [ ] **Step 2: Build exactly once from public releases.**

```bash
uv run python ci/build-provider-linting-stack.py --provider-repository . \
  --pyvider-version 0.8.0 --components-version 0.8.0 --output-dir dist
lint_binary="$PWD/dist/$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')/terraform-provider-pyvider_v0.6.0"
test -x "$lint_binary"
```

Expected: schema-v2 provenance names and hashes public 0.8.0 wheels.
This is the review candidate only. The post-merge workflow later builds the
release candidate from the exact merged SHA and its proof assets supersede this
local checkpoint for release and website claims.

- [ ] **Step 3: Run the same binary through every proof.**

```bash
tofu_cache=$(mktemp -d /tmp/pyvider-opentofu-beta.XXXXXX)
PYVIDER_OPENTOFU_BINARY=$(ci/install-opentofu-beta.sh \
  --version 1.13.0-beta1 --cache-dir "$tofu_cache")
test -x "$PYVIDER_OPENTOFU_BINARY"
export PYVIDER_OPENTOFU_BINARY
make test-conformance-binary PYVIDER_CONFORMANCE_PSP="$lint_binary"
make test-linting-opentofu-binary PYVIDER_CONFORMANCE_PSP="$lint_binary" \
  PYVIDER_OPENTOFU_BINARY="$PYVIDER_OPENTOFU_BINARY"
uvx --from tofusoup==0.8.0 soup lint tests/e2e/provider-linting/lint.soup.toml \
  --provider "$lint_binary" --lane direct
uvx --from tofusoup==0.8.0 soup lint tests/e2e/provider-linting/lint.soup.toml \
  --provider "$lint_binary" --opentofu "$PYVIDER_OPENTOFU_BINARY" --lane opentofu
```

Expected: direct 7/7 and OpenTofu four reachable paths.

- [ ] **Step 4: Regenerate and verify the three casts and manifest.**

```bash
PYVIDER_CONFORMANCE_PSP="$lint_binary" ci/record-provider-linting.sh
uv run python ci/verify-provider-linting-proof.py \
  provider-linting-proof.json provider-linting-opentofu.cast \
  provider-linting-direct.cast provider-linting-walkthrough.cast
uv run pytest tests/proof -q
```

Require versions 0.6.0/0.8.0/0.8.0/0.8.0, matching public wheel hashes and
binary hash, 7/7 direct observations, and 4/7 OpenTofu observations. Require the
OpenTofu cast at 30–36 seconds (target 34), direct cast at 33–39 (target 37),
and walkthrough at 36–40 (target 40). Compare with the backup and preserve any
truthful pacing improvement. Require the cast copy to call the second lane
“OpenTofu beta validation” and never “native linting.”

- [ ] **Step 5: Commit only the four final proof files.**

```bash
git add provider-linting-direct.cast provider-linting-opentofu.cast \
  provider-linting-walkthrough.cast provider-linting-proof.json
test "$(git diff --cached --name-only | wc -l | tr -d ' ')" = 4
git commit -m "chore: record 0.6.0 provider linting proof"
```

### Task 6: Review, merge, release, and reverify the released binary

**Files:**
- No planned source edits

- [ ] **Step 1: Obtain specification and quality approval.**

Review public-only build provenance, workflow binding, release assets, all
versions, artifact checkpoint handling, proof contents, and full test evidence.
Resolve all findings and regenerate proof if any input changes.

- [ ] **Step 2: Push and merge after checks.**

```bash
git push gh-origin codex/provider-linting
pr_url=$(gh pr create --repo provide-io/terraform-provider-pyvider --base main \
  --head codex/provider-linting --title "Release provider linting proof in v0.6.0" \
  --body "Builds and proves provider linting from released PyPI dependencies.")
gh pr checks --repo provide-io/terraform-provider-pyvider --watch
gh pr merge --repo provide-io/terraform-provider-pyvider --merge --delete-branch=false
merge_sha=$(gh pr view "$pr_url" --repo provide-io/terraform-provider-pyvider \
  --json mergeCommit --jq '.mergeCommit.oid')
test -n "$merge_sha"
```

- [ ] **Step 3: Dispatch the exact proof-producing build and publish release.**

Create an immutable branch at the merge SHA, dispatch against it, and bind both
workflows to runs created after their dispatch timestamps:

```bash
git push gh-origin "$merge_sha:refs/heads/codex/release-v0.6.0"
build_before=$(date -u +%Y-%m-%dT%H:%M:%SZ)
gh workflow run build-provider.yml --repo provide-io/terraform-provider-pyvider \
  --ref codex/release-v0.6.0 -f provider_linting_proof=true
for attempt in {1..30}; do
  build_run=$(gh run list --repo provide-io/terraform-provider-pyvider \
    --workflow build-provider.yml --event workflow_dispatch \
    --branch codex/release-v0.6.0 --limit 20 \
    --json databaseId,headSha,createdAt \
    --jq ".[] | select(.headSha == \"$merge_sha\" and .createdAt >= \"$build_before\") | .databaseId" | head -1)
  test -n "$build_run" && break
  sleep 2
done
test -n "$build_run"
gh run watch "$build_run" --repo provide-io/terraform-provider-pyvider --exit-status
gh run view "$build_run" --repo provide-io/terraform-provider-pyvider \
  --json headSha,conclusion,workflowName > /tmp/provider-build-run.json
python3 - "$merge_sha" /tmp/provider-build-run.json <<'PY'
import json, sys
run = json.load(open(sys.argv[2], encoding="utf-8"))
assert run == {"conclusion": "success", "headSha": sys.argv[1], "workflowName": "🏗️ Build Provider Binary"}
PY
gh api "repos/provide-io/terraform-provider-pyvider/actions/runs/$build_run/artifacts" \
  --jq '[.artifacts[] | select(.expired == false) | .name] | sort' \
  > /tmp/provider-build-artifacts.json
python3 - /tmp/provider-build-artifacts.json <<'PY'
import json, sys
names = set(json.load(open(sys.argv[1], encoding="utf-8")))
assert "provider-linting-proof" in names
assert any("linux_amd64" in name for name in names)
PY

release_before=$(date -u +%Y-%m-%dT%H:%M:%SZ)
gh workflow run release.yml --repo provide-io/terraform-provider-pyvider \
  --ref codex/release-v0.6.0 -f build_run_id="$build_run" -f prerelease=false
for attempt in {1..30}; do
  release_run=$(gh run list --repo provide-io/terraform-provider-pyvider \
    --workflow release.yml --event workflow_dispatch --branch codex/release-v0.6.0 \
    --limit 20 --json databaseId,headSha,createdAt \
    --jq ".[] | select(.headSha == \"$merge_sha\" and .createdAt >= \"$release_before\") | .databaseId" | head -1)
  test -n "$release_run" && break
  sleep 2
done
test -n "$release_run"
gh run watch "$release_run" --repo provide-io/terraform-provider-pyvider --exit-status
tag_object=$(gh api repos/provide-io/terraform-provider-pyvider/git/ref/tags/v0.6.0 --jq '.object.sha')
tag_type=$(gh api repos/provide-io/terraform-provider-pyvider/git/ref/tags/v0.6.0 --jq '.object.type')
if [ "$tag_type" = tag ]; then
  tag_object=$(gh api "repos/provide-io/terraform-provider-pyvider/git/tags/$tag_object" --jq '.object.sha')
fi
test "$tag_object" = "$merge_sha"
```

The exact merged-SHA build supersedes the pre-merge review proof. Require the
release workflow's `verify-release-proof` job and all checksum, signature,
provenance, and proof assets before proceeding.

- [ ] **Step 4: Download and reverify the released artifact.**

Download all `v0.6.0` assets, then independently verify the published bytes and
the recorded proof platform. The executable re-run has already occurred in the
release workflow's Ubuntu `verify-release-proof` job, where `linux_amd64` can
run natively; do not substitute a host-platform binary for that proved binary.

```bash
release_tmp=$(mktemp -d /tmp/terraform-provider-pyvider-0.6.0.XXXXXX)
gh release download v0.6.0 --repo provide-io/terraform-provider-pyvider \
  --dir "$release_tmp"
(cd "$release_tmp" && shasum -a 256 -c terraform-provider-pyvider_0.6.0_SHA256SUMS)
unzip -q "$release_tmp/terraform-provider-pyvider_0.6.0_linux_amd64.zip" \
  -d "$release_tmp/linux_amd64"
PYVIDER_RELEASE_BIN=$(find "$release_tmp/linux_amd64" -type f \
  -name 'terraform-provider-pyvider_v0.6.0' -print -quit)
test -x "$PYVIDER_RELEASE_BIN"
test "$(shasum -a 256 "$PYVIDER_RELEASE_BIN" | awk '{print $1}')" = \
  "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["provider_binary"]["sha256"])' "$release_tmp/provider-linting-proof.json")"
uv run python ci/verify-provider-linting-proof.py \
  "$release_tmp/provider-linting-proof.json" \
  "$release_tmp/provider-linting-opentofu.cast" \
  "$release_tmp/provider-linting-direct.cast" \
  "$release_tmp/provider-linting-walkthrough.cast"
```

Expected: released binary hash equals the schema-v3 manifest, the proof verifier
passes absolute downloaded paths, and the release workflow's exact-SHA
`verify-release-proof` job is green with no source-ref variables or sibling
worktree on `PYTHONPATH`.
