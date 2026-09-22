# Provider Linting Site, Staging, and Production Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish accurate Pyvider 0.8.0 linting documentation, Tutorial Part 7, released proof artifacts, and the same verified commit to Cloudflare staging and production.

**Architecture:** One site data value owns the current Pyvider version. Provider and tutorial proof artifacts are independently verified before Hugo renders them; deployment uses a fail-closed branch/SHA gate, immutable preview smoke, exact-directory production promotion, and a tested rollback path.

**Tech Stack:** Hugo, Python stdlib tests/checkers, MkDocs baked output, asciinema-player, GitHub artifacts, Cloudflare Pages/Wrangler 4.101.0 and Pages API.

---

**Repository:** `/Users/tim/.config/superpowers/worktrees/site-pyvider-com/provider-linting`
**Starting branch:** `codex/provider-linting`
**Cloudflare project:** `pyvider-one`
**Cloudflare account:** `mindtenet` (`e2d28194f1bca547163391790d66e51f`)
**Production branch:** `main`

Preserve untracked `.superpowers/`, `scripts/__pycache__/`, and
`tests/__pycache__/`; never stage them.

### Task 1: Centralize the current Pyvider version

**Files:**
- Create: `data/versions.toml`
- Create: `layouts/shortcodes/current-pyvider-version.html`
- Create: `tests/test_current_version.py`
- Modify: `content/tutorials/actions-and-list-resources.md`

- [ ] **Step 1: Write the failing version-source tests.**

```python
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).parents[1]


class CurrentVersionTests(unittest.TestCase):
    def test_current_pyvider_version_has_one_structured_source(self) -> None:
        values = tomllib.loads((ROOT / "data/versions.toml").read_text(encoding="utf-8"))
        self.assertEqual(values["pyvider"]["current"], "0.8.0")

    def test_part6_uses_current_version_shortcode(self) -> None:
        source = (ROOT / "content/tutorials/actions-and-list-resources.md").read_text(encoding="utf-8")
        self.assertIn("introduced in Pyvider 0.5", source)
        self.assertIn('{{< current-pyvider-version >}}', source)
        self.assertNotIn("implemented in pyvider 0.5 today", source)
```

- [ ] **Step 2: Run red.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_current_version -v
```

Expected: missing data/shortcode and stale Part 6 copy failures.

- [ ] **Step 3: Add the data and shortcode.**

```toml
[pyvider]
current = "0.8.0"
```

The shortcode renders only `{{ .Site.Data.versions.pyvider.current }}` with
whitespace trimmed. Change Part 6 to:

```text
Actions and list resources were introduced in Pyvider 0.5 and are available in Pyvider {{< current-pyvider-version >}} today.
```

- [ ] **Step 4: Test rendered output and commit.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_current_version -v
version_public=$(mktemp -d /tmp/pyvider-current-version.XXXXXX)
hugo --environment production --minify --destination "$version_public"
rg -F "available in Pyvider 0.8.0 today" "$version_public/tutorials/actions-and-list-resources/index.html"
git add data/versions.toml layouts/shortcodes/current-pyvider-version.html \
  tests/test_current_version.py content/tutorials/actions-and-list-resources.md
git commit -m "feat: centralize current Pyvider version"
```

### Task 2: Publish Tutorial Part 7 and its proof

**Files:**
- Create: `content/tutorials/provider-linting.md`
- Create: `static/casts/tutorial-part7-provider-linting.cast`
- Create: `static/proofs/tutorial-part7-provider-linting-proof.json`
- Create: `scripts/verify-tutorial-provider-linting-proof.py`
- Modify: `tests/test_content_architecture.py`
- Modify: `scripts/check-content-architecture.py`
- Create or modify: `tests/test_tutorial_provider_linting.py`

- [ ] **Step 1: Write failing source/proof contracts.**

Require front matter with weight 7, series `Building a Provider from Scratch`,
alias `/posts/provider-linting/`, the exact rule ID, author-hook example, public
test/package/TofuSoup commands, enable/exclude/disable examples, and links to:

