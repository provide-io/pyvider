# Provider Linting Release Review Blockers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the release provenance, registry-byte verification, and fail-open lint transport gaps found in the final 0.8.0 review.

**Architecture:** Extend the existing standalone stdlib verifier so it owns wheel-version inspection, registry JSON validation, digest-checked download, and a machine-readable result. Keep package installation in the workflow, but install the verifier-downloaded wheel with dependencies resolved only from PyPI. Treat lint model construction and protobuf compatibility encoding as one fail-open provider boundary, with validation in the public immutable model and a safe generic warning from the adapter.

**Tech Stack:** Python 3.11 stdlib, pytest, attrs, generated protobuf bindings, GitHub Actions YAML, uv.

---

### Task 1: Bind build artifacts to the release version

**Files:**
- Modify: `scripts/verify_lint_release.py`
- Modify: `tests/scripts/test_verify_lint_release.py`
- Modify: `tests/scripts/test_release_workflow.py`
- Modify: `.github/workflows/release.yml`

- [ ] Add tests that build minimal wheel ZIPs with `.dist-info/METADATA` and prove filename/METADATA/expected-version equality, including tag normalization and mismatches.
- [ ] Run the focused tests and record the expected RED failures for the missing expected-version wheel contract and release-tag workflow binding.
- [ ] Implement `normalize_version`, wheel filename parsing, METADATA parsing, and `verify_wheel(path, expected_version=...)` with clear `SystemExit` failures.
- [ ] Pass `github.event.release.tag_name` to the release verification job; retain a tag-free dry-run that cross-checks filename and METADATA.
- [ ] Run the focused verifier/workflow tests GREEN and commit the coherent artifact-binding change.

### Task 2: Verify and install exact registry bytes

**Files:**
- Modify: `scripts/verify_lint_release.py`
- Modify: `tests/scripts/test_verify_lint_release.py`
- Modify: `tests/scripts/test_release_workflow.py`
- Modify: `.github/workflows/release.yml`

- [ ] Add offline tests for exact filename/digest match, missing/extra artifacts, metadata digest mismatch, unsafe artifact URL, downloaded digest mismatch, and cache-busting metadata URLs.
- [ ] Run those tests and record RED failures because registry verification mode does not exist.
- [ ] Implement stdlib registry JSON loading, exact release comparison against `dist`, HTTPS same-registry artifact URL validation, digest-checked wheel download, and JSON output.
- [ ] Download `release-artifacts` into both registry verification jobs, retry the verifier with a fresh query parameter, install only its verified local wheel, and resolve dependencies exclusively with `--index-url https://pypi.org/simple/`.
- [ ] Add workflow assertions excluding TestPyPI from dependency resolution and requiring installation from the verified downloaded wheel.
- [ ] Run focused tests GREEN and exercise the registry verifier against a local fixture server.
- [ ] Commit the coherent registry-verification change.

### Task 3: Complete the lint fail-open boundary

**Files:**
- Modify: `src/pyvider/lint/model.py`
- Modify: `src/pyvider/protocols/tfprotov6/handlers/_linting.py`
- Modify: `tests/lint/test_model.py`
- Modify: `tests/lint/test_runner.py`
- Modify: `tests/tfprotov6/handlers/test_provider_linting_contract.py`
- Modify: `docs/core-concepts/provider-linting.md`

- [ ] Add model tests rejecting lone-surrogate text in every string field and rejecting non-top-level attribute paths.
- [ ] Add seven-surface handler tests whose hooks attempt malformed findings and require one generic warning, never an error or uncaught exception; retain the valid targeted-warning contract.
- [ ] Run model/runner/seven-surface tests and record RED failures demonstrating the constructor and compatibility encoding gaps.
- [ ] Validate UTF-8 encodability and the top-level attribute name grammar in `LintFinding`.
- [ ] Wrap hook execution plus protobuf diagnostic construction in a safe adapter boundary that logs only context and returns the generic warning on any provider metadata/encoding failure.
- [ ] Run focused tests GREEN and commit the coherent fail-open change.

### Task 4: Make transport documentation time-specific

**Files:**
- Modify: `docs/core-concepts/provider-linting.md`
- Modify: `tests/lint/test_public_api.py`

- [ ] Add a documentation test requiring the as-of date, exact `v1.13.0-beta1` proof version, and immutable OpenTofu tag links.
- [ ] Run it RED against the undated “current/today” text.
- [ ] Rewrite the transport status with dated evidence and tag-pinned RFC/source links derived from local repository proof or Git refs.
- [ ] Run the documentation test GREEN and commit.

### Task 5: Full verification and clean handoff

**Files:**
- Verify all changed files and generated release artifacts; do not publish or push.

- [ ] Run focused verifier, workflow, model, runner, public API, and seven-surface tests.
- [ ] Parse release YAML; run actionlint if available; run `bash -n`/shellcheck on extracted changed workflow scripts.
- [ ] Run `we run format.check`, `we run lint`, `we run typecheck`, `we run security`, `we run test`, `we run docs.build`, the doc-link checker, and `we run build`.
- [ ] Install the exact built 0.8.0 wheel in an isolated environment and run the standalone verifier.
- [ ] Exercise registry verification against an offline/local fixture and prove the downloaded bytes match the built artifact.
- [ ] Inspect `git diff --check`, commit any final corrections, and require a clean worktree.
