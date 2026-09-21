# Provider Linting Release, Tutorial, and Site Design

**Date:** 2026-09-21  
**Status:** Approved design  
**Primary repository:** `provide-io/pyvider`  
**Related repositories:** `provide-io/pyvider-components`,
`provide-io/terraform-provider-pyvider`, `provide-io/tofusoup`,
`provide-io/pyvider-tutorial`, and `provide-io/site-pyvider-com`

## Summary

Provider linting must ship as a public, reproducible feature rather than as a
website demonstration assembled from development worktrees. The release train
therefore publishes and verifies the framework first, then its reusable rules,
then the real provider, then a tutorial and recording built only from those
public artifacts, and finally the website content that presents the result.

The release train is:

1. Finish and release Pyvider 0.8.0.
2. Verify the PyPI wheel in a clean environment.
3. Finish and release pyvider-components 0.8.0 against the public Pyvider
   release.
4. Build and release terraform-provider-pyvider 0.6.0 from public dependencies.
5. Verify TofuSoup 0.8.0 against the released provider; publish a tested patch
   release only if integration exposes a TofuSoup defect.
6. Build Tutorial Part 7 and its recording from the released packages.
7. Publish the verified tutorial, release notes, overview, and proof metadata to
   staging and then production.

No tutorial, recording, changelog entry, or production claim may rely on an
unpublished worktree import, a private CI helper, or an unreleased wheel.

## Goals

- Make provider-authored lint findings a supported Pyvider API.
- Support every Pyvider validation surface without coupling component code to
  protobufs or a provisional OpenTofu wire format.
- Supply seven useful reusable rules through pyvider-components and exercise
  them through the installable provider.
- Let provider authors select, exclude, override, and disable rules explicitly.
- Verify the same packaged provider through TofuSoup's direct and OpenTofu
  lanes without conflating what those lanes prove.
- Teach the complete author workflow in Part 7 of the existing `mycloud`
  tutorial.
- Produce a polished, readable, reproducible terminal recording lasting about
  35–40 seconds.
- Present the feature accurately on pyvider.com, including its release status
  and OpenTofu's upstream status as of a named version and date.
- Preserve machine-readable provenance for every public proof claim.

## Non-goals

- Inventing a provider-lint protobuf message before OpenTofu publishes one.
- Claiming that OpenTofu passes provider-rule selectors over tfprotov6 today.
- Treating provider lint findings as hard validation failures.
- Shipping the seven pyvider-components rules as universal Pyvider core policy.
- Advertising seven-path OpenTofu coverage when OpenTofu currently reaches only
  four relevant validation paths.
- Teaching file authoring inside the terminal recording; the written tutorial
  owns that explanation.
- Adding linting as a primary website navigation destination.

## Release architecture

The public-artifact boundary is the central constraint:

```text
Pyvider 0.8.0
  -> clean PyPI verification
  -> pyvider-components 0.8.0
  -> terraform-provider-pyvider 0.6.0
  -> packaged-provider proof with TofuSoup 0.8.x
  -> Tutorial Part 7 and checked-in recording
  -> pyvider.com staging
  -> the same site commit in production
```

Each arrow is a release gate. A downstream repository may be developed against
an exact public commit while the train is being prepared, but its final lock,
proof, and release must resolve the published upstream artifact. The recorded
tutorial and website may use only public release coordinates.

## Pyvider 0.8.0 contract

### Public model

Pyvider exports these supported types from `pyvider.lint`:

- `LintFinding`: immutable rule result containing its rule identifier, groups,
  summary, detail, and optional top-level attribute path.
- `LintSelector`: parser and matcher for includes and exclusions.
- `LintContext[ConfigT]`: decoded configuration plus the effective selector and
  a convenience `enabled()` check.

The supported provider-author hook is:

```python
async def lint(self, ctx: LintContext[ConfigT]) -> Sequence[LintFinding]:
    ...
```

The hook exists on provider, resource, data-source, ephemeral-resource,
list-resource, action, and state-store base classes. Existing validation APIs
and method signatures remain compatible.

### Selection and configuration

Linting is disabled by default. A provider process can enable it persistently
through `pyvider.toml`:

```toml
[lint]
rules = ["example/acme:all", "!example/acme:insecure-http"]
```

`PYVIDER_LINT` supplies a comma-separated process override. Presence matters:
an explicitly empty value disables provider linting for that process.

```text
PYVIDER_LINT > [lint].rules > disabled
```

Selectors support exact rules, groups, provider-defined namespaced groups,
global `all`, and a single leading `!` for exclusions. Matching uses this
precedence:

1. exact rule inclusion;
2. exact rule exclusion;
3. included group;
4. excluded group;
5. global `all`;
6. disabled.

Malformed selectors are logged and ignored. Valid but unknown selectors are
silent no-ops. Defensive filtering after a hook runs prevents an unselected
finding from escaping a provider implementation.

### Failure semantics

Lint execution is fail-open. Unknown or absent configuration skips the hook.
A raised hook or invalid return value leaves normal validation intact and adds
one generic, non-blocking warning only when linting was requested. Logs include
safe component identity and operation context but never decoded configuration
or exception text that may contain secrets.

