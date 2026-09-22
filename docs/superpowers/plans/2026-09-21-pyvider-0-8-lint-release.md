# Pyvider 0.8.0 Provider Linting Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish, merge, publish, and independently verify Pyvider 0.8.0 with provider linting as a supported public API.

**Architecture:** The implemented `pyvider.lint` model and seven validation integrations remain protocol-neutral; one compatibility adapter emits warning diagnostics until OpenTofu defines a provider-lint wire protocol. Remaining work adds the required architecture diagram and makes the built wheel, TestPyPI install, and final PyPI install all prove the public API and runner behavior before signing.

**Tech Stack:** Python 3.11+, attrs, pytest, mypy, Ruff, MkDocs/Mermaid, uv build, GitHub Releases, TestPyPI, PyPI.

---

**Repository:** `/Users/tim/.config/superpowers/worktrees/pyvider/provider-linting`
**Starting branch:** `codex/provider-linting`
**Approved design:** `docs/superpowers/specs/2026-09-21-provider-linting-release-tutorial-site-design.md`

The lint model, selector, configuration precedence, seven hooks, seven handler
integrations, fail-open runner, compatibility adapter, public guide, and their
tests are already implemented. Do not rewrite them. Review their existing
commits and limit changes to the release gaps named below.

### Task 1: Add the lint lifecycle and transport diagram

**Files:**
- Modify: `tests/lint/test_public_api.py`
- Modify: `docs/core-concepts/provider-linting.md`

- [ ] **Step 1: Write the failing documentation contract.**

Add:

```python
def test_provider_linting_documentation_diagrams_lifecycle_and_transport() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")
    expected = (
        "```mermaid",
        "Existing tfprotov6 validation RPC",
        "Decoded semantically valid configuration",
        "Provider component lint()",
        "LintSelector",
        "Fail-open runner",
        "Defensive finding filter",
        "tfprotov6 compatibility adapter",
        "TofuSoup direct lane: 7 paths",
        "OpenTofu beta validation lane: 4 paths",
        "Validation RPC response",
        "Future native adapter",
    )
    assert all(value in content for value in expected)
```

- [ ] **Step 2: Run the focused test and observe the expected failure.**

Run:

```bash
uv run pytest tests/lint/test_public_api.py::test_provider_linting_documentation_diagrams_lifecycle_and_transport -q
```

Expected: FAIL because the page has no Mermaid lifecycle diagram.

- [ ] **Step 3: Add the diagram after the authoring example.**

Add this exact conceptual flow, using Mermaid syntax already supported by the
documentation site:

```mermaid
flowchart LR
    T[TofuSoup direct lane: 7 paths] --> V[Existing tfprotov6 validation RPC]
    O[OpenTofu beta validation lane: 4 paths] --> V
    V --> C[Decoded semantically valid configuration]
    C --> R[Fail-open runner]
    S[LintSelector] --> R
    R --> H[Provider component lint()]
    H --> F[LintFinding values]
    F --> D[Defensive finding filter]
    D --> A[tfprotov6 compatibility adapter]
    A --> W[Validation warning diagnostics]
    W --> X[Validation RPC response]
    D -. same findings .-> N[Future native adapter]