```text
/linting/
/docs/core-concepts/provider-linting/
/changelog/pyvider-0-8-0-release/
```

Require the proof verifier to reject a wrong public artifact SHA, a source
commit that is not its ancestor, public package
versions, binary/cast hash, geometry other than 120×40, duration outside 35–40 seconds,
missing commands, and non-empty excluded/disabled diagnostics.

- [ ] **Step 2: Run red.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_tutorial_provider_linting tests.test_content_architecture -v
```

Expected: missing page, verifier, cast, and proof failures.

- [ ] **Step 3: Implement the independent verifier.**

Use only the Python standard library. Require exact 120×40 geometry. Validate the tutorial proof schema,
recompute the cast SHA, parse every asciicast event, strip ANSI controls, and
assert the six public commands and enabled/direct/OpenTofu/excluded/disabled
outcomes. Reject absolute user paths and token-like values. Accept separate
`--expected-source-sha` and `--artifact-sha` coordinates; query the public
GitHub compare API and require the source commit to be equal to or an ancestor
of the artifact commit.

- [ ] **Step 4: Copy only verified tutorial artifacts.**

Read `tutorial.artifact_commit` from the release ledger and fetch both files
from `provide-io/pyvider-tutorial` at that exact merged public SHA with `gh api`
or raw GitHub content URLs. Do not copy from a local tutorial worktree. Verify
the returned commit identity and bytes with the tutorial verifier, install the
identical bytes into the two static destinations, then rerun the site's
independent verifier with both source and artifact coordinates.

- [ ] **Step 5: Write the tutorial page.**

Use natural instructional prose, not protocol caveats as the opening. Explain
why the production-name rule is advisory, show its TDD implementation, then
package and run the two lanes. State precisely:

- direct TofuSoup proves the provider hook;
- OpenTofu 1.13.0-beta1 runs its built-in lint mode alongside ordinary provider
  validation warnings;
- no provider-lint selection protocol has been released;
- idle recording gaps were shortened and results held for readability.

Embed the Part 7 cast at 120×40 and keep playback responsive.

- [ ] **Step 6: Verify and commit.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_tutorial_provider_linting tests.test_content_architecture -v
git add content/tutorials/provider-linting.md static/casts/tutorial-part7-provider-linting.cast \
  static/proofs/tutorial-part7-provider-linting-proof.json \
  scripts/verify-tutorial-provider-linting-proof.py \
  tests/test_tutorial_provider_linting.py tests/test_content_architecture.py \
  scripts/check-content-architecture.py
git commit -m "docs: publish provider linting tutorial"
```

### Task 3: Add the detailed Pyvider 0.8.0 changelog

**Files:**
- Create: `content/changelog/pyvider-0-8-0-release.md`
- Modify: `tests/test_content_architecture.py`
- Modify: `scripts/check-content-architecture.py`

- [ ] **Step 1: Add failing inventory assertions.**

Query `gh release view v0.8.0 --repo provide-io/pyvider --json publishedAt,url`
and derive the calendar date from `publishedAt`; do not assume the planning
date. Add 0.8.0 with that verified date as the newest detailed release. Require release URL,
public lint API, selector controls, seven framework surfaces, fail-open behavior,
compatibility boundary, migration note, tutorial link, and Pyvider API docs
link. Update homepage/latest-release expectations from 0.7.0 to 0.8.0 while
retaining detailed 0.6+ entries and consolidated 0.3–0.5 history.

- [ ] **Step 2: Run red, write the page, then run green.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_content_architecture -v
```

The page must describe Pyvider's framework, not claim that its wheel contains
the seven concrete pyvider-components rules.

- [ ] **Step 3: Commit.**

```bash
git add content/changelog/pyvider-0-8-0-release.md \
  tests/test_content_architecture.py scripts/check-content-architecture.py