### Transport boundary

As of 2026-09-21, OpenTofu's built-in linter is still an upstream beta feature
and tfprotov6 contains no provider-lint request, response, or selection hints.
Pyvider therefore maps selected findings into ordinary warning diagnostics on
existing validation RPCs. The rule ID is retained in the summary, detail and
the optional top-level attribute path are preserved, and groups remain internal
because the wire format cannot carry them.

All protobuf knowledge remains inside the compatibility adapter. Component
hooks return protocol-neutral `LintFinding` values. When OpenTofu publishes a
native provider-lint protocol, a capability-negotiated native adapter will
replace the compatibility encoder without changing hooks, rule IDs, or selector
semantics. A request emits native findings or compatibility warnings, never
both.

### Documentation and release readiness

Pyvider 0.8.0 includes:

- author documentation for the public model and hook;
- selector grammar and precedence;
- persistent, environment, exclusion, and disablement examples;
- linting-versus-validation guidance;
- unknown-value and secret-safety guidance;
- compatibility and future native-protocol sections;
- a lifecycle/transport diagram showing component hook, selector, runner,
  compatibility adapter, validation RPC, TofuSoup direct lane, and OpenTofu
  lane;
- an accurate 0.8.0 changelog and version metadata;
- wheel-content and clean-install release tests.

The release is not complete until a clean environment installs
`pyvider==0.8.0` from PyPI and verifies the public imports and a minimal lint
execution without access to a source checkout.

## Rule ownership and downstream releases

Pyvider owns the framework. pyvider-components owns seven concrete reusable
rules:

| Surface | Rule |
| --- | --- |
| Provider | `provide-io/pyvider:insecure-tls` |
| Resource | `provide-io/pyvider:world-writable-directory` |
| Data source | `provide-io/pyvider:insecure-http` |
| Ephemeral resource | `provide-io/pyvider:long-lived-lease` |
| List resource | `provide-io/pyvider:include-hidden-files` |
| Action | `provide-io/pyvider:long-action-timeout` |
| State store | `provide-io/pyvider:relative-state-store-path` |

pyvider-components 0.8.0 depends on the released Pyvider 0.8.0 API and documents
each rule beside the affected component. Every rule must remain safe for
unknown, missing, or incomparable values and must point at the triggering
attribute.

terraform-provider-pyvider 0.6.0 is the installable, packaged demonstration of
those rules. Its existing release workflow builds platform artifacts and runs
provider conformance. Provider-lint proof is added to that artifact-based path,
not run against an editable dependency.

TofuSoup 0.8.0 is already the public runner for direct and OpenTofu lint lanes.
The integration first verifies that published release. If the tutorial or
provider proof reveals a TofuSoup defect, the defect is reproduced with a
failing test, fixed, documented, and released as a patch before the train
continues. The tutorial never carries a private workaround.

## Tutorial Part 7

### Place in the learning path

Part 7 follows the protocol 6.11 action/list-resource tutorial and continues the
same `mycloud` provider. Its directory is `part7-provider-linting`. The tutorial
repository README, runner, recorder, aggregate recording script, and CI matrix
all treat Part 7 as a first-class part rather than a standalone demo.

### Example rule

Part 7 adds `example/mycloud:production-name` to `mycloud_server`. It warns when
`prod` is encoded only in the server name. The configuration is valid, so this
is intentionally advisory: the finding asks the author to consider explicit
environment metadata rather than rejecting the server.

The finding points to `name`. The hook returns no finding when the value is
unknown, absent, not a string, or non-triggering. The written tutorial explains
the distinction between validation errors, deprecations, ordinary runtime
warnings, and selectable lint findings.

### Tutorial flow

The written tutorial teaches:

1. defining a stable namespaced rule and optional groups;
2. implementing an async, unknown-safe hook;
3. writing the triggering test before implementation;
4. adding non-triggering, selector, exclusion, disablement, and failure tests;
5. packaging the provider from released Pyvider 0.8.0;
6. declaring a public TofuSoup lint suite;
7. running the direct lane against the packaged binary;
8. running the OpenTofu beta lane against the same binary;
9. selecting rules persistently and for one process;
10. excluding the exact rule and explicitly disabling provider linting;
11. interpreting the two lanes without claiming a native provider protocol.

Small checked-in suite/config variants provide enabled, exact-excluded, and
disabled runs. They use TofuSoup's public suite format and provider environment
table. A reader can run every displayed command without repository-private
scripts. Repository scripts may orchestrate and verify those commands in CI,
but the recording displays only public commands.

### Recording design

The cast starts from a prepared Part 7 checkout. Source authoring stays in the
written tutorial; the cast demonstrates observable behavior. Its target length
is 38 seconds, acceptable within a 35–40 second band:

| Time | Observation |
| --- | --- |
| 0–3 s | Title and purpose |
| 3–8 s | Focused tests pass |
| 8–13 s | The provider is packaged |
| 13–21 s | TofuSoup direct lane returns the provider finding |
| 21–29 s | OpenTofu beta lane reports its separately labelled result |
| 29–34 s | Exact exclusion produces no selected finding |
| 34–38 s | Explicit disablement produces no selected finding and holds the final frame |

