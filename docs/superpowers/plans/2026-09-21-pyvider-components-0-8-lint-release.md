# pyvider-components 0.8.0 Lint Rules Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish pyvider-components 0.8.0 with seven documented, tested provider-lint rules built against the released Pyvider 0.8.0 API.

**Architecture:** Rule implementations remain pure component hooks and import only Pyvider's public lint types. Release work raises the public dependency floor, removes obsolete typing suppressions, hardens wheel verification across all seven rules, and publishes only after a clean installation proves the complete policy set is present.

**Tech Stack:** Python 3.11+, Pyvider 0.8.0, pytest, Plating, MkDocs/Mermaid, uv, PyPI/TestPyPI, GitHub Releases.

---

**Repository:** `/Users/tim/.config/superpowers/worktrees/pyvider-components/provider-linting`
**Starting branch:** `codex/provider-linting`

All seven hooks, rule constants, component templates, generated docs, and rule
tests are already implemented. Preserve them and address only the release gaps.

### Task 1: Pin the public framework contract and wheel smoke

**Files:**
- Create: `tests/test_lint_release_contract.py`
- Modify: `pyproject.toml`
- Modify: `uv.lock`
- Modify: `.github/workflows/release.yml`
- Modify: `src/pyvider/components/provider.py`
- Modify: `src/pyvider/components/data_sources/http_api.py`
- Modify: `src/pyvider/components/ephemerals/lease.py`
- Modify: `src/pyvider/components/list_resources/file_contents.py`
- Modify: `src/pyvider/components/actions/wait_for_file.py`
- Modify: `src/pyvider/components/state_stores/filesystem_store.py`

- [ ] **Step 1: Add failing dependency and workflow assertions.**

```python
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_lint_release_requires_pyvider_0_8() -> None:
    project = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"pyvider>=0.8.0"' in project


def test_release_wheel_smoke_imports_lint_rules() -> None:
    workflow = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    for rule in (
        "INSECURE_TLS", "WORLD_WRITABLE_DIRECTORY", "INSECURE_HTTP",
        "LONG_LIVED_LEASE", "INCLUDE_HIDDEN_FILES",
        "LONG_ACTION_TIMEOUT", "RELATIVE_STATE_STORE_PATH",
    ):
        assert rule in workflow
    assert "LintContext" in workflow
    assert "LintSelector" in workflow
    assert "PyviderProvider" in workflow
    assert "asyncio.run" in workflow
```

- [ ] **Step 2: Run both tests red.**

```bash
uv run pytest tests/test_lint_release_contract.py -q
```

Expected: failures because the floor is 0.7.0 and the workflow imports only the
package root.

- [ ] **Step 3: Raise the floor and regenerate the lock.**

Change the runtime dependency to `pyvider>=0.8.0`, then run:

```bash
uv lock --upgrade-package pyvider
```

Require the resolved Pyvider version to be at least 0.8.0 and from the public
index, with no `[tool.uv.sources]` path override.

- [ ] **Step 4: Remove obsolete lint-group typing suppressions.**

Delete only the six `# type: ignore[arg-type]  # attrs converter typing`
comments on lint `groups=` declarations in the files listed above. Pyvider 0.8
provides the corrected public type, so each line must pass mypy without a local
suppression.

- [ ] **Step 5: Strengthen the TestPyPI verification command.**

The smoke must import all seven constants, construct public `LintContext` and
`LintSelector` values, and directly await `PyviderProvider().lint(...)` with
`SimpleNamespace(api_insecure_skip_verify=True)`, requiring one result whose
rule equals `INSECURE_TLS`. Do not import private `pyvider.lint._runner`; a
root-package import alone is not sufficient.

- [ ] **Step 6: Run tests, typecheck, lowest-direct resolution, and commit.**

```bash
uv run pytest tests/test_lint_release_contract.py tests/test_provider_lint_rules_security.py tests/test_provider_lint_rules_reliability.py -q
we run typecheck
normal_lock=$(mktemp /tmp/pyvider-components-normal-lock.XXXXXX)
cp uv.lock "$normal_lock"
uv lock --resolution lowest-direct
uv run pytest tests/test_provider_lint_rules_security.py tests/test_provider_lint_rules_reliability.py -q
cp "$normal_lock" uv.lock
uv lock --check
git add tests/test_lint_release_contract.py pyproject.toml uv.lock .github/workflows/release.yml \
  src/pyvider/components/provider.py src/pyvider/components/data_sources/http_api.py \
  src/pyvider/components/ephemerals/lease.py \
  src/pyvider/components/list_resources/file_contents.py \
  src/pyvider/components/actions/wait_for_file.py \
  src/pyvider/components/state_stores/filesystem_store.py
git commit -m "build: require pyvider 0.8 lint API"
```