git commit -m "docs: add Pyvider 0.8.0 release notes"
```

### Task 4: Sync the released provider proof and correct lane language

**Files:**
- Modify: `scripts/verify-provider-linting-proof.py`
- Modify: `scripts/sync-provider-linting-proof.py`
- Modify: `tests/test_provider_linting_proof.py`
- Modify: `tests/test_linting_site.py`
- Modify: `scripts/check-linting-site.py`
- Modify: `tests/test_linting_preview_smoke.py`
- Modify: `scripts/smoke-linting-preview.py`
- Modify: `content/linting.md`
- Modify: `layouts/partials/linting.html`
- Replace: `static/proofs/provider-linting-proof.json`
- Replace: `static/casts/provider-linting-opentofu.cast`
- Replace: `static/casts/provider-linting-direct.cast`
- Replace: `static/casts/provider-linting-walkthrough.cast`
- Delete: `static/casts/provider-linting-direct-rpc.cast`

- [ ] **Step 1: Add failing schema-v3/public-release assertions.**

Require provider 0.6.0, Pyvider 0.8.0, pyvider-components 0.8.0, public wheel
filenames/hashes, released provider binary hash, exact proof workflow run ID,
three current casts, 7/7 direct paths, and four OpenTofu paths. Reject the
legacy direct-RPC cast.

- [ ] **Step 2: Add failing language assertions.**

Require “OpenTofu beta validation lane” and “ordinary validation RPCs”. Reject
“OpenTofu native linting”, “OpenTofu-native validation”, and any wording that
implies a released provider-lint protocol.

- [ ] **Step 3: Run red.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_provider_linting_proof tests.test_linting_site \
  tests.test_linting_preview_smoke -v
```

- [ ] **Step 4: Update verifier/sync/content contracts.**

Migrate the site verifier to provider proof schema 3 and its public dependency
and build-provenance fields. Retain transactional sync. Remove legacy destinations from current sync
while preserving compatibility tests only where needed to reject stale input.
Update all visible/checker language to the approved beta-validation wording.

- [ ] **Step 5: Sync from the public provider release.**

```bash
python3 scripts/sync-provider-linting-proof.py \
  --repository provide-io/terraform-provider-pyvider \
  --release v0.6.0 \
  --expected-provider-sha "$PROVIDER_RELEASE_SHA"
```

The script downloads the schema-v3 manifest, build provenance, and three casts
from immutable GitHub Release assets—not an expiring Actions artifact. It keeps
the numeric workflow run only as verified provenance inside the manifest.
Expected: only the manifest and three current casts change; all independently
verify. Delete the obsolete direct-RPC cast after tests prove no reference.

- [ ] **Step 6: Add dated upstream status.**

State that the recording uses 1.13.0-beta1 and that, as of 2026-09-21, the
newest 1.13 prerelease is `v1.13.0-rc1`. Verify that exact tag and its
`publishedAt` through `gh release view v1.13.0-rc1 --repo opentofu/opentofu`
and inspect the upstream linting RFC/implementation before writing. Describe
provider transport as unreleased unless that source verification proves
otherwise. Avoid timeless “current OpenTofu” language.

- [ ] **Step 7: Verify and commit.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_provider_linting_proof tests.test_linting_site \
  tests.test_linting_preview_smoke -v
git add content/linting.md layouts/partials/linting.html scripts tests \
  static/proofs/provider-linting-proof.json static/casts/provider-linting-opentofu.cast \
  static/casts/provider-linting-direct.cast static/casts/provider-linting-walkthrough.cast
git add -u static/casts/provider-linting-direct-rpc.cast
git commit -m "build: sync released provider lint proof"
```

### Task 5: Refresh baked Pyvider 0.8.0 API docs

**Files:**
- Replace generated files under: `static/docs/`
- Verify: `static/docs/core-concepts/provider-linting/index.html`

- [ ] **Step 1: Build docs from public tag `v0.8.0`.**

Use the public tag archive—not the feature worktree—and an explicit staging
directory:

```bash
docs_tmp=$(mktemp -d /tmp/pyvider-0.8.0-docs.XXXXXX)
gh release download v0.8.0 --repo provide-io/pyvider --archive=tar.gz \
  --dir "$docs_tmp"