```

Immediately below it, state that TofuSoup directly invokes declared validation
RPCs across provider, resource, data source, ephemeral, list, action, and state
store paths. OpenTofu reaches provider, resource, data source, and ephemeral
validation paths in this fixture. Neither client supplies provider selector
hints over tfprotov6 today.

- [ ] **Step 4: Run focused and documentation verification.**

```bash
uv run pytest tests/lint/test_public_api.py -q
we run docs.build
```

Expected: all tests pass and strict MkDocs build exits zero.

- [ ] **Step 5: Commit.**

```bash
git add tests/lint/test_public_api.py docs/core-concepts/provider-linting.md
git commit -m "docs: diagram provider linting transport"
```

### Task 2: Make release verification require the lint API

**Files:**
- Create: `scripts/verify_lint_release.py`
- Create: `tests/scripts/test_verify_lint_release.py`
- Create: `tests/scripts/test_release_workflow.py`
- Modify: `.github/workflows/release.yml`

- [ ] **Step 1: Write failing verifier tests.**

The tests must build a small wheel-shaped ZIP fixture and prove that the
verifier rejects a missing lint module, rejects a version mismatch, and accepts
an artifact containing all required paths. Add an installed-package test with a
dummy component whose async `lint()` returns one `LintFinding`; invoke
`_runner.run_lints` with its selected group and require exactly one finding and
no failure.

The wheel contents contract is:

```python
REQUIRED_WHEEL_PATHS = {
    "pyvider/lint/__init__.py",
    "pyvider/lint/model.py",
    "pyvider/lint/selector.py",
    "pyvider/lint/_runner.py",
    "pyvider/protocols/tfprotov6/handlers/_linting.py",
}
```

Use these exact public helper entry points in the tests:

```python
from scripts.verify_lint_release import REQUIRED_WHEEL_PATHS, verify_installed, verify_lint_behavior, verify_wheel


def write_wheel(tmp_path: Path, names: set[str]) -> Path:
    wheel = tmp_path / "pyvider-0.8.0-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        for name in names:
            archive.writestr(name, "")
    return wheel


def test_wheel_requires_every_lint_module(tmp_path: Path) -> None:
    wheel = write_wheel(tmp_path, REQUIRED_WHEEL_PATHS - {"pyvider/lint/model.py"})
    with pytest.raises(SystemExit, match="pyvider/lint/model.py"):
        verify_wheel(wheel)


def test_complete_wheel_contract_passes(tmp_path: Path) -> None:
    verify_wheel(write_wheel(tmp_path, REQUIRED_WHEEL_PATHS))


def test_installed_contract_runs_one_selected_finding() -> None:
    result = asyncio.run(verify_lint_behavior())
    assert result == {"version": pyvider.__version__, "findings": 1, "failed": False}


def test_installed_contract_rejects_version_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pyvider, "__version__", "0.0.0")
    with pytest.raises(SystemExit, match="expected 0.8.0"):
        asyncio.run(verify_installed(expected_version="0.8.0"))
```

- [ ] **Step 2: Write failing workflow-DAG tests.**

Parse `.github/workflows/release.yml` and assert:

- `verify-wheel` depends on the reusable build job and runs for releases and
  dry-run dispatches;
- TestPyPI publication depends on `verify-wheel`;
- TestPyPI verification invokes `scripts/verify_lint_release.py`;
- `verify-pypi` depends on PyPI publication, installs the exact tag version in
  a clean environment, and invokes the verifier with `python -I`;
- signing depends on both `verify-pypi` and `sbom`.

The test body must use `yaml.safe_load`, normalize scalar/list `needs`, and
assert the isolation controls rather than searching prose:

```python
def test_release_dag_verifies_each_published_artifact() -> None:
    jobs = load_workflow()["jobs"]
    assert needs(jobs["verify-wheel"]) == {"release"}
    assert needs(jobs["publish-testpypi"]) == {"verify-wheel"}
    assert needs(jobs["verify-testpypi"]) == {"publish-testpypi"}
    assert needs(jobs["publish-pypi"]) == {"verify-testpypi"}
    assert needs(jobs["verify-pypi"]) == {"publish-pypi"}
    assert needs(jobs["sign-and-upload"]) == {"verify-pypi", "sbom"}


@pytest.mark.parametrize("job_name", ["verify-testpypi", "verify-pypi"])
def test_registry_verification_is_isolated(job_name: str) -> None:
    rendered = json.dumps(load_workflow()["jobs"][job_name])
    assert "scripts/verify_lint_release.py" in rendered
    assert '"persist-credentials": false' in rendered
    assert "python -I" in rendered
    assert "src" not in sparse_checkout_for(job_name)
    assert "retry" in rendered.lower()
```

Define the helpers in that test module exactly as:

```python
ROOT = Path(__file__).parents[2]

def load_workflow() -> dict[str, object]:
    return yaml.safe_load((ROOT / ".github/workflows/release.yml").read_text())