Each command is separated by a blank line. Meaningful results remain visible
long enough to read. Only idle build time is compressed. The raw execution is
real; output is not fabricated or replaced with private helper output. The
recording uses consistent terminal geometry, responsive playback, and an
adjacent note explaining that idle time was shortened and results were held for
readability.

## Website information architecture

The website separates content by visitor intent:

- `/linting/` explains the feature, selection model, two proof lanes, and
  upstream status in approachable language.
- `/tutorials/provider-linting/` is Part 7's hands-on author workflow.
- Pyvider's documentation is the API and architecture reference.
- `/changelog/pyvider-0-8-0-release/` is the detailed release record and
  migration guide.

Linting remains a secondary feature and is not added to the primary header.
Part 7 follows Part 6 in the tutorial learning path. The overview links to the
tutorial; the tutorial links to API documentation and the 0.8.0 release notes.
The changelog retains detailed entries from 0.6 onward and consolidated history
for 0.3 through 0.5.

### Version accuracy

The site owns one structured Hugo data value for the current Pyvider version,
consumed through a small shortcode or partial wherever prose means “available
today.” Release-history prose may still name a literal historical version.

The stale Part 6 sentence becomes the factual equivalent of:

> Actions and list resources were introduced in Pyvider 0.5 and are available
> in Pyvider 0.8.0 today.

OpenTofu copy names the exact beta and an “as of” date, links to upstream
sources, and distinguishes inference from released behavior. It does not use
timeless statements such as “current OpenTofu cannot …”.

## Verification and provenance

### TDD layers

Each implementation task follows red, green, refactor, and focused verification
before broader regression tests.

Pyvider covers:

- model invariants and public imports;
- selector parsing, normalization, precedence, and conflicts;
- configuration precedence and explicit empty override;
- seven base hook contracts;
- seven validation-handler integrations;
- unknown and absent configuration;
- defensive result filtering and fail-open errors;
- packaged-provider subprocess behavior;
- wheel contents and clean PyPI installation;
- formatting, static typing, security, and the full regression suite.

pyvider-components covers every rule's trigger, non-trigger, unknown handling,
rule and group identifiers, message, and attribute path.

terraform-provider-pyvider proves 7/7 declared paths through TofuSoup's direct
lane. The OpenTofu beta lane proves only provider, resource, data-source, and
ephemeral-resource paths because those are the four paths OpenTofu currently
executes in this fixture. List-resource, action, and state-store coverage remains
direct-lane evidence and is labelled as such.

Tutorial CI builds Part 7 from public dependencies, executes all three selector
variants, regenerates or verifies the cast, and fails if output or duration
drifts outside the contract.

The website runs content assertions, Hugo's production build, internal-link and
proof-manifest validation, and browser checks at desktop and narrow responsive
widths. Cast controls, terminal framing, wrapping, duration, and readability are
checked on staging before production.

### Proof manifest

Recorded proof is generated from execution, not manually asserted. Its
machine-readable manifest contains:

- repository names and exact commits;
- released package names and versions;
- provider binary SHA-256;
- TofuSoup and OpenTofu versions;
- exact public commands;
- requested lanes and observed findings;
- direct-versus-OpenTofu coverage labels;
- cast filename, terminal geometry, duration, and generation timestamp.

Site tests compare prose and rule tables with this manifest so version, hash,
rule, path, and command drift fails before deployment.

## Release and deployment gates

The train advances only when the current gate is green:

1. Pyvider tests, docs, metadata, and release workflow pass.
2. Pyvider 0.8.0 is published and clean-install verified from PyPI.
3. pyvider-components tests and docs pass against that public release.
4. pyvider-components 0.8.0 is published and clean-install verified.
5. terraform-provider-pyvider builds all supported artifacts, passes conformance,
   and produces the lint proof from public inputs.
6. terraform-provider-pyvider 0.6.0 is released through its normal artifact
   workflow and the released binary is reverified.
7. Tutorial Part 7 passes and its cast and proof metadata are generated from
   released dependencies.
8. The site passes all local tests and production build checks.
9. Staging deploys the candidate commit and passes live desktop, responsive,
   navigation, link, and recording smoke tests.
10. Production deploys the exact staging-tested commit and passes the same smoke
    checks.

Failed staging leaves production untouched. A post-deployment production smoke
failure rolls back to the previous deployment. No failure is converted into a
success through a worktree dependency, skipped required lane, or softened CI
conclusion.

## Execution model

Implementation uses subagent-driven development with repository-scoped tasks.
Each task receives the approved design and a concrete test-first plan. An
implementer makes the smallest coherent change, a specification reviewer checks
it against this document, and a quality reviewer checks maintainability and
verification evidence. Sequential release dependencies remain controlled by the
primary agent even when independent documentation or site tasks are prepared in
parallel.

The implementation plan must preserve existing user changes and dirty-worktree
artifacts, especially regenerated provider proof recordings, and must identify
which existing branches are merged, released, or superseded rather than
reimplementing completed work.
