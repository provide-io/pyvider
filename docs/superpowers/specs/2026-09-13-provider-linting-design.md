# Provider-Native Linting Through Staging

**Date:** 2026-09-13

**Status:** Approved
**Scope:** `pyvider`, `pyvider-components`, `terraform-provider-pyvider`, and `site-pyvider-com`

## Purpose

Add provider-defined configuration linting to Pyvider now, using the semantic model OpenTofu introduced in v1.13.0-beta1, without depending on a provider lint wire protocol that does not yet exist.

The result must be a complete vertical slice:

1. A supported author-facing lint API in Pyvider.
2. A real lint rule for every config-bearing component kind in `pyvider-components`.
3. Packaged-provider verification through both OpenTofu and TofuSoup.
4. A reproducible, machine-verifiable asciinema recording.
5. A pyvider.com feature page deployed to a Cloudflare Pages staging preview.

The author API is a permanent Pyvider capability. Only the temporary conversion to ordinary protocol warning diagnostics is provisional.

## Upstream Basis

This design follows OpenTofu's accepted built-in linting RFC and shipped implementation:

- [Built-in linter RFC](https://github.com/opentofu/opentofu/blob/main/rfc/20260406-linting.md)
- [Linting implementation tracker](https://github.com/opentofu/opentofu/issues/4310)
- [Initial implementation](https://github.com/opentofu/opentofu/pull/4337)
- [OpenTofu v1.13.0-beta1](https://github.com/opentofu/opentofu/releases/tag/v1.13.0-beta1)

Pyvider directly adopts these established semantics:

- A lint identifies a potential configuration concern, not an invalid configuration.
- Lints are warning-like, opt-in, individually selectable, and grouped.
- Each finding has a primary rule ID, zero or more group IDs, a summary, details, and a location when available.
- Rule selection supports `all`, namespace-level `all`, comma-separated selectors, and `!` exclusions.
- Rules should avoid work when selection hints prove their output would be discarded.
- Provider rules and their group membership are owned by the provider.
- Linting runs beneath configuration-validation paths shared by validation, planning, and application.

OpenTofu explicitly reserves provider-based lint rules for a future provider protocol proposal. The current protocol has no lint-specific diagnostic fields and cannot pass `-lint` selections to providers. Pyvider therefore does not invent protobuf fields or modify OpenTofu.

## Architecture

### Public model

Create a public `pyvider.lint` package containing three protocol-neutral types:

#### `LintFinding`

An immutable finding with:

- `rule: str` — the unique, fully-qualified rule ID.
- `groups: tuple[str, ...]` — group IDs associated with the rule.
- `summary: str` — short human-readable heading.
- `detail: str` — explanation and remediation guidance.
- `attribute_path: str | None` — the top-level configured attribute responsible for the finding, when one exists.

Rule and group IDs are validated against OpenTofu's current implemented address grammar:

```text
^([a-z0-9]+[a-z0-9_\-/]*:)?[a-z0-9]+[a-z0-9_\-]*$
```

Invalid finding metadata is an author error caught by the lint runner's fail-open boundary.

#### `LintSelector`

An immutable parsed selection containing include and exclude sets. It owns OpenTofu-compatible parsing and matching.

#### `LintContext[ConfigT]`

An immutable author-facing context containing:

- The decoded component configuration.
- The effective `LintSelector`.
- `enabled(rule, *groups) -> bool`, equivalent in purpose to OpenTofu's lint-enabled hint.

Component authors use `enabled` before costly checks. The framework also filters returned findings defensively.

### Component hook

Every config-bearing base class gains the same asynchronous default no-op hook:

```python
async def lint(self, ctx: LintContext[ConfigT]) -> Sequence[LintFinding]:
    return ()
```

The hook is added to:

- `BaseProvider`
- `BaseResource`
- `BaseDataSource`
- `BaseEphemeralResource`
- `BaseListResource`
- `BaseAction`
- `BaseStateStore`

Existing `validate()` signatures and behavior remain unchanged. Provider functions are excluded because function arguments do not participate in an equivalent configuration-validation lifecycle.

### Shared runner

A single framework runner is responsible for:

1. Detecting that linting is enabled before invoking a component hook.
2. Creating `LintContext` from decoded configuration and effective selection.
3. Calling the hook.
4. Validating finding metadata.
5. Applying selection again to returned findings.
6. Sending selected findings to the active diagnostic encoder.

Handlers do not reimplement selection or error handling.

### Validation-handler integration

Each relevant `Validate*Config` handler follows the same order:

```text
decode -> semantic validate -> lint -> select -> encode diagnostics
```

Linting runs only after decoding and existing semantic validation succeed. A rule can therefore assume valid field shapes, while still treating unknown or omitted values conservatively. A rule emits nothing unless the triggering value is known.

The shared runner is integrated into provider, managed resource, data source, ephemeral resource, list resource, action, and state store validation handlers.

### Failure behavior

Linting is fail-open. If an enabled lint hook raises or returns invalid finding metadata:

- Valid configuration remains valid.
- Pyvider logs the exception with component kind, component name, and operation.
- The response includes one ordinary, non-blocking warning titled `Provider linting did not complete`.
- The client-facing detail does not include a traceback, environment data, or configuration secrets.
- Other validation diagnostics remain intact.

This warning appears only when provider linting was requested. It prevents silent loss of requested analysis without turning advice into a gate.

## Selection and Configuration

Provider linting is off by default.

### Persistent configuration

`pyvider.toml` accepts:

```toml
[lint]
rules = [
  "provide-io/pyvider:all",
  "!provide-io/pyvider:long-action-timeout",
]
```

### Per-process override

`PYVIDER_LINT` accepts a comma-separated selector list and completely overrides `[lint].rules` when present:

```shell
PYVIDER_LINT=provide-io/pyvider:security tofu validate
PYVIDER_LINT='provide-io/pyvider:all,!provide-io/pyvider:insecure-http' tofu validate
PYVIDER_LINT='!all' tofu validate
```

An explicitly empty `PYVIDER_LINT=''` also overrides the file and disables all provider rules. This makes one-command suppression possible without editing project configuration.

Configuration precedence is:

```text
PYVIDER_LINT > [lint].rules > disabled
```

Malformed entries are logged and ignored, matching OpenTofu's permissive implementation. Syntactically valid but unknown selectors are silent no-ops.

### Matching precedence

For a finding's primary rule and groups, matching follows OpenTofu's current implementation:

1. Exact rule inclusion enables the finding.
2. Exact rule exclusion disables it.
3. Any included group enables it.
4. Any excluded group disables it.
5. Global `all` enables it.
6. Otherwise it is disabled.

An identifier included and excluded at the same level is logged; inclusion wins.

### Current operator experience

OpenTofu's `-lint` flag controls core rules only because it cannot yet reach a provider. Until the provider protocol changes, enabling both layers is explicit:

```shell
PYVIDER_LINT=provide-io/pyvider:all tofu validate -lint=all
```

This is documented as a compatibility limitation, not as an experimental Pyvider API.

## Compatibility Diagnostic Encoder

The current encoder maps each selected finding to the existing protocol `Diagnostic` message:

- Severity is `WARNING`.
- Summary is rendered as `<summary> (<rule-id>)`, matching OpenTofu's shipped display behavior.
- Detail is copied verbatim.
- `attribute_path` is mapped to the protocol attribute path when present.
- Group IDs remain internal because the current wire format has nowhere to carry them.

The compatibility encoder is isolated behind one internal boundary. No component imports protobuf types or builds protocol diagnostics directly.

Provider-side exact-once deduplication across validate, plan, and apply is not attempted. Current provider requests do not carry enough source identity to reproduce OpenTofu's source-range execution key safely.

## First-Party Rule Catalog

All rules belong to `provide-io/pyvider:all` and one category group.

| Kind | Rule | Group | Trigger | Attribute |
|---|---|---|---|---|
| Provider | `provide-io/pyvider:insecure-tls` | `provide-io/pyvider:security` | `api_insecure_skip_verify` is explicitly `true` | `api_insecure_skip_verify` |
| Resource | `provide-io/pyvider:world-writable-directory` | `provide-io/pyvider:security` | `pyvider_local_directory.permissions` has the POSIX other-write bit | `permissions` |
| Data source | `provide-io/pyvider:insecure-http` | `provide-io/pyvider:security` | `pyvider_http_api.url` starts with `http://` | `url` |
| Ephemeral resource | `provide-io/pyvider:long-lived-lease` | `provide-io/pyvider:reliability` | `pyvider_lease.ttl_seconds` is greater than 3600 | `ttl_seconds` |
| List resource | `provide-io/pyvider:include-hidden-files` | `provide-io/pyvider:security` | `pyvider_file_content.include_hidden` is explicitly `true` | `include_hidden` |
| Action | `provide-io/pyvider:long-action-timeout` | `provide-io/pyvider:reliability` | `pyvider_wait_for_file.timeout_seconds` is greater than 300 | `timeout_seconds` |
| State store | `provide-io/pyvider:relative-state-store-path` | `provide-io/pyvider:reliability` | `pyvider_filesystem_store.path` is relative | `path` |

Each rule describes why the configuration may be intentional and tells the operator how to make it safer or suppress that exact rule. No rule reads files, contacts a network service, or mutates external state.

## TDD Strategy

Implementation uses strict red-green-refactor slices. Production code for a behavior is not written until its failing test exists and has been observed failing for the expected reason.

### Slice 1: Core model and selectors

Add failing tests for:

- Finding immutability and metadata validation.
- Accepted and rejected OpenTofu rule addresses.
- Exact rule and group precedence.
- `all`, namespace `all`, and `!` exclusions.
- Include/exclude conflicts.
- Unknown selector tolerance.
- Disabled-by-default behavior.
- TOML and environment precedence.

Implement only enough to make this layer green, then refactor.

### Slice 2: First vertical path

Use `provide-io/pyvider:insecure-http` to prove one complete data-source path. Tests cover:

- Default base hook.
- `LintContext.enabled` hints.
- Handler sequencing after validation.
- Disabled hooks not running.
- Compatibility warning encoding.
- Attribute-path preservation.
- Fail-open behavior.
- Triggering and safe HTTP API configurations.

Generalization begins only after this path passes through the handler boundary.

### Slice 3: Seven framework paths

Parameterize the handler contract suite across all seven component kinds. Each path proves:

- Hook invocation for valid decoded configuration.
- No invocation when disabled.
- No invocation after semantic validation errors.
- Exact-rule and group selection.
- Exact exclusion.
- Warning severity and location.
- Existing validation diagnostics are unchanged.

### Slice 4: Seven component rules

Each real rule receives tests for:

- Its triggering configuration.
- A nearby safe configuration.
- Omitted values.
- Unknown values where the component lifecycle permits them.
- Exact selection.
- Category selection.
- Exact exclusion from a selected group.
- Accurate summary, remediation, group, and attribute path.

### Slice 5: Packaged-provider proof

The actual provider repository builds and launches its packaged artifact from coordinated local Pyvider and component revisions. Tests must demonstrate that they did not accidentally import and exercise an editable provider in-process.

The packaged test suite covers:

- Provider linting off.
- `PYVIDER_LINT` enablement.
- `[lint].rules` enablement.
- Environment override of file settings.
- Individual and group selection.
- Exact exclusion.
- All seven validation RPCs.

## End-to-End Verification

### OpenTofu stage

Pin OpenTofu `v1.13.0-beta1` and run a real initialized configuration against the launched packaged provider binary.

`tofu validate` can currently reach four of the seven validation paths:

- Provider
- Managed resource
- Data source
- Ephemeral resource

Machine assertions use JSON output and verify severity, rule ID in the summary, detail, attribute path, enable/disable behavior, and exclusion behavior. The human recording uses normal terminal rendering.

### TofuSoup stage

OpenTofu declares action, list-resource, and state-store validation RPCs but does not yet call them from core. TofuSoup therefore drives the same packaged provider binary directly and verifies all seven paths, including those three.

The output and documentation must state this boundary plainly. TofuSoup is additional protocol proof, not a claim that OpenTofu core can currently traverse all seven configurations.

### Required verification layers

Before recording or deploying:

1. Pyvider unit and handler suites pass.
2. `pyvider-components` unit suite passes after rebuilding its flavor helpers as required by that repository.
3. The actual provider conformance suite passes against the packaged binary.
4. The real OpenTofu JSON E2E suite passes.
5. The recording and manifest integrity suite passes.
6. The site proof checks and Hugo production build pass.

## Recorded Proof

The actual provider repository owns the canonical proof generator and CI artifact.

### Artifacts

- `provider-linting.cast` — asciinema v2 recording.
- `provider-linting-proof.json` — machine-readable provenance and expectations.

The manifest contains:

- Pyvider, `pyvider-components`, and actual-provider versions or commit SHAs.
- OpenTofu version and checksum.
- Packaged provider binary checksum.
- Exact commands executed.
- Seven expected rule IDs and their component kinds.
- Which rules were observed in OpenTofu and which were observed through TofuSoup.
- Cast checksum.
- CI run identity and generation timestamp.

It contains no tokens, environment dumps, user paths, or other secrets.

### Visible recording sequence

The deterministic recording shows:

```text
tofu version
tofu validate
PYVIDER_LINT=provide-io/pyvider:all tofu validate -lint=all
PYVIDER_LINT='provide-io/pyvider:all,!provide-io/pyvider:insecure-http' tofu validate
soup stir provider-linting
```

The first validation proves default-off behavior. The second shows core and four provider validation paths. The third proves exact exclusion. TofuSoup finishes with all seven packaged-provider paths passing.

The existing PTY recorder and retiming utilities are reused. CI parses the generated asciicast, removes terminal control sequences for assertions, verifies the expected commands and rule IDs, validates the manifest, and uploads both files as one named artifact. An unchecked recording is not accepted as proof.

## Documentation

### Pyvider

Document:

- `LintFinding`, `LintSelector`, and `LintContext`.
- The `lint()` hook with a minimal author example.
- The distinction between validation, deprecation, ordinary warning, and lint findings.
- Pure, unknown-safe rule-writing guidance.
- Current and future transport behavior.

### `pyvider-components`

Document all seven rules beside their components, including trigger, remediation, groups, and suppression examples. Generated provider documentation must include the provider-level rule and configuration examples.

### Actual provider

Document how to reproduce the packaged OpenTofu and TofuSoup proof locally and how CI generates the cast and manifest.

## pyvider.com

The live `provide-io/site-pyvider-com` repository receives:

- An evergreen `/linting/` page.
- A concise homepage link to that page.
- The verified cast under `static/casts/provider-linting.cast`.
- The proof manifest as a downloadable static asset.
- A sync script that fetches a specifically identified provider CI artifact and verifies its manifest and checksum before installing it.

The page includes:

- The embedded cast using the site's existing asciinema shortcode.
- The seven-rule catalog.
- Copyable enable, exclude, and disable commands.
- Persistent `[lint]` examples.
- An OpenTofu/TofuSoup capability matrix.
- Links to the upstream RFC, tracker, implementation, and pinned beta.
- A reproduction link to the exact actual-provider fixture and proof manifest.
- A clear statement that current OpenTofu does not yet transport provider lint metadata.

Pyvider's API is described as supported. OpenTofu's built-in linting is described using OpenTofu's own experimental status, and the ordinary-warning transport is described as a compatibility bridge.

## Staging Deployment

Production deployment is out of scope. Staging uses a Cloudflare Pages feature-branch preview for project `pyvider-one`.

Before deployment:

1. The artifact sync verifies the named CI artifact.
2. Proof integrity checks pass.
3. Hugo's production build passes.

After deployment, automated smoke checks require:

- `/linting/` returns HTTP 200.
- The cast and proof manifest return HTTP 200.
- Rendered HTML contains all seven rule IDs.
- Enable, exclude, and disable commands are present.
- Upstream source links are present.
- The asciinema player targets the verified cast.

The resulting preview URL is reported for human review. No command in this project changes the production `pyvider.com` deployment.

## Native Protocol Migration

When OpenTofu publishes provider lint protocol support:

1. Add a native encoder and any defined capability negotiation.
2. Populate `LintContext` from official selection hints when the protocol provides them.
3. Otherwise return native findings and let OpenTofu perform its specified final filtering.
4. Treat explicit Pyvider file/environment selection as an optional provider-side policy filter.
5. Emit either native lint messages or compatibility warnings, never both.
6. Run the same finding, selection, component, and packaged-provider contracts against the native adapter.
7. Retire the compatibility encoder only after supported OpenTofu versions no longer need it.

The migration must not require changes to component `lint()` implementations, rule IDs, groups, or documentation examples unrelated to transport activation.

## Out of Scope

- Changes to the OpenTofu repository.
- Production pyvider.com deployment.
- Provider-function linting.
- Third-party or dynamically loaded rule registries.
- Source-comment suppression annotations.
- Module-authored lint rules.
- Automated fixes or replacement hints.
- Full HCL source ranges before the provider protocol supplies them.
- Reclassifying validation errors or deprecations as lints.
- Cross-phase source deduplication without stable source identity.

## Completion Criteria

This feature is complete only when all of the following are true:

- The stable public Pyvider lint API is documented and tested.
- All seven base component kinds and validation handlers support linting.
- All seven shipping `pyvider-components` rules behave as documented.
- Default-off, file configuration, environment override, groups, and exclusions are proven.
- The actual packaged provider passes direct seven-RPC conformance.
- OpenTofu v1.13.0-beta1 proves all four core-reachable paths.
- The checked cast and proof manifest are produced by CI.
- pyvider.com embeds the verified proof and accurately describes the compatibility boundary.
- A Cloudflare Pages staging preview passes automated smoke checks and its URL is available for review.