def needs(job: dict[str, object]) -> set[str]:
    value = job.get("needs", [])
    return {value} if isinstance(value, str) else set(value)

def sparse_checkout_for(job_name: str) -> str:
    job = load_workflow()["jobs"][job_name]
    checkout = next(step for step in job["steps"] if step.get("uses", "").startswith("actions/checkout@"))
    return str(checkout.get("with", {}).get("sparse-checkout", ""))
```

- [ ] **Step 3: Run the new tests red.**

```bash
uv run pytest tests/scripts/test_verify_lint_release.py tests/scripts/test_release_workflow.py -q
```

Expected: FAIL because the verifier and workflow jobs do not exist.

- [ ] **Step 4: Implement the reusable release verifier.**

`scripts/verify_lint_release.py` must accept `--wheel PATH` for artifact
inspection and `--expected-version VERSION` for an installed-package check.
Implement this core exactly, adding only argparse/error-reporting boilerplate:

```python
async def verify_lint_behavior() -> dict[str, object]:
    import pyvider
    from pyvider.lint import LintContext, LintFinding, LintSelector
    from pyvider.lint._runner import run_lints

    class Component:
        async def lint(self, ctx: object) -> tuple[LintFinding, ...]:
            return (
                LintFinding(
                    rule="release/pyvider:smoke",
                    groups=("release/pyvider:all",),
                    summary="Release verifier finding",
                    detail="The public runner executed the installed lint hook.",
                    attribute_path="name",
                ),
            )

    selector = LintSelector.parse(("release/pyvider:all",))
    context = LintContext({"name": "release"}, selector)
    if not context.enabled("release/pyvider:smoke", "release/pyvider:all"):
        raise SystemExit("public LintContext selector contract failed")
    result = await run_lints(
        Component(), context.config, context.selector,
        kind="provider", name="release-smoke", operation="verify-release",
    )
    if result.failed or len(result.findings) != 1:
        raise SystemExit(f"unexpected lint result: {result!r}")
    return {"version": pyvider.__version__, "findings": 1, "failed": False}


async def verify_installed(*, expected_version: str) -> dict[str, object]:
    import pyvider
    if pyvider.__version__ != expected_version:
        raise SystemExit(f"expected {expected_version}, got {pyvider.__version__}")
    origin = Path(pyvider.__file__).resolve()
    if Path(sys.prefix).resolve() not in origin.parents:
        raise SystemExit(f"pyvider imported outside isolated environment: {origin}")
    result = await verify_lint_behavior()
    result["origin"] = str(origin)
    return result


