# Provider Linting Release Train Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish provider linting through the complete public chain—framework, reusable rules, packaged provider, TofuSoup proof, tutorial, website staging, and production.

**Architecture:** Six repository-scoped plans produce independently testable artifacts. This orchestration plan enforces their dependency order and records immutable release coordinates so no downstream proof can fall back to a worktree.

**Tech Stack:** Python 3.11+, uv, pytest, PyPI/TestPyPI, GitHub Actions/Releases, Flavorpack, TofuSoup, OpenTofu 1.13.0-beta1, Hugo, asciinema casts, Cloudflare Pages.

---

## Plan suite and worktrees

Execute these plans in order:

1. `docs/superpowers/plans/2026-09-21-pyvider-0-8-lint-release.md`
   - worktree: `/Users/tim/.config/superpowers/worktrees/pyvider/provider-linting`
2. `docs/superpowers/plans/2026-09-21-pyvider-components-0-8-lint-release.md`
   - worktree: `/Users/tim/.config/superpowers/worktrees/pyvider-components/provider-linting`
3. `docs/superpowers/plans/2026-09-21-terraform-provider-pyvider-0-6-lint-release.md`
   - worktree: `/Users/tim/.config/superpowers/worktrees/terraform-provider-pyvider/provider-linting`
4. `docs/superpowers/plans/2026-09-21-tofusoup-0-8-public-verification.md`
   - worktree: `/Volumes/data/pyv/tofusoup-lint-suite`
5. `docs/superpowers/plans/2026-09-21-provider-linting-tutorial-part-7.md`
   - repository: `/Volumes/data/pyv/pyvider-tutorial`; create an isolated
     `codex/provider-linting-tutorial` worktree before editing
6. `docs/superpowers/plans/2026-09-21-provider-linting-site-release.md`
   - worktree: `/Users/tim/.config/superpowers/worktrees/site-pyvider-com/provider-linting`

The provider worktree currently contains four user-owned regenerated artifacts:

```text
provider-linting-direct.cast
provider-linting-opentofu.cast
provider-linting-proof.json
provider-linting-walkthrough.cast
```

Do not stage, replace, or discard them until the provider plan reaches its
artifact-regeneration task. At that point compare them with the newly generated
public-release proof and commit only the verified final artifacts.

This plan suite is committed before Task 1 starts. Child plans are normative
for repository-local command bodies; this umbrella names their task boundaries
and adds only cross-repository gates rather than duplicating those commands.

## Task 1: Record starting state

- [ ] **Step 1: Capture immutable branch coordinates.**

Run:

```bash
for repo in \
  /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting \
  /Users/tim/.config/superpowers/worktrees/pyvider-components/provider-linting \
  /Users/tim/.config/superpowers/worktrees/terraform-provider-pyvider/provider-linting \
  /Volumes/data/pyv/tofusoup-lint-suite \
  /Volumes/data/pyv/pyvider-tutorial \
  /Users/tim/.config/superpowers/worktrees/site-pyvider-com/provider-linting
do
  git -C "$repo" status --short --branch
  git -C "$repo" rev-parse HEAD
done
```

Expected: only the four provider proof artifacts and the site's pre-existing
`.superpowers/`/`__pycache__` paths are dirty or untracked.

- [ ] **Step 2: Create the release-coordinate ledger.**

Create an execution note outside Git at
`/tmp/pyvider-provider-lint-release-coordinates.json` with this initial shape:

```json
{
  "pyvider": {},
  "pyvider_components": {},
  "tofusoup": {"version": "0.8.0"},
  "terraform_provider_pyvider": {},
  "tutorial": {},
  "site": {}
}
```

Update it only from verified command output. Never use it as proof on the site;
the repository proof manifests remain authoritative.

## Task 2: Publish framework and reusable rules

- [ ] **Step 1: Execute the Pyvider 0.8.0 plan completely.**

Expected handoff: Git tag/release `v0.8.0`, PyPI `pyvider==0.8.0`, clean-wheel
lint import smoke, release commit SHA, wheel SHA-256, and green release run ID.

- [ ] **Step 2: Record and independently verify Pyvider.**

Run in a temporary directory and exercise actual installed behavior:

```bash
verify_tmp=$(mktemp -d /tmp/pyvider-public-api.XXXXXX)
(cd "$verify_tmp" && uv run --isolated --no-project --refresh --index https://pypi.org/simple \
  --with pyvider==0.8.0 python -I - <<'PY'
import asyncio
from pathlib import Path
import pyvider
from pyvider.lint import LintFinding, LintSelector
from pyvider.lint._runner import run_lints
class Component:
    async def lint(self, ctx):
        return (LintFinding(rule="release/pyvider:smoke", groups=("release/pyvider:all",), summary="ok", detail="public runner"),)
assert pyvider.__version__ == "0.8.0"
result = asyncio.run(run_lints(Component(), {}, LintSelector.parse(("release/pyvider:all",)), kind="provider", name="release", operation="verify"))
assert len(result.findings) == 1 and result.failed is False
assert Path.cwd() not in Path(pyvider.__file__).resolve().parents
print(f"pyvider lint API: {pyvider.__version__}; findings={len(result.findings)}")
PY
)
```

Expected: `pyvider lint API: 0.8.0; findings=1` and an exit status of zero.

- [ ] **Step 3: Execute the pyvider-components 0.8.0 plan completely.**

Expected handoff: Git tag/release `v0.8.0`, PyPI
`pyvider-components==0.8.0`, clean-wheel rule import smoke, release commit SHA,
wheel SHA-256, and green release run ID.

## Task 3: Release the provider and verify the public runner

- [ ] **Step 1: Execute the terraform-provider-pyvider 0.6.0 plan.**

Expected handoff: GitHub release `v0.6.0`, released provider artifacts, exact
source and dependency SHAs, provider binary SHA-256, proof manifest, three
verified casts, and the green artifact-producing workflow run ID.

- [ ] **Step 2: Execute the TofuSoup public verification plan against the released provider.**

Expected handoff: proof that `tofusoup==0.8.0` runs both lanes, or a separately
designed, tested, published, and verified patch release. Record the effective
released version in the coordinate ledger.

- [ ] **Step 3: Verify the four-versus-seven boundary.**

Run the provider proof verifier named by the provider plan and inspect the
manifest. Expected:

```text
direct: provider, resource, data-source, ephemeral, list, action, state-store
opentofu: provider, resource, data-source, ephemeral
```

Any fifth OpenTofu path or missing direct path blocks the tutorial until its
cause is understood and the documentation is updated from evidence.

## Task 4: Publish the learning artifact

- [ ] **Step 1: Execute the Tutorial Part 7 plan.**

Expected handoff: a clean tutorial commit using released package coordinates,
green Part 7 CI, a 35–40 second cast, and a machine-readable tutorial proof
manifest containing exact versions, commits, commands, binary hash, dimensions,
and duration.

- [ ] **Step 2: Reproduce the tutorial from a fresh clone or archive.**

Run the tutorial plan's public commands from a directory with no sibling source
worktrees on `PYTHONPATH` or `PATH`. Expected: tests, package, direct lane,
OpenTofu lane, exclusion, and disablement all pass.

## Task 5: Stage and publish the website

- [ ] **Step 1: Execute the site release plan through staging.**

Expected handoff: one staging URL serving the exact candidate commit, with live
desktop and narrow-width checks passing for the tutorial, lint overview,
0.8.0 changelog, casts, proof files, and navigation.

- [ ] **Step 2: Compare the deployment commit with staging.**

Run:

```bash
git -C /Users/tim/.config/superpowers/worktrees/site-pyvider-com/provider-linting rev-parse HEAD
```

Expected: the SHA equals the staging deployment metadata and the SHA selected
for production.

- [ ] **Step 3: Deploy that exact commit to production and smoke-test it.**

Run the site plan's tested deploy and production-smoke commands. Expected:
HTTP 200 and current proof/version assertions on `https://pyvider.com/`,
`/linting/`, `/tutorials/provider-linting/`, and
`/changelog/pyvider-0-8-0-release/`.

## Task 6: Final audit and closeout

- [ ] **Step 1: Run every repository's final verification command.**

Expected: all commands named in the six child plans exit zero from clean
working trees, except the site's deliberately untracked brainstorm/cache paths.

- [ ] **Step 2: Dispatch a fresh final reviewer.**

Give the reviewer the approved design, all seven plans, release coordinates,
proof manifests, deployment URLs, and commit ranges. Require an explicit check
of public-only dependencies, seven-versus-four coverage language, selector
controls, documentation diagrams, cast readability, and production identity.

- [ ] **Step 3: Resolve every finding and rerun affected gates.**

No waived finding may change a factual claim, release artifact, test result,
or deployment identity.

- [ ] **Step 4: Archive final release coordinates.**

Attach the final `/tmp/pyvider-provider-lint-release-coordinates.json` values to
the release task or release notes after removing local filesystem paths. Do not
edit completed checkboxes in the already merged plan commit merely to record
execution state.
