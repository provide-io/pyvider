# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- **`requires_replace` no longer looks effective on a write-only attribute while doing nothing.** Terraform requires write-only values to be null in both prior and planned state, so the plan comparison always saw `null == null` and an attribute declared `write_only=True, requires_replace=True` never once produced a replacement path -- a silent no-op on exactly the attributes (secrets, credentials) whose rotation most needs one. The combination is now rejected at schema-definition time with a `ValueError` pointing at the alternatives, matching Terraform's own SDK, which errors with `WriteOnly cannot be set with ForceNew`. To rotate a write-only secret, pair it with a companion attribute the practitioner bumps -- conventionally `<name>_wo_version` -- and set `requires_replace=True` on that, or call `ctx.require_replace()` from the plan hook.

### Added

- **Resources can force replacement instead of an in-place update.** `PlanResourceChange` never populated `requires_replace`, so an attribute the remote API cannot change (a region, an availability zone, an immutable name) was planned as an update, and the provider's `_update()` was asked to perform something it could not do. Two ways to say so: `requires_replace=True` on a schema attribute -- the equivalent of the SDK's `ForceNew` and the plugin framework's `RequiresReplace()` -- which compares the planned value against prior state, and `ctx.require_replace(path)` for replacement that depends on the values themselves rather than on the mere fact of a change. Neither reports anything on create or destroy, where Terraform rejects replacement paths, and a planned value that is still unknown counts as a change because the plan has to be decided before the value resolves.

## [0.5.3] - 2026-08-22

### Fixed

- **An absent state no longer panics Terraform.** `ReadStateBytes` sent no `range` on the empty-state path. `Range` is a message field, so unset is a nil `*StateRange` on the other side, and `grpc_provider.go:1610` dereferences it with no nil check. The result is not a diagnostic but a crashed process, on `terraform init` against a workspace that has no state yet -- which is the first thing anyone does.
- **`range.end` is the index of the last byte, not one past it.** Core writes `End: totalBytesProcessed + len(chunk) - 1` and decides which chunk is the last with `Range.End < TotalLength-1`, so an exclusive end moved that boundary by a byte and misclassified the second-to-last chunk whenever the payload ended exactly one byte past a chunk boundary.
- **Chunk sizes follow Core's.** It proposes `chunks.DefaultStateStoreChunkSize` (8 MB) and refuses to negotiate above `chunks.MaxStateStoreChunkSize` (128 MB). This defaulted to 32 KB and had no ceiling, so an oversized proposal was echoed back and became this provider's configuration failure rather than the client's.

### Changed

- **`pyvider-rpcplugin>=0.4.2`**, which raises the gRPC server's message limits from the 4 MB default to Terraform's 256 MB. A state store negotiates 8 MB chunks, so on anything older every chunk of a multi-chunk write is refused before it arrives.

Verified against Terraform built from source with the pluggable-state-storage experiment enabled: `init`, `apply`, `plan` and `destroy` all succeed with state served entirely by the provider, and an 18 MB state reads back in three chunks with no size warnings from Core.



## [0.5.2] - 2026-08-21

### Fixed
- **A list resource's identity schema is published under its own type name.**
  `GetResourceIdentitySchemas` iterated managed resources only, so a list
  resource -- for which identity is mandatory, since it is how Terraform ties a
  listed instance back to a managed one -- was absent from the map.

## [0.5.1] - 2026-08-21

### Fixed
- **A provider-defined function is no longer handed a half-known argument.**
  `call_function` guarded with `is_unknown`, which is top-level only: a list
  whose *elements* are unknown is itself known, so the guard never fired,
  `cty_to_native` rendered those elements as `None`, and the function ran on a
  partially known argument. At plan time
  `provider::x::join("\n", [resource.a.token, ...])` raised `TypeError` from
  inside `str.join` and Terraform reported "Invalid function argument" for a
  configuration that is valid. Both the required and variadic paths now test
  `is_wholly_known()` and defer the call instead.
- **`BaseEphemeralResource.validate` is annotated `ConfigType | None`.** The
  handler passes whatever `cty_to_attrs_instance` returns, which is `None` when
  the configuration is not wholly known -- an attribute referencing a
  not-yet-created resource, for instance. Every other component type already
  declared this; ephemeral resources did not, so an implementation written
  against the annotation raised `AttributeError` at plan time.

## [0.5.0] - 2026-08-20

### Added
- **Terraform plugin protocol 6.11.** Ninety-seven commits:
  - **State stores** -- a provider can serve Terraform's state backend, with
    locking that survives a crashed process on non-POSIX hosts.
  - **List resources** and **actions**, the two new 6.11 component types,
    discovered into a caller's registry.
  - **Deferred responses** in resource handlers, so a provider can answer "not
    yet" rather than guessing.
  - **Resource identity** carried across the import boundary.
  - **Server and client capability advertisement** in `GetProviderSchema`,
    including `provider_meta`.

### Fixed
- `StopProvider` is answered before the server stops.
- An unknown data source is reported as a diagnostic rather than a crash.
- The proposed new state may carry unknown values.
- `WriteStateBytes` accepts a multi-chunk stream.
- A create is no longer executed as a destroy.
- A crashed process no longer wedges state on non-POSIX hosts.