def verify_wheel(path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        missing = REQUIRED_WHEEL_PATHS - set(archive.namelist())
    if missing:
        raise SystemExit("wheel missing: " + ", ".join(sorted(missing)))
```

The CLI serializes the returned installed result with
`print(json.dumps(result, sort_keys=True))`, so release evidence can retain the
resolved module origin without parsing prose.

- [ ] **Step 5: Wire the verifier into every release boundary.**

Add `verify-wheel` after the reusable build. It downloads the release artifact,
checks the wheel ZIP, creates a clean venv, installs that wheel, and runs the
installed check with `python -I`. Make TestPyPI publication depend on it. In
`verify-testpypi`, check out this repository's verifier, install the exact
TestPyPI version, and run it with isolated Python. Add `verify-pypi` after PyPI
publication with the same exact-version clean-install check. Make
`sign-and-upload` depend on `[verify-pypi, sbom]`.

For both registry jobs, sparse-check out only
`scripts/verify_lint_release.py`, set `persist-credentials: false`, create a
fresh `.verify-venv`, and retry registry installation for at most five minutes
to absorb index propagation. TestPyPI uses
`--index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/`;
PyPI uses `--index-url https://pypi.org/simple/`. Each successful install runs:

```bash
.verify-venv/bin/python -I scripts/verify_lint_release.py \
  --expected-version "${VERSION}"
```

The wheel job copies the verifier into its temporary venv directory before
execution, never adds the checkout `src/` to `PYTHONPATH`, and runs both
`--wheel "$wheel"` and the installed check.

- [ ] **Step 6: Run focused tests and validate workflow syntax.**

```bash
uv run pytest tests/scripts/test_verify_lint_release.py tests/scripts/test_release_workflow.py -q
uv run python -c 'import pathlib, yaml; yaml.safe_load(pathlib.Path(".github/workflows/release.yml").read_text())'
```

Expected: both commands exit zero.

- [ ] **Step 7: Commit.**

```bash
git add scripts/verify_lint_release.py tests/scripts/test_verify_lint_release.py \
  tests/scripts/test_release_workflow.py .github/workflows/release.yml
git commit -m "ci: verify lint API in release wheel"
```

### Task 3: Prepare 0.8.0 metadata and changelog

**Files:**
- Modify: `tests/scripts/test_release_workflow.py`
- Modify: `VERSION`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Add failing metadata assertions.**

Add:

```python
def test_provider_linting_is_prepared_as_0_8_0() -> None:
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == "0.8.0"
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    section = changelog.partition("## [0.8.0] - 2026-09-21")[2].partition("\n## [")[0]
    required = (
        "`LintFinding`",
        "`LintSelector`",
        "`LintContext`",
        "provider, resource, data source, ephemeral resource, list resource, action, and state store",
        "`PYVIDER_LINT`",
        "compatibility",
        "OpenTofu",
    )
    assert all(value in section for value in required)
```

- [ ] **Step 2: Run it red.**

```bash
uv run pytest tests/scripts/test_release_workflow.py::test_provider_linting_is_prepared_as_0_8_0 -q
```

Expected: FAIL because `VERSION` is `0.7.0` and no 0.8.0 section exists.

- [ ] **Step 3: Write the 0.8.0 release entry and bump the version.**

Set `VERSION` to `0.8.0`. Under `[Unreleased]`, add
`## [0.8.0] - 2026-09-21` with:

- an **Added** entry for the three public lint types and async hooks on all
  seven named surfaces;
- an **Added** entry for default-off selection, `[lint].rules`,
  `PYVIDER_LINT`, exact/group/all selectors, exclusions, and explicit empty
  disablement;
- a **Behavior** entry for fail-open execution and attribute-targeted warnings;
- a **Compatibility** entry explaining that tfprotov6 has no provider-lint
  message, so selected findings travel as ordinary validation warnings while
  OpenTofu's built-in beta remains separate;
- a **Documentation** entry for author guidance and the lifecycle diagram.
- release notes for the provide-foundation dependency floor and supply-chain
  hardening delivered since 0.7.0.

Do not claim native provider-lint protocol support.
Do not name the seven pyvider-components rule IDs; this is the framework
release, while concrete policy belongs to pyvider-components.

- [ ] **Step 4: Run focused and version tests.**

```bash
uv run pytest tests/scripts/test_release_workflow.py tests/test_version.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit.**

```bash
git add VERSION CHANGELOG.md tests/scripts/test_release_workflow.py
git commit -m "release: prepare pyvider 0.8.0"
```

### Task 4: Verify the source and built wheel

**Files:**
- No source changes expected

- [ ] **Step 1: Run focused lint verification.**

```bash
uv run pytest tests/lint tests/cli/test_lint_selector_registration.py tests/tfprotov6/handlers/test_provider_linting_contract.py tests/tfprotov6/handlers/test_provider_linting_data_source.py -q
uv run pytest tests/scripts/test_verify_lint_release.py tests/scripts/test_release_workflow.py -q
```

Expected: all tests pass.

- [ ] **Step 2: Run repository gates.**

```bash
uv lock --check
we run format.check
we run lint
we run typecheck
we run security
we run test
we run docs.build
uv run python scripts/check_doc_links.py
we run build
git diff --check gh-origin/main...HEAD
```

Expected: every command exits zero.

- [ ] **Step 3: Build and inspect the distribution.**

```bash
release_tmp=$(mktemp -d /tmp/pyvider-0.8.0-wheel.XXXXXX)
uv venv --python 3.11 "$release_tmp/venv"
wheel=$(find dist -maxdepth 1 -name 'pyvider-0.8.0-*.whl' -print -quit)
test -n "$wheel"
uv run python scripts/verify_lint_release.py --wheel "$wheel"
cp scripts/verify_lint_release.py "$release_tmp/verify_lint_release.py"
uv pip install --python "$release_tmp/venv/bin/python" "$wheel"
(cd "$release_tmp" && \
  "$release_tmp/venv/bin/python" -I verify_lint_release.py --expected-version 0.8.0)
```

Expected: clean installation and import succeed without the repository on
`PYTHONPATH`.

- [ ] **Step 4: Dispatch independent specification and quality reviews.**

Reviewers must check the approved design, `gh-origin/main...HEAD`, test output,
wheel contents, release wording, and transport claims. Resolve every finding
and repeat the affected verification.

### Task 5: Merge and publish 0.8.0

**Files:**
- No planned source edits

- [ ] **Step 1: Confirm the branch starts from current main, then exercise dry-run.**

```bash
git fetch gh-origin main
test "$(git rev-list --count HEAD..gh-origin/main)" = 0
git push gh-origin codex/provider-linting
dry_before=$(date -u +%Y-%m-%dT%H:%M:%SZ)
gh workflow run release.yml --repo provide-io/pyvider --ref codex/provider-linting
dry_head=$(git rev-parse HEAD)
for attempt in {1..150}; do
  dry_run=$(gh run list --repo provide-io/pyvider --workflow release.yml \
    --event workflow_dispatch --branch codex/provider-linting --limit 20 \
    --json databaseId,headSha,createdAt \
    --jq ".[] | select(.headSha == \"$dry_head\" and .createdAt >= \"$dry_before\") | .databaseId" | head -1)
  test -n "$dry_run" && break
  sleep 2
done
test -n "$dry_run"
gh run watch "$dry_run" --repo provide-io/pyvider --exit-status
```

Expected: the dry run builds, verifies the wheel, and produces the SBOM without
publishing to either package index.

- [ ] **Step 2: Open the release PR.**

```bash
pr_url=$(gh pr create --repo provide-io/pyvider \
  --base main --head codex/provider-linting \
  --title "Release provider linting in Pyvider 0.8.0" \
  --body-file docs/superpowers/specs/2026-09-21-provider-linting-release-tutorial-site-design.md)
test -n "$pr_url"
```

Expected: one PR URL. Attach it to the Codex task.

- [ ] **Step 3: Wait for all required checks and merge without rewriting commits.**

```bash
gh pr checks --repo provide-io/pyvider --watch
gh pr merge --repo provide-io/pyvider --merge --delete-branch=false
merge_sha=$(gh pr view "$pr_url" --repo provide-io/pyvider --json mergeCommit --jq '.mergeCommit.oid')
test -n "$merge_sha"
test "$(gh api "repos/provide-io/pyvider/contents/VERSION?ref=$merge_sha" --jq '.content' | base64 --decode | tr -d '\n')" = 0.8.0
```

Expected: required checks pass and the PR is merged.

- [ ] **Step 4: Create the GitHub release from merged `main`.**

```bash
release_before=$(date -u +%Y-%m-%dT%H:%M:%SZ)
gh release create v0.8.0 --repo provide-io/pyvider --draft \
  --target "$merge_sha" --title "Pyvider 0.8.0" --generate-notes
test "$(gh release view v0.8.0 --repo provide-io/pyvider --json isDraft,targetCommitish --jq '.isDraft')" = true
test "$(gh release view v0.8.0 --repo provide-io/pyvider --json targetCommitish --jq '.targetCommitish')" = "$merge_sha"
gh release view v0.8.0 --repo provide-io/pyvider
gh release edit v0.8.0 --repo provide-io/pyvider --draft=false
tag_object=$(gh api repos/provide-io/pyvider/git/ref/tags/v0.8.0 --jq '.object.sha')
tag_type=$(gh api repos/provide-io/pyvider/git/ref/tags/v0.8.0 --jq '.object.type')
if [ "$tag_type" = tag ]; then
  tag_object=$(gh api "repos/provide-io/pyvider/git/tags/$tag_object" --jq '.object.sha')
fi
test "$tag_object" = "$merge_sha"
```

Expected: the release event starts `.github/workflows/release.yml`.

- [ ] **Step 5: Wait for release publication and verify PyPI.**

```bash
for attempt in {1..150}; do
  release_run=$(gh run list --repo provide-io/pyvider --workflow release.yml \
    --event release --limit 20 --json databaseId,headSha,createdAt \
    --jq ".[] | select(.headSha == \"$merge_sha\" and .createdAt >= \"$release_before\") | .databaseId" | head -1)
  test -n "$release_run" && break
  sleep 2
done
test -n "$release_run"
gh run watch "$release_run" --repo provide-io/pyvider --exit-status
verify_tmp=$(mktemp -d /tmp/pyvider-0.8.0-pypi.XXXXXX)
cp scripts/verify_lint_release.py "$verify_tmp/"
(cd "$verify_tmp" && \
  uv run --isolated --no-project --refresh --index https://pypi.org/simple \
    --with pyvider==0.8.0 python -I verify_lint_release.py \
    --expected-version 0.8.0 | tee verifier-result.json)
```

Expected: the workflow is green and the final line is
`pyvider 0.8.0 lint API verified`.

- [ ] **Step 6: Record immutable release evidence.**

Run the following from a fresh evidence directory:

```bash
evidence_tmp=$(mktemp -d /tmp/pyvider-0.8.0-evidence.XXXXXX)
curl --fail --silent --show-error https://pypi.org/pypi/pyvider/0.8.0/json \
  > "$evidence_tmp/pypi.json"
python3 - "$evidence_tmp/pypi.json" "$evidence_tmp" <<'PY'
import hashlib, json, pathlib, sys, urllib.request
payload = json.load(open(sys.argv[1], encoding="utf-8"))
out = pathlib.Path(sys.argv[2])
assert payload["info"]["version"] == "0.8.0"
assert {item["packagetype"] for item in payload["urls"]} == {"bdist_wheel", "sdist"}
for item in payload["urls"]:
    target = out / item["filename"]
    urllib.request.urlretrieve(item["url"], target)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == item["digests"]["sha256"]
PY
gh release download v0.8.0 --repo provide-io/pyvider --dir "$evidence_tmp/github"
gh release view v0.8.0 --repo provide-io/pyvider \
  --json isDraft,targetCommitish,assets > "$evidence_tmp/github-release.json"
python3 - "$evidence_tmp/github-release.json" <<'PY'
import hashlib, json, pathlib, sys
release = json.load(open(sys.argv[1], encoding="utf-8"))
assert release["isDraft"] is False
names = {asset["name"] for asset in release["assets"]}
expected = {
    "pyvider-0.8.0-py3-none-any.whl",
    "pyvider-0.8.0-py3-none-any.whl.sigstore.json",
    "pyvider-0.8.0.tar.gz",
    "pyvider-0.8.0.tar.gz.sigstore.json",
    "v0.8.0.sbom.cdx.json",
    "v0.8.0.sbom.cdx.json.sigstore.json",
    "v0.8.0.tar.gz",
    "v0.8.0.tar.gz.sigstore.json",
    "v0.8.0.zip",
    "v0.8.0.zip.sigstore.json",
}
assert names == expected
root = pathlib.Path(sys.argv[1]).parent
for name in ("pyvider-0.8.0-py3-none-any.whl", "pyvider-0.8.0.tar.gz"):
    assert hashlib.sha256((root / name).read_bytes()).digest() == hashlib.sha256((root / "github" / name).read_bytes()).digest()
PY
```

Record `merge_sha`, tag target, `release_run`, the two PyPI filenames and
SHA-256 values, exact GitHub asset names, and `origin` from
`$verify_tmp/verifier-result.json` in
`/tmp/pyvider-provider-lint-release-coordinates.json` using a small JSON update
that preserves the other repository keys.