docs_archive=$(find "$docs_tmp" -maxdepth 1 -name '*.tar.gz' -print -quit)
tar -xzf "$docs_archive" -C "$docs_tmp"
docs_source=$(find "$docs_tmp" -maxdepth 1 -type d -name 'pyvider-*' -print -quit)
docs_build="$docs_tmp/site"
(cd "$docs_source" && uv sync --frozen --only-group docs && \
  uv run mkdocs build --strict --site-dir "$docs_build")
test -f "$docs_build/core-concepts/provider-linting/index.html"
rsync -a --delete --exclude 'overrides/' "$docs_build/" static/docs/
```

The `--delete` removes stale generated pages while the exclusion preserves the
site-owned canonical `static/docs/overrides/main.html`. Assert that override's
checksum is unchanged before header synchronization.

- [ ] **Step 2: Synchronize and check the shared header.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/sync-baked-docs-header.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/sync-baked-docs-header.py --check
```

Require `/docs/core-concepts/provider-linting/`, the Mermaid diagram, version
0.8.0, matching header geometry, and no worktree path leakage.

- [ ] **Step 3: Run content tests and commit generated docs.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_content_architecture -v
git add static/docs
git commit -m "docs: refresh Pyvider 0.8 API documentation"
```

### Task 6: Add tested staging, production, and rollback gates

**Files:**
- Create: `scripts/smoke-site-deployment.py`
- Create: `scripts/deploy-site.py`
- Create: `scripts/rollback-pages-deployment.py`
- Create: `tests/test_site_deployment.py`
- Modify: `docs/deployment.md`

- [ ] **Step 1: Write failing deployment tests.**

Using local HTTP/API fixtures, require:

- staging and production smoke cover `/`, `/linting/`,
  `/tutorials/provider-linting/`, `/changelog/pyvider-0-8-0-release/`, both proof
  manifests, all four current casts, and
  `/docs/core-concepts/provider-linting/`;
- redirects remain on the expected host;
- production deploy accepts only the exact staging-tested commit and build
  directory checksum;
- rollback calls
  `POST /accounts/{account}/pages/projects/{project}/deployments/{id}/rollback`;
- rollback success checks the restored Cloudflare deployment identity and a
  legacy-safe `/` health response, not new Part 7 routes absent from the old
  deployment;
- missing/mismatched account, token, previous deployment, or commit fails
  closed.

- [ ] **Step 2: Run red.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_site_deployment -v
```

- [ ] **Step 3: Implement stdlib smoke, deployment, and rollback clients.**

All scripts require explicit arguments and timeouts. `deploy-site.py` computes a
deterministic SHA-256 over sorted relative paths plus file bytes, supports
`--print-checksum`, and before invoking pinned Wrangler requires its recomputed
value to equal `--expected-checksum`. It also requires explicit project, branch,
and source SHA. The rollback script reads
`CLOUDFLARE_API_TOKEN` only from the environment, never logs it, posts to the
official endpoint, and verifies the returned deployment identity.

- [ ] **Step 4: Document the exact deployment sequence.**

Update `docs/deployment.md` for:

```bash
export CLOUDFLARE_ACCOUNT_ID=e2d28194f1bca547163391790d66e51f
```

Capture the previous production deployment ID before staging. Build one fresh
directory, checksum it, deploy it to the feature branch, smoke it, then deploy
that unchanged directory with `--branch main --commit-hash "$source_sha"`.
On failed production smoke, immediately call the tested rollback script with
the captured previous deployment ID.

- [ ] **Step 5: Run tests and commit.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_site_deployment -v
git add scripts/smoke-site-deployment.py scripts/deploy-site.py scripts/rollback-pages-deployment.py \
  tests/test_site_deployment.py docs/deployment.md
