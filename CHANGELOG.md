# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Resources can version their state schema and migrate it.** `UpgradeResourceState` was a documented pass-through, and correct only because `s_resource` accepted no version: the stored version could never differ from the advertised one, so the RPC was never asked to do anything. That held right up until a provider author changed a resource's state shape — a renamed attribute, a changed type, one attribute split into two — at which point they had no way to signal it, Terraform handed the old state to the new schema, and the result was a decode error at best and a silent mis-read at worst. The workaround was to tell practitioners to `terraform state rm` and re-import, which is the migration the provider was supposed to perform for them. Now `s_resource(..., version=N)` declares the version, and `BaseResource.upgrade_state(version, raw_state)` migrates data written under an older one, mirroring the `s_identity` / `upgrade_identity` pair that already existed for identity. `version` is the version the state was *written* under, so a resource that has migrated more than once can branch on it. The default stays 1, which is what every pyvider resource has advertised since the framework began, so existing providers are unchanged and the hook costs a resource that never bumps its version nothing.
- **An upgrade the current schema rejects fails the RPC instead of being written to state.** The hook returns plain Python and nothing else checked it, so a migration that dropped a required attribute or changed a type would have persisted state the provider cannot read back — the very failure the version bump exists to prevent. The result is now validated against the current schema, and a failure returns a diagnostic naming the resource and both versions with no `upgraded_state`, leaving the stored state alone.

### Changed

- **`UpgradeResourceState` now resolves the resource it was asked about**, and reports an unregistered type as an error rather than passing the state through. It has to: the resource is what knows the version to compare against. This matches `UpgradeResourceIdentity` and terraform-plugin-framework, and Terraform only calls this RPC for types the provider advertised, so an unresolvable one is a provider bug.

## [0.6.0] - 2026-08-29

A release of defect fixes, most of them found by a full-codebase audit and
each of which produced a wrong answer rather than an error. Several were
silent: the apply reported success and the practitioner learned about it
later, or never.

### Breaking

- **`a_obj()` attributes are sent as `Schema.Attribute.nested_type` rather than a flat object type.** Terraform now sees each member's required/optional/computed flags, so members marked optional can be omitted individually instead of the whole object being all-or-nothing. This changes the `GetProviderSchema` payload for any provider using `a_obj()`, and an `object_type` carrying `block_types` is now rejected at `GetProviderSchema` rather than silently producing a schema Terraform reads differently than the author intended.
- **`requires_replace` is now rejected at schema-definition time where it never worked.** On a write-only attribute, and inside a nested block or object-typed attribute, the flag was read by nothing. Declarations that were silently inert now raise `ValueError` naming the offending path. See *Fixed* below for what to use instead.
- **A `default=` on an identity attribute is now an error.** Identity is assigned by the provider at create and read back verbatim on import, so a default can never apply.

### Added

- **`PvsAttribute.default` is applied to configuration and to plans.** The plugin protocol has no field for a default: Terraform sends an omitted attribute as null and never learns what the provider considers the default, so the provider is the only party that can resolve one — and it has to do so before anything reads the configuration, not only while planning. Defaults now resolve into the decoded configuration, so `ctx.config` reports them, and are reconciled into the plan at the protocol boundary after the resource's `plan()` hook, so the plan and the configuration agree and apply returns a state Terraform planned. They resolve recursively, inside `a_obj()` attributes and nested blocks, to any depth. A default implies Computed, since Terraform only lets a provider plan a value the configuration does not contain for a computed attribute. Deleting an argument now reverts it to its default rather than keeping the value the resource last had.
- **Resources can force replacement instead of an in-place update.** `PlanResourceChange` never populated `requires_replace`, so an attribute the remote API cannot change — a region, an availability zone, an immutable name — was planned as an update and the provider's `_update_apply()` was asked to perform something it could not do. Two ways to say so: `requires_replace=True` on a schema attribute, the equivalent of the SDK's `ForceNew` and the plugin framework's `RequiresReplace()`, which compares the planned value against prior state; and `ctx.require_replace(path)` for replacement that depends on the values themselves rather than on the mere fact of a change. Neither reports anything on create or destroy, where Terraform rejects replacement paths, and a planned value that is still unknown counts as a change because the plan has to be decided before the value resolves.

### Fixed

