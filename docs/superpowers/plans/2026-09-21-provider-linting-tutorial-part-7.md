# Provider Linting Tutorial Part 7 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a seventh `mycloud` tutorial that authors, tests, packages, selects, excludes, disables, and proves one provider lint rule using public releases and a readable 35–40 second cast.

**Architecture:** Part 7 continues the Part 6 provider, adds one advisory resource hook, and packages it with Pyvider 0.8.0. Three checked TofuSoup suite variants demonstrate enabled, exact-excluded, and disabled selection; CI parses JSON to prove absence because the version-one suite format only asserts expected presence. Each tutorial part keeps its required engine rather than forcing one tool across the series.

**Tech Stack:** Python 3.11+, Pyvider 0.8.0, Flavorpack, pytest, TofuSoup 0.8.0, OpenTofu 1.13.0-beta1, TOML/HCL, asciinema v2 casts.

---

**Repository:** `/Volumes/data/pyv/pyvider-tutorial`
**New worktree/branch:** create `codex/provider-linting-tutorial` with `superpowers:using-git-worktrees` before editing.

### Task 1: Add the lint rule with TDD

**Files:**
- Create: `part7-provider-linting/` by copying tracked Part 6 source files, excluding `.venv`, `.terraform`, state, `dist`, egg-info, and caches
- Modify: `part7-provider-linting/pyproject.toml`
- Modify: `.gitignore`
- Modify: `part7-provider-linting/my_provider/server.py`
- Create: `part7-provider-linting/tests/test_linting.py`

- [ ] **Step 1: Create a clean Part 7 skeleton.**

Use `git ls-files part6-protocol-611` as the copy allow-list. Rename the project
description to “part 7: provider linting” and set public dependencies:

```toml
dependencies = ["pyvider==0.8.0", "flavorpack>=0.5.0"]

[dependency-groups]
dev = ["pytest>=8", "pytest-asyncio>=0.25", "tofusoup==0.8.0"]
```

Run `uv lock` inside Part 7 and assert no path, editable, or Git sources.
Add `!part7-provider-linting/uv.lock` after the global `uv.lock` ignore so this
lesson's public dependency lock is tracked. Add a contract test for
`git check-ignore part7-provider-linting/uv.lock` returning nonzero and, after
the first commit, `git ls-files --error-unmatch part7-provider-linting/uv.lock`.

- [ ] **Step 2: Write the triggering and non-triggering tests first.**

```python
import pytest
from pyvider.lint import LintContext, LintSelector
from pyvider.schema import a_str, a_unknown

from my_provider.server import PRODUCTION_NAME, Server, ServerConfig


@pytest.mark.asyncio
async def test_production_name_lint_is_advisory() -> None:
    findings = await Server().lint(
        LintContext(
            config=ServerConfig(name="web-prod"),
            selector=LintSelector.parse((PRODUCTION_NAME,)),
        )
    )
    assert len(findings) == 1
    finding = findings[0]
    assert finding.rule == "example/mycloud:production-name"
    assert finding.groups == ("example/mycloud:all", "example/mycloud:naming")
    assert finding.attribute_path == "name"
    assert finding.summary == "Production environment is encoded in the server name"


@pytest.mark.asyncio
@pytest.mark.parametrize("name", ["web-dev", "ready", "", None, 7, a_unknown(a_str())])
async def test_production_name_lint_ignores_non_triggers(name: object) -> None:
    config = ServerConfig(name=name)  # type: ignore[arg-type]
    findings = await Server().lint(
        LintContext(config=config, selector=LintSelector.parse(("all",)))
    )
    assert findings == ()
```

- [ ] **Step 3: Run the focused tests red.**

```bash
cd part7-provider-linting
uv run pytest tests/test_linting.py -q
```

Expected: import/missing-hook failure.

- [ ] **Step 4: Implement the minimal advisory hook.**

Add stable constants and imports:

```python
from pyvider.lint import LintContext, LintFinding

PRODUCTION_NAME = "example/mycloud:production-name"
ALL_LINTS = "example/mycloud:all"
NAMING = "example/mycloud:naming"
```

Add to `Server`:

```python
async def lint(self, ctx: LintContext[ServerConfig]) -> tuple[LintFinding, ...]:
    if not ctx.enabled(PRODUCTION_NAME, ALL_LINTS, NAMING):
        return ()
    name = getattr(ctx.config, "name", None)
    if not isinstance(name, str) or "prod" not in name.lower():
        return ()
    return (
        LintFinding(
            rule=PRODUCTION_NAME,
            groups=(ALL_LINTS, NAMING),
            summary="Production environment is encoded in the server name",
            detail=(
                "The name may be intentional, but explicit environment metadata is "
                "easier to review and automate. Suppress with "
                "!example/mycloud:production-name when the naming convention is deliberate."
            ),
            attribute_path="name",
        ),
    )
```