### Changed
- Requires **pyvider-cty >= 0.5.0**, which carries 61 breaking changes. Read its
  changelog before upgrading: arithmetic width, set ordering on the wire, mark
  propagation, `regex` argument order, and stricter `csvdecode`/`jsondecode` all
  moved.
- `[tool.uv.sources]` is gone from the manifest; sibling checkouts are installed
  with `uv pip install -e ../<repo>` for local development instead, so the
  published metadata describes what a real install resolves.

## [0.4.0] - 2026-04-24

Released without a changelog entry at the time; recorded here for continuity.
See the [GitHub release](https://github.com/provide-io/pyvider/releases/tag/v0.4.0).

## [0.3.33] - 2026-04-13

### Fixed
- **Ephemeral resources now surface to Terraform.** `GetMetadata` and
  `GetProviderSchema` handlers populate the `ephemeral_resources` and
  `ephemeral_resource_schemas` protobuf fields. Previously ephemerals
  were registered with the hub but invisible to Terraform, causing
  `ephemeral "<type>" "<name>" {}` blocks to fail with "Invalid
  ephemeral resource" regardless of registration.
- **Broad-exception swallowing in `apply_resource_change`.** Unexpected
  exceptions are now wrapped in `ResourceError` with `__cause__`
  preserved, `handler_errors` metric now bumps on the error path, and
  the catch-all produces a diagnostic that names the origin exception
  type instead of an opaque "unexpected error".
- **Race in `StreamStdio`.** Replaced the hand-rolled `_stream_active`
  boolean with `asyncio.Event`; removed the nested-generator layer and
  stale debugging comment. Stream lifetime is now signaled through a
  single source of truth that callers can `await`.
- **`BaseProvider.capabilities` no longer shared across instances.**
  Previously declared as `ClassVar[dict]`, which meant every provider
  instance in a process saw the same capability registrations.
  `capabilities` is now a per-instance attrs field populated inside
  `setup()` and published atomically. `setup()` is idempotent and
  guarded by an `asyncio.Lock` + `_setup_done` flag.
- **Bare `RuntimeError` in `apply_resource_change`.** Replaced with
  `FrameworkConfigurationError` carrying enriched context
  (`resource.type_name`, `terraform.summary`, `terraform.detail`) so
  the framework's diagnostic enrichment path applies.
- **Non-attrs classes silently round-tripped to empty objects.**
  `cty_to_attrs_instance` now rejects non-attrs classes up front with
  a `FrameworkConfigurationError` that names the offending class and
  suggests decorating with `@attrs.define` / `@attrs.frozen`.

### Changed
- **Refactor: all 20 tfprotov6 RPC handlers share an `@rpc_handler`
  decorator** (`src/pyvider/protocols/tfprotov6/handlers/_metrics.py`).
  Replaces ~12 lines of per-handler boilerplate that wrapped metric
  collection and `@resilient()` — a single-file change for any future
  cross-cutting concern at the handler boundary.
- `pyvider.hub.DISCOVERY_READY_EVENT` is now the canonical key for the
  discovery-ready singleton. Three files previously hardcoded the
  magic string; a typo at any one of them used to turn into a silent
  55-second startup hang. Now it's an ImportError at module load.
- Protocol timeouts in `protocols/service.py` lifted out of magic
  numbers into named module-level constants:
  `STREAM_STARTUP_TIMEOUT_SECONDS`,
  `STREAM_HEARTBEAT_INTERVAL_SECONDS`, `SHUTDOWN_DRAIN_SECONDS`.
  `StreamStdio`'s inbound iterator is now typed as
  `AsyncIterator[Any]` rather than plain `Any`.
- `BaseResource` and `BaseDataSource` class docstrings now document
  the attrs-class requirement for `config_class` / `state_class` /
  `private_state_class`.
- Test-mode access-check log promoted from debug to info so successful
  test-only access events are visible in audit logs.
- `common/launch_context.py` uses `Path.cwd()` instead of
  `os.getcwd()` (PTH109).
- Drop Python 3.14 classifier from `pyproject.toml`; `requires-python`
  remains `>=3.11` and CI targets 3.11.
- Copyright range extended through 2026 across SPDX headers, LICENSE,
  and site footer.

### Docs
- Replace stale `foundry.provide.io/pyvider/` URLs with
  `pyvider.com/docs/` in `README.md`, `docs/index.md`, `docs/faq.md`,
  `pyproject.toml`, and `mkdocs.yml`.
- Remove "Made with ❤️" footers and the
  "🛠️ with 💚 and 🦝 on 🌎" emoji flourish from project metadata.
- Add full ephemeral resource showcase (`DemoSessionToken`) to the
  demo provider in `examples/demo-provider/`.

### Added
- `tests/regression/test_high_severity_fixes.py`: 10 regression tests
  locking in the behavior of every fix above, including two new tests
  that cover the attrs-class validator.

### Infrastructure
- Full CI suite (ruff format, ruff check, mypy strict, pytest): 1,407
  passed / 3 skipped / 2 xfailed.

## [0.3.32] - 2026-04-11

### Added
- Initial development release of pyvider
- Python Terraform Provider Framework core functionality
- Integration with pyvider-cty for type system
- Integration with pyvider-rpcplugin for gRPC protocol