- **A wrong answer came back from any function with a defaulted parameter.** `_extract_parameters_meta` promotes a Python parameter carrying a default into the schema's `variadic_parameter`, because tfproto v6 has no optional positional parameter. But `_process_function_arguments` bound trailing arguments only after finding a `VAR_POSITIONAL`, and a defaulted parameter is `POSITIONAL_OR_KEYWORD` — so the argument was unmarshalled, checked for unknowns, converted to native, then matched nothing and was dropped. `repeat("ab", 5)` returned `"abab"`. No error, no diagnostic, no log line above debug: the handler reported "Function executed successfully" and Terraform recorded the answer.
- **A truncated write destroyed good state and reported it as a warning.** `WriteStateBytes` persisted the received bytes and *then* compared them against the client-declared `total_length`. Terraform does not fail an apply on a warning, so a stream ending short — an aborted apply, a half-closed connection, a dropped chunk — overwrote existing state with a partial one and the apply reported success. The length is now checked before the write, and a mismatch is an ERROR that stores nothing.
- **A state-store backend failure panicked Terraform instead of showing its diagnostic.** The `ReadStateBytes` error path omitted the `range` that the empty-state path had been given, and Core dereferences `chunk.Range.End` without a nil check.
- **A name ending in a dot was stored under a name the encoder could not reproduce.** Windows drops trailing dots from a path component, so `foo..` was written to `foo` and read back as `foo`, and four of the seven traversal fixtures raised on Windows where they were quietly confined on POSIX. Confinement itself always held — nothing was ever written outside the root.
- **`pyvider.toml` was parsed, logged as loaded, and then ignored.** `PyviderConfig` documents "Environment Variable > Config File > Default" and never implemented the middle term: the parsed document was kept in `_config_data`, which only `get()` consults, and `get()` returns a typed field before it looks there. The sharp end was private state — `docs/schema/sensitive-data.md` tells operators to write `private_state_shared_secret` into `pyvider.toml`, and doing exactly that failed every plan and apply with a message telling them to do the thing they had just done. `[logging] level` is now recognised as the documented spelling of `log_level`.
- **`MoveResourceState` accepted every move and copied state between unrelated types.** The handler answered yes for any pair of types and wrote `source_state.json` straight into `target_state`, private state included — bytes written by one type's `private_state_class` handed to another's. Nothing downstream re-validates a moved state, so the practitioner met it later as an unexplained diff or a failure inside a resource they had not touched. The target resource now decides, matching terraform-plugin-framework: no `MoveState` implementation means refusal.
- **`@requires_capability` never injected anything from a sync method.** The sync wrapper read `_parent_capability` off the undecorated function; the decorators stamp it on the class. Every sync method fell through to the "provider" default and returned without injecting — silently, because injecting nothing is also correct for a provider-level component.
- **The safety net under `_delegate` had never run.** Both recovery branches looked up their response with `getattr(pb, f"{method}.Response", None)`, and an attribute name containing a dot is never an attribute, so that expression was `None` for every method. An exception escaping a handler re-raised into gRPC instead of becoming the diagnostic the code had carefully composed, and an RPC with no registered handler returned `None` and failed on serialisation. The response class now comes from the service descriptor, which is the only thing that knows `ValidateStateStoreConfig` answers with a `ValidateStateStore.Response`.
- **`is_valid_refinement` rejected refinements its own docstring calls valid.** The null check ran before the unknown short-circuit, so `unknown(string) -> null(string)` was refused as "non-null in plan but became null in result", and the structural branches ran before it too, making `if plan.is_unknown: return True` unreachable for every object, list and tuple. Maps and sets had no branch at all.
- **Set and list elements now receive the defaults their configuration resolved.** The element matcher skipped every attribute carrying a default, so two set elements sharing all their non-defaulted attributes matched both configurations, nothing paired, and neither got its default — the plan promised null for an attribute `ctx.config` reported as the default value.
- **`requires_replace` no longer looks effective on a write-only attribute while doing nothing.** Terraform requires write-only values to be null in both prior and planned state, so the plan comparison always saw `null == null` and an attribute declared `write_only=True, requires_replace=True` never once produced a replacement path — a silent no-op on exactly the attributes whose rotation most needs one. To rotate a write-only secret, pair it with a companion attribute the practitioner bumps — conventionally `<name>_wo_version` — and set `requires_replace=True` on that, or call `ctx.require_replace()` from the plan hook.
- **`requires_replace` no longer looks effective inside a nested block or an object-typed attribute.** Replacement is decided from a flat list of attribute paths, and an attribute inside a block has no stable path until Terraform matches the block's elements between prior and planned state, so the flag was read by nothing and the practitioner got an in-place update the remote API could not honour — discovered at apply time. Use `ctx.require_replace()`, which runs where the changed element is known.
- **Attribute paths in diagnostics are parsed by `CtyPath.parse` rather than a regex.** The old pattern split `retention-days` into `["retention", "days"]`, silently accepted the unterminated `tags[0`, and read `items[0]extra` as three steps. An unparsable path is now dropped with a warning rather than pointing Terraform at an attribute that does not exist.
- **Blocking filesystem calls on the event loop.** `FileSystemStateStore.validate` and `.configure` ran `stat` and `expanduser` inline in `async def`, on the loop serving every other RPC; the rest of that module already hands blocking work to `asyncio.to_thread`.
- **`tfprotov6/adapters/` shipped as an implicit namespace package.** It had no `__init__.py` while both its siblings did, which a stricter build backend would silently drop from the wheel.

### Changed

- **Requires `pyvider-cty>=0.5.2`**, for `CtyPath.parse(..., within=)`, which resolves set-versus-map bracket ambiguity from the schema rather than guessing.
- **Ruff now gates on the rule families that catch defects** — `ASYNC`, `G`, `LOG`, `ISC`, `INP`, `PGH`, `T20`, `DTZ`, `SLF`, `RET`, `RSE` and others — rather than on style. `select = ["ALL"]` was measured and rejected: ~1900 findings, mostly docstring and annotation policy that would bury the rules that matter.
- **Every function in `src/` is under a McCabe complexity of 8**, with `PLR0912` and `PLR0915` on at ruff's defaults and no per-file suppressions. 20 functions were over the ceiling; `create_diagnostic_from_exception` was at 14 and `_read_resource_impl` at 74 statements and 14 branches.

## [0.5.3] - 2026-08-22

### Fixed


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