- [ ] **Step 5: Add selector and failure-boundary tests.**

Test exact rule, namespaced `all`, namespaced naming group, exact exclusion, and
disabled selector. For the failure boundary, create a temporary test fixture
copy whose `Server.lint()` raises `RuntimeError("fixture lint failure")`, package
that copy with the public `flavor pack` command, and derive a temporary suite
whose sole expected diagnostic is the warning `Provider linting did not
complete` instead of the production-name warning. Invoke it through
`uvx --from tofusoup==0.8.0 soup lint failure.soup.toml --lane direct --json`.
Require exactly that warning, no error diagnostic, and a zero suite exit. This
changes only the temporary fixture—do not add a production failure switch or
import Pyvider's private runner/handlers.

- [ ] **Step 6: Run and commit.**

```bash
uv run pytest -q
git add .gitignore part7-provider-linting
git ls-files --error-unmatch part7-provider-linting/uv.lock
git commit -m "feat: add tutorial provider lint rule"
```

Expected: Part 7 tests pass.

### Task 2: Add reproducible direct and OpenTofu suites

**Files:**
- Create: `part7-provider-linting/lint-fixture/main.tf`
- Create: `part7-provider-linting/lint.soup.toml`
- Create: `part7-provider-linting/lint-excluded.soup.toml`
- Create: `part7-provider-linting/lint-disabled.soup.toml`
- Create: `part7-provider-linting/tests/test_lint_suites.py`

- [ ] **Step 1: Write failing suite-contract tests.**

Parse all three TOML files and assert source
`registry.opentofu.org/example/mycloud`, provider version `0.1.0`, one resource
case with `name = "web-prod"`, and environment values:

```python
{
    "lint.soup.toml": "example/mycloud:all",
    "lint-excluded.soup.toml": "example/mycloud:all,!example/mycloud:production-name",
    "lint-disabled.soup.toml": "",
}
```

Assert only the enabled suite expects summary
`Production environment is encoded in the server name (example/mycloud:production-name)`.

- [ ] **Step 2: Run red.**

```bash
uv run pytest tests/test_lint_suites.py -q
```

Expected: missing fixture/suite failures.

- [ ] **Step 3: Add the isolated OpenTofu fixture.**

The HCL declares only the local `mycloud` provider and:

```hcl
resource "mycloud_server" "web" {
  name = "web-prod"
}
```

Do not include Part 6 action/list syntax; the lint lesson must not require
Terraform-only constructs.

- [ ] **Step 4: Add the three TofuSoup suites.**

Each file uses schema version 1, the same provider coordinate, one resource
case, and `[opentofu] fixture = "lint-fixture"` with `lint = "all"`. Only
`[provider.environment].PYVIDER_LINT` differs as specified by the test.

- [ ] **Step 5: Run tests and commit.**

```bash
uv run pytest tests/test_lint_suites.py -q
git add part7-provider-linting/lint-fixture part7-provider-linting/lint*.soup.toml \
  part7-provider-linting/tests/test_lint_suites.py
git commit -m "test: define tutorial lint proof suites"
```

### Task 3: Add the public workflow verifier

**Files:**
- Create: `scripts/verify-provider-linting-tutorial.py`
- Create: `tests/test_tutorial_part7.py`
- Modify: `scripts/run-tutorial-part.sh`
- Modify: `scripts/record-tutorial-part.sh`
- Modify: `scripts/record-all.sh`
- Modify: `.github/workflows/ci.yml`

- [ ] **Step 1: Write failing orchestration tests.**

Assert runner and recorder case 7 exist, CI covers Parts 1–7, no command
contains a local Pyvider/TofuSoup path, and the engine matrix is exact:

- Parts 1–5 use OpenTofu 1.12.6;
- Part 6 uses Terraform 1.15.9 for action/list/query support;
- Part 7 uses OpenTofu 1.13.0-beta1 plus TofuSoup 0.8.0.

The verifier rejects JSON when:

- enabled direct output lacks the rule;
- OpenTofu output lacks the rule or is not separately labelled;
- excluded/disabled direct output contains any diagnostic;
- package versions differ from 0.8.0;
- any before/after binary hash for any lane differs from the packaged hash.

- [ ] **Step 2: Run red.**

```bash
uv run --project part7-provider-linting pytest tests/test_tutorial_part7.py -q
```

Expected: missing verifier and Part 7 runner failures.

- [ ] **Step 3: Implement the verifier.**