Expected: both normal and declared-floor rule suites pass.

### Task 2: Prepare 0.8.0 release metadata

**Files:**
- Modify: `tests/test_lint_release_contract.py`
- Modify: `VERSION`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Add the failing release metadata test.**

```python
def test_lint_rules_are_prepared_as_0_8_0() -> None:
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == "0.8.0"
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    section = changelog.partition("## [0.8.0] - 2026-09-21")[2].partition("\n## [")[0]
    for rule in (
        "insecure-tls", "world-writable-directory", "insecure-http",
        "long-lived-lease", "include-hidden-files", "long-action-timeout",
        "relative-state-store-path",
    ):
        assert rule in section
```

- [ ] **Step 2: Run it red.**

```bash
uv run pytest tests/test_lint_release_contract.py::test_lint_rules_are_prepared_as_0_8_0 -q
```

Expected: FAIL on version 0.7.2 and the absent section.

- [ ] **Step 3: Bump and document the release.**

Set `VERSION` to `0.8.0`. Add a dated 0.8.0 section naming all seven rules,
their seven surfaces, default-off/selectable behavior inherited from Pyvider,
unknown-safe pure hooks, attribute paths, exact suppression syntax, and the
Pyvider 0.8.0 runtime floor. State that direct seven-path coverage and OpenTofu
reachability are different facts.

- [ ] **Step 4: Verify and commit.**

```bash
uv run pytest tests/test_lint_release_contract.py -q
git add VERSION CHANGELOG.md tests/test_lint_release_contract.py
git commit -m "release: prepare pyvider-components 0.8.0"
```

### Task 3: Run release gates and inspect a clean wheel

**Files:**
- No source changes expected

- [ ] **Step 1: Regenerate docs and require a clean result.**

Run the exact checked Plating command used by its docs contract, then:

```bash
uv run python scripts/generate-component-docs.py --output-dir docs
git diff --exit-code -- docs mkdocs.yml
```

Expected: no generated documentation or navigation changes.

- [ ] **Step 2: Run all gates and build.**

```bash
uv lock --check
uv sync --frozen --all-groups
uv run pytest -q
we run format.check
we run lint
we run typecheck
we run docs.build
uv build
git diff --check gh-origin/main...HEAD
```

Expected: every command exits zero.

- [ ] **Step 3: Install the built wheel in isolation.**

```bash
release_tmp=$(mktemp -d /tmp/pyvider-components-0.8.0-wheel.XXXXXX)
uv venv --python 3.11 "$release_tmp/venv"
wheel=$(find dist -maxdepth 1 -name 'pyvider_components-0.8.0-*.whl' -print -quit)
test -n "$wheel"
uv pip install --python "$release_tmp/venv/bin/python" "$wheel"
"$release_tmp/venv/bin/python" -I -c 'import asyncio; from types import SimpleNamespace; import pyvider, pyvider.components; from pyvider.lint import LintContext, LintSelector; from pyvider.components.provider import PyviderProvider; from pyvider.components.lint_rules import ALL, INSECURE_TLS, WORLD_WRITABLE_DIRECTORY, INSECURE_HTTP, LONG_LIVED_LEASE, INCLUDE_HIDDEN_FILES, LONG_ACTION_TIMEOUT, RELATIVE_STATE_STORE_PATH; assert pyvider.__version__ == "0.8.0"; assert pyvider.components.__version__ == "0.8.0"; assert len({INSECURE_TLS, WORLD_WRITABLE_DIRECTORY, INSECURE_HTTP, LONG_LIVED_LEASE, INCLUDE_HIDDEN_FILES, LONG_ACTION_TIMEOUT, RELATIVE_STATE_STORE_PATH}) == 7; findings = asyncio.run(PyviderProvider().lint(LintContext(SimpleNamespace(api_insecure_skip_verify=True), LintSelector.parse((ALL,))))); assert len(findings) == 1 and findings[0].rule == INSECURE_TLS'
```

Expected: import succeeds without a sibling source checkout.

- [ ] **Step 4: Obtain specification and quality approval.**

