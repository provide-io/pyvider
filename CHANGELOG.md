# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