Accept explicit paths for four JSON results and the packaged binary. In this
task the verifier checks execution only; manifest generation happens after the
cast exists in Task 4. Capture `source_commit` as the commit used to build and
run the provider, plus Pyvider/TofuSoup versions, binary SHA-256, exact commands,
direct/OpenTofu observations, and selector variant results in a temporary
results JSON. Reject absolute home/worktree paths and token-like values.

- [ ] **Step 4: Implement Part 7 runner commands.**

The runner's machine-proof set executes, in order. This set is distinct from
Task 4's human-readable visible command set:

```text
uv run pytest -q
uv run flavor pack --manifest pyproject.toml
uvx --from tofusoup==0.8.0 soup lint lint.soup.toml --provider "$tutorial_provider" --lane direct --json
uvx --from tofusoup==0.8.0 soup lint lint.soup.toml --provider "$tutorial_provider" --opentofu "$opentofu_beta" --lane opentofu --json
uvx --from tofusoup==0.8.0 soup lint lint-excluded.soup.toml --provider "$tutorial_provider" --lane direct --json
uvx --from tofusoup==0.8.0 soup lint lint-disabled.soup.toml --provider "$tutorial_provider" --lane direct --json
```

Capture JSON separately and call the verifier. Do not infer exclusion/disable
success from TofuSoup's suite exit status; assert diagnostics are empty.
After Flavorpack, normalize the actual output exactly:

```bash
mv dist/terraform-provider-mycloud.psp dist/terraform-provider-mycloud
chmod +x dist/terraform-provider-mycloud
tutorial_provider="$PWD/dist/terraform-provider-mycloud"
test -x "$tutorial_provider"
tutorial_provider_sha=$(shasum -a 256 "$tutorial_provider" | awk '{print $1}')
```

Every lane uses that path. Hash immediately before and after each of the four
machine JSON commands, fail on any mismatch, and record all eight values plus
the packaged checksum in the temporary results JSON. The recorder applies the
same before/after check around the four visible lane commands; final proof
requires every recorded hash to be identical.

- [ ] **Step 5: Repair the full tutorial runner/recorder matrix and commit.**

Update the root run, record, record-all, and CI paths together. Do not let the
generic recorder select OpenTofu for Part 6; that lesson requires Terraform
1.15.9. Ensure the root README/CI no longer stop at Parts 1–5. Use an explicit
CI matrix:

```yaml
include:
  - {part: 1, engine: opentofu, version: 1.12.6}
  - {part: 2, engine: opentofu, version: 1.12.6}
  - {part: 3, engine: opentofu, version: 1.12.6}
  - {part: 4, engine: opentofu, version: 1.12.6}
  - {part: 5, engine: opentofu, version: 1.12.6}
  - {part: 6, engine: terraform, version: 1.15.9}
  - {part: 7, engine: opentofu, version: 1.13.0-beta1}
```

The setup step installs only the matrix engine/version. The runner accepts the
resolved executable explicitly instead of searching `tofu` before `terraform`.
Part 6 retains its `terraform apply` and `terraform query` commands; Part 7
installs TofuSoup 0.8.0 and runs the six lint workflow commands.

```bash
uv run --project part7-provider-linting pytest tests/test_tutorial_part7.py -q
git add scripts/verify-provider-linting-tutorial.py scripts/run-tutorial-part.sh \
  scripts/record-tutorial-part.sh scripts/record-all.sh \
  tests/test_tutorial_part7.py .github/workflows/ci.yml
git commit -m "ci: prove tutorial provider linting"
```

### Task 4: Record a readable 35–40 second cast

**Files:**
- Modify: `scripts/record-tutorial-part.sh`
- Modify: `scripts/record-all.sh`
- Create: `scripts/lib/pace-provider-linting-cast.py`
- Create: `casts/tutorial-part7-provider-linting.cast`
- Create: `proofs/tutorial-part7-provider-linting-proof.json`
- Modify: `tests/test_tutorial_part7.py`

- [ ] **Step 1: Add failing cast contracts.**

Assert asciinema version 2, exact 120×40 geometry, duration between 35 and 40
seconds, all six public commands in order, a blank CRLF
between commands, readable holds after direct/OpenTofu/excluded/disabled results,
and no private `ci/*.py` command displayed.

- [ ] **Step 2: Run red.**

```bash
uv run --project part7-provider-linting pytest tests/test_tutorial_part7.py -q
```

Expected: missing Part 7 cast/recorder failures.

- [ ] **Step 3: Add a Part 7 recording case.**

Use `record-to-cast.py --split-lines --pause-end=3`, print a blank line before
each command, and run the six commands for real. The visible set is exactly:

```bash
uv run pytest tests/test_linting.py -q
uv run flavor pack --manifest pyproject.toml
set -o pipefail; uvx --from tofusoup==0.8.0 soup lint lint.soup.toml --provider "$tutorial_provider" --lane direct --json | jq -r '"Direct provider lint: \([.direct.cases[].diagnostics[]] | length) finding(s)", .direct.cases[].diagnostics[]?.summary'
set -o pipefail; uvx --from tofusoup==0.8.0 soup lint lint.soup.toml --provider "$tutorial_provider" --opentofu "$opentofu_beta" --lane opentofu --json | jq -r '"OpenTofu beta validation lane: \(if .opentofu.valid then "valid" else "invalid" end)", .opentofu.diagnostics[]?.summary'
set -o pipefail; uvx --from tofusoup==0.8.0 soup lint lint-excluded.soup.toml --provider "$tutorial_provider" --lane direct --json | jq -r '"Exact exclusion: \([.direct.cases[].diagnostics[]] | length) finding(s)"'
set -o pipefail; uvx --from tofusoup==0.8.0 soup lint lint-disabled.soup.toml --provider "$tutorial_provider" --lane direct --json | jq -r '"Provider linting disabled: \([.direct.cases[].diagnostics[]] | length) finding(s)"'
```

These are public TofuSoup commands with a public deterministic `jq` projection;
`pipefail` preserves a TofuSoup failure. The projection deliberately presents
the accurate “OpenTofu beta validation lane” label rather than replaying
TofuSoup 0.8.0's already-released shorthand “native linting.” Run the four raw
JSON commands separately outside the PTY into temporary files for machine
assertions. The proof records the visible projected commands and hidden raw
commands in separate fields, all using the same binary and suite files.

Implement the specialized
`pace-provider-linting-cast.py` transformer: cap long idle gaps, preserve typing
and output ordering, add at least two-second result holds after direct,
OpenTofu, and excluded outcomes, add a three-second final disabled hold, and
target 38 seconds without proportionally accelerating every event. The proof
must bind the paced cast hash to the same real command outputs.

- [ ] **Step 4: Record and verify.**

```bash
scripts/run-tutorial-part.sh 7
scripts/record-tutorial-part.sh 7 casts
uv run --project part7-provider-linting pytest tests/test_tutorial_part7.py -q
```

After the paced cast exists, invoke
`scripts/verify-provider-linting-tutorial.py --write-proof` with the cast,
packaged binary, four hidden JSON results, and the captured `source_commit`.
It writes `proofs/tutorial-part7-provider-linting-proof.json` with exact
120×40 dimensions, duration, cast hash, binary hash, public versions, commands,
and outcomes. Immediately rerun the same tool without `--write-proof` as a
read-only verifier. Expected: all proof assertions pass and the cast is 35–40
seconds.

The manifest's `source_commit` is the commit built and tested before recording;
it is not the later commit that adds the cast itself. After PR merge, the public
artifact commit is recorded by the site sync as a separate coordinate and must
contain `source_commit` as an ancestor. Never create a self-referential
“manifest commit” hash.

- [ ] **Step 5: Commit.**

```bash
git add scripts/record-tutorial-part.sh scripts/record-all.sh \
  scripts/lib/pace-provider-linting-cast.py \
  casts/tutorial-part7-provider-linting.cast \
  proofs/tutorial-part7-provider-linting-proof.json tests/test_tutorial_part7.py
git commit -m "docs: record provider linting tutorial"
```

### Task 5: Document and publish Part 7 source

**Files:**
- Modify: `README.md`
- Create: `part7-provider-linting/README.md`

- [ ] **Step 1: Add failing README assertions to `tests/test_tutorial_part7.py`.**

Require the root series table to list Part 7, released versions, six public
commands, the rule ID, and links to Pyvider and TofuSoup docs. Require the Part
7 README to explain direct versus OpenTofu beta coverage without saying native
provider-lint protocol.

- [ ] **Step 2: Run red, write both README sections, and rerun green.**

```bash
uv run --project part7-provider-linting pytest tests/test_tutorial_part7.py -q
```

- [ ] **Step 3: Run full repository verification.**

```bash
scripts/run-tutorial-part.sh 7
git diff --check origin/main...HEAD
git status --short
```

Expected: Part 7 passes and only intended tracked changes exist.

- [ ] **Step 4: Obtain spec and quality review, then commit.**

```bash
git add README.md part7-provider-linting/README.md
git commit -m "docs: teach provider linting in part 7"
```

- [ ] **Step 5: Push, open, check, and merge the tutorial PR.**

Push `codex/provider-linting-tutorial`, open a PR to `main`, wait for CI, merge
without deleting the worktree, and record the merged SHA plus cast/proof hashes.