Require independent review of all seven rule implementations, docs, dependency
floor, wheel contents, and release language. Resolve findings and rerun gates.

### Task 4: Merge and publish 0.8.0

**Files:**
- No planned source edits

- [ ] **Step 1: Push, open, check, and merge the PR.**

```bash
git push gh-origin codex/provider-linting
pr_url=$(gh pr create --repo provide-io/pyvider-components --base main --head codex/provider-linting \
  --title "Release provider lint rules in pyvider-components 0.8.0" \
  --body "Adds seven tested provider-lint rules on the public Pyvider 0.8.0 API.")
gh pr checks --repo provide-io/pyvider-components --watch
gh pr merge --repo provide-io/pyvider-components --merge --delete-branch=false
release_sha=$(gh pr view "$pr_url" --repo provide-io/pyvider-components \
  --json mergeCommit --jq '.mergeCommit.oid')
test -n "$release_sha"
```

Expected: PR merged after all checks pass.

- [ ] **Step 2: Create and wait for the release.**

```bash
release_before=$(date -u +%Y-%m-%dT%H:%M:%SZ)
gh release create v0.8.0 --repo provide-io/pyvider-components --target "$release_sha" \
  --title "pyvider-components 0.8.0" --generate-notes
tag_object=$(gh api repos/provide-io/pyvider-components/git/ref/tags/v0.8.0 --jq '.object.sha')
tag_type=$(gh api repos/provide-io/pyvider-components/git/ref/tags/v0.8.0 --jq '.object.type')
if [ "$tag_type" = tag ]; then
  tag_object=$(gh api "repos/provide-io/pyvider-components/git/tags/$tag_object" --jq '.object.sha')
fi
test "$tag_object" = "$release_sha"
for attempt in {1..150}; do
  release_run=$(gh run list --repo provide-io/pyvider-components --workflow release.yml \
    --event release --limit 20 --json databaseId,headSha,createdAt \
    --jq ".[] | select(.headSha == \"$release_sha\" and .createdAt >= \"$release_before\") | .databaseId" | head -1)
  test -n "$release_run" && break
  sleep 2
done
test -n "$release_run"
gh run watch "$release_run" --repo provide-io/pyvider-components --exit-status
```

Expected: release workflow green.

- [ ] **Step 3: Verify PyPI independently.**

```bash
verify_tmp=$(mktemp -d /tmp/pyvider-components-0.8.0-pypi.XXXXXX)
(cd "$verify_tmp" && uv run --isolated --no-project --refresh --index https://pypi.org/simple \
  --with pyvider-components==0.8.0 python -I -c 'import asyncio; from types import SimpleNamespace; import pyvider, pyvider.components; from pyvider.lint import LintContext, LintSelector; from pyvider.components.provider import PyviderProvider; from pyvider.components.lint_rules import ALL, INSECURE_TLS, WORLD_WRITABLE_DIRECTORY, INSECURE_HTTP, LONG_LIVED_LEASE, INCLUDE_HIDDEN_FILES, LONG_ACTION_TIMEOUT, RELATIVE_STATE_STORE_PATH; assert pyvider.__version__ == "0.8.0"; assert pyvider.components.__version__ == "0.8.0"; assert len({INSECURE_TLS, WORLD_WRITABLE_DIRECTORY, INSECURE_HTTP, LONG_LIVED_LEASE, INCLUDE_HIDDEN_FILES, LONG_ACTION_TIMEOUT, RELATIVE_STATE_STORE_PATH}) == 7; findings = asyncio.run(PyviderProvider().lint(LintContext(SimpleNamespace(api_insecure_skip_verify=True), LintSelector.parse((ALL,))))); assert len(findings) == 1 and findings[0].rule == INSECURE_TLS; print("pyvider-components 0.8.0 lint rules verified")'
curl --fail --silent --show-error https://pypi.org/pypi/pyvider-components/0.8.0/json > pypi.json
python3 - <<'PY'
import json, urllib.request, hashlib
payload = json.load(open("pypi.json", encoding="utf-8"))
assert payload["info"]["version"] == "0.8.0"
for item in payload["urls"]:
    data = urllib.request.urlopen(item["url"]).read()
    assert hashlib.sha256(data).hexdigest() == item["digests"]["sha256"]
PY
)
```

Expected: printed verification line and exit zero. Record commit, tag, run ID,
wheel filename, and checksum in the release ledger.