git commit -m "ci: gate staging production and rollback"
```

### Task 7: Verify, stage, inspect, and publish production

**Files:**
- No content changes after the verified build directory is created

- [ ] **Step 1: Run complete local verification.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/sync-baked-docs-header.py --check
python3 scripts/verify-provider-linting-proof.py \
  static/proofs/provider-linting-proof.json \
  static/casts/provider-linting-opentofu.cast \
  static/casts/provider-linting-direct.cast \
  static/casts/provider-linting-walkthrough.cast
python3 scripts/verify-tutorial-provider-linting-proof.py \
  static/proofs/tutorial-part7-provider-linting-proof.json \
  static/casts/tutorial-part7-provider-linting.cast \
  --expected-source-sha "$TUTORIAL_SOURCE_SHA" \
  --artifact-sha "$TUTORIAL_ARTIFACT_SHA"
deploy_dir=$(mktemp -d /tmp/pyvider-site-release.XXXXXX)
hugo --environment production --minify --destination "$deploy_dir"
python3 scripts/check-content-architecture.py "$deploy_dir"
python3 scripts/check-linting-site.py "$deploy_dir"
deploy_checksum=$(python3 scripts/deploy-site.py --print-checksum \
  --directory "$deploy_dir")
test -n "$deploy_checksum"
```

Expected: all pass. Inspect desktop plus 1024, 768, and 390 pixel widths for
header consistency, navigation visibility, command wrapping, and cast framing.
Read `TUTORIAL_SOURCE_SHA` and `TUTORIAL_ARTIFACT_SHA` from the verified release
ledger before running; the verifier requires both.

- [ ] **Step 2: Obtain final specification and visual quality approval.**

Require reviewers to compare the design, proof manifests, rendered site, and
responsive screenshots. Resolve every finding before deployment.

- [ ] **Step 3: Push the exact candidate and deploy staging.**

Require clean tracked status, push branch, verify remote SHA equals HEAD, set
the known account ID, capture current production deployment, run the existing
preview target gate, and deploy `deploy_dir` with the feature branch and exact
commit hash through `scripts/deploy-site.py --expected-checksum
"$deploy_checksum"` using Wrangler 4.101.0.

- [ ] **Step 4: Smoke and inspect the immutable preview.**

Run both existing lint smoke and the new whole-site smoke against the immutable
preview URL. Inspect desktop and 390px browser views. Record preview URL, source
SHA, build-directory checksum, proof hashes, and smoke output.

- [ ] **Step 5: Satisfy the rollback credential gate.**

Before production, require `CLOUDFLARE_API_TOKEN` with Pages Write and perform a
non-destructive API authentication check. If no such token is available, stop
after staging and report this single production blocker; do not deploy
production without the approved rollback capability.

- [ ] **Step 6: Fast-forward site `main` and deploy the unchanged directory.**

Fast-forward only after checks and do not create a merge commit:

```bash
source_sha=$(git rev-parse HEAD)
git fetch gh-origin main
git merge-base --is-ancestor gh-origin/main "$source_sha"
git push gh-origin "$source_sha:refs/heads/main"
remote_main=$(git ls-remote gh-origin refs/heads/main | awk '{print $1}')
test "$remote_main" = "$source_sha"
test "$STAGING_SOURCE_SHA" = "$source_sha"
python3 scripts/deploy-site.py --directory "$deploy_dir" \
  --expected-checksum "$deploy_checksum" --project pyvider-one \
  --branch main --source-sha "$source_sha"
```

Query the resulting Cloudflare deployment and require its source commit,
remote `main`, local `source_sha`, and staging metadata to be identical. Do not
rebuild between environments.

- [ ] **Step 7: Smoke production or roll back.**

Run the whole-site smoke against `https://pyvider.com/`. If any assertion fails,
call the rollback script with the captured previous production deployment ID,
verify the restored Cloudflare deployment ID/custom-domain target plus a
legacy-safe `/` health check, and report failure. Do not run the new-release
route set against the rolled-back deployment because it legitimately lacks
Part 7. If all pass, record the production deployment ID and final release
coordinates.
