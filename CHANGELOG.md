# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Breaking

- **A schema Terraform would reject at `terraform init` is now rejected where
  it is written.** Terraform runs `Block.InternalValidate()` over every managed,
  data, ephemeral and list schema as it loads a provider, and one violation
  takes the whole provider down with "provider ... has invalid schema ... which
  is a bug in the provider", naming the provider rather than the declaration
  that caused it. None of those rules were checked here, and eleven invalid
  shapes were accepted: a single block requiring two elements, a single block
  with mismatched bounds, a group or map block carrying item counts, a list
  with a minimum above its maximum, a set block containing a dynamic or
  write-only attribute, an attribute and a block sharing a name, an uppercase
  block name, and negative counts. Write-only on a provider or data source
  schema is refused too, as terraform-plugin-sdk refuses it: Terraform's
  write-only enforcement only runs against managed resources, so anywhere else
  the flag is advertised and never enforced. A provider carrying one of these
  will now fail its own test run rather than every practitioner's `init`.
- **A state or config class that requires a field its schema does not declare
  now raises `StateClassMismatchError`.** It previously converted to None, and
  None was read as "Terraform asked for a destroy" -- see the fix below.
- **`a_list`, `a_set` and `a_map` refuse an `a_obj` element whose members carry
  `computed`, `sensitive`, `write_only` or a default.** Those flags reach
  Terraform only through a nested type, which this framework does not yet emit
  for collection nesting, so they were being dropped silently. Declaring the
  same shape without them still works; a nested block carries them today.
- **State locks no longer expire by default.** See below.

### Added

- **A resource's returned state is checked against its schema.**
  `complete_state_dict()` walks every attribute the schema declares. Write-only
  attributes are forced to null, matching the documented contract. Any other
  attribute the resource left out raises `IncompleteResourceStateError`, which
  names the resource type, the attribute, and the state class to fix — where
  previously the omission fell through to a generic "Missing required
  attribute" raised deep inside `pyvider-cty`, with nothing to say which
  resource produced it. `apply_resource_change` and `read_resource` both call
  the one shared helper instead of each hand-rolling the write-only set.
- **`pyvider.testing.assert_schema_state_parity()`** fails a resource author's
  own test suite when a non-write-only schema attribute has no matching field
  on the state class — the same predicate the runtime check enforces, applied
  statically. A Go provider cannot construct an incomplete state value at all:
  `tftypes.NewValue` panics on a mismatched attribute set, and
  `terraform-plugin-framework`'s `resp.State.Set` requires a struct field per
  schema attribute. An attrs state class carries no such invariant, so this is
  the closest Python equivalent. It lives here rather than in
  `provide-testkit`, which is schema-agnostic and sits below pyvider in the
  dependency graph; pyvider is the only package that can see both halves of the
  comparison.

### Changed

- **`pyvider-cty>=0.5.3`** (was `>=0.5.2`). The lock has resolved 0.5.3 since it
  was published, so the declared floor promised a combination nothing here had
  run. 0.5.3 also types `CtyObject.optional_attributes` precisely enough that
  two `# type: ignore[arg-type]` comments here became unused, and mypy strict
  rejects those, so they are gone. Verified at the floor with
  `uv lock --resolution lowest-direct`.
- **`provide-testkit>=0.4.5`** (was `>=0.4.0`), in the `dev` and `docs`
  dependency groups only, so there is no runtime effect on a provider that
  installs pyvider. The lock was at 0.4.3 when the floor was raised, so 0.4.4
  and 0.4.5 satisfied the declared floor without anything here having run
  against them. (An earlier wording said the lock "had only ever resolved
  0.4.3"; it had also resolved 0.4.0 and 0.4.2 under the same floor.)

### Removed

- **The `google` dependency.** It is the Google-search scraper package, pulled
  into every provider install, and nothing here imports it.

### Fixed

- **A resource could be destroyed by an update.** `BaseResource.apply` chose
  between create, update and destroy by asking whether `ctx.planned_state` is
  None. That is derived data: the planned state is produced by converting the
  planned value into the resource's attrs state class, and the converter
  returned None whenever the class could not be constructed. So a state class
  requiring a field its schema does not declare -- an ordinary authoring
  mistake -- was read as a destroy. On a create that produced a null state and
  Terraform's "inconsistent result after apply"; on an update it ran the
  resource's own `_delete_apply` against a live object, with `ctx.state` also
  None, so the resource was destroyed on no information. Terraform says it
  wants a destroy by sending a null `planned_state` and in no other way, so
  that is what the decision is taken from now.
- **A value referencing another resource crashed the plan.** Conversion
  recognised an unknown by identity against the unrefined singleton. Terraform
  refines an unknown whenever it knows something about a value it cannot yet
  compute, and `targets = other_resource.some_list` arrives refined, as a
  different object -- which fell through to the list branch and raised
  `TypeError: 'RefinedUnknownValue' object is not iterable`, reaching the
  practitioner as "Internal Provider Error" on every plan. go-cty has emitted
  refinements since Terraform 1.6.
- **`terraform plan` never came back empty for a resource with an
  optional+computed attribute.** Every such attribute the plan hook did not set
  was re-planned unknown on every run, regardless of state. If the API returned
  null, the null was replaced by unknown; if it returned a value, the value was
  discarded. With `requires_replace` the attribute then landed in the
  replacement paths, so the resource was destroyed and recreated on every plan.
  Terraform's own `ProposedNew` carries the prior value forward for an
  optional+computed attribute whose configuration is null, and so does this.
- **Private state was erased by the first plan after a create.** Terraform
  records whatever the plan and apply return and hands it back as
  `prior_private` next time, so returning nothing erases it rather than leaving
  it alone. Both handlers set the field only when the resource's hook produced
  an object, and the default `_update` returns none -- so any lease, token or
  bookkeeping a resource established at create was lost.
  terraform-plugin-sdk defaults the other way, and now so does this.
- **A decrypt failure at plan time was swallowed.** Failing to decrypt private
  state and failing to rebuild the object from it were caught together and both
  reported as "may be expected if the resource schema changed". Only the second
  is recoverable. A rotated or lost `PYVIDER_PRIVATE_STATE_SHARED_SECRET`
  produced a clean-looking plan and an apply that failed on the same bytes.
- **Ctrl-C during an apply cut the provider off mid-call.** `StopProvider`
  scheduled a server stop shortly after replying, which tore down the gRPC
  server, unlinked the socket and exited. Terraform's Stop is advisory: it asks
  in-flight work to wind up and then waits for it to return, and stopping the
  process is a separate step it drives itself. An interrupted
  `ApplyResourceChange` failed with `Unavailable` and a resource created
  remotely never reached state. It now raises a provider-wide signal, readable
  from any context as `ctx.stop_requested`, so a resource polling an API can
  return early and be accounted for.
- **A state lock could be taken from a running apply.** Locks were leased for
  five minutes and an expired lease was reclaimable by any other process.
  Terraform acquires a state lock once per operation and never renews it, so
  any apply longer than the lease -- an ordinary size of infrastructure -- could
  be joined by a second writer, and the first writer's own `UnlockState` was
  then refused. The default is no expiry; `terraform force-unlock <ID>` is the
  standard answer for a stale lock and already works. Expiry remains available
  and now warns when configured.
- **Write-only values reached Terraform on three paths.** The nulling was done
  in two places and neither covered the contract: the plan path went through a
  `BaseResource` helper that a resource overriding `plan()` skips, and the
  apply and read path iterated only top-level attributes, so a write-only
  attribute inside a nested block or an `a_obj` was untouched. Import, upgrade
  and move did none of it, and import additionally failed with "Missing
  required attribute" when the state class did not carry the field. It is now
  one recursive pass at the protocol boundary on all six paths.
- **`ctx.capabilities` was the wrong object.** Every resource handler populated
  it from `provider_instance.metadata.capabilities` -- a flags struct describing
  what the provider supports -- rather than the configured capability instances.
  The documented `ctx.capabilities["auth"]` raised `TypeError`, and there was no
  way to reach a capability from a resource at all.
- **A null function argument shifted every argument after it.** An argument
  whose Python parameter carries a default is dropped so the default applies,
  and the remaining arguments were then rebuilt as a positional list, so
  `pad("x", null, "-")` bound `fill` to `width`. No error, just the wrong
  answer. Arguments are bound by name now wherever Python allows it.
- **`FunctionError.function_argument` reached the wire for the first time.**
  Terraform uses it to point at the offending expression rather than the call as
  a whole; the conversion was a commented-out placeholder, so every function
  error pointed at the whole call.
- **An ephemeral resource that keeps no private state could not be closed.**
  Close and Renew required a `private_state_class` and unpacked the private
  bytes unconditionally, and unpacking empty bytes raises. Terraform closes
  every ephemeral resource it opened, so the ordinary case -- one that just
  reads a value -- failed on every close.
- **A provider block carrying an unknown value failed the plan.** The deferral
  was guarded on the whole configuration being unknown, which Terraform never
  sends; what it does send during plan and apply is a known object with an
  unknown inside it. That fell through to a hard error, while the log line above
  it said the configuration was being deferred.
- **A set block element could take a neighbour's configured values.** Elements
  are paired with their configuration by value, because a set has no order, but
  that pairing was skipped when the plan held exactly one element -- which then
  took configuration element zero. A plan hook dropping one element of a
  two-element set handed the survivor the other's explicit values.
- **`terraform plan -generate-config-out` produced configuration Terraform
  rejects.** When a resource does not override `generate_config`, the handler
  forwarded the state verbatim, so the generated file assigned computed-only
  attributes such as `id`. The state still stands in, reduced to what a
  configuration may contain.
- **Numbers lost precision on upgrade and move.** State JSON was decoded with
  binary floats where Terraform's numbers are arbitrary precision, so a value
  that arrived exact went back out rounded -- a diff on an attribute nobody
  touched.
- **`UpgradeResourceState` invented state that was not there.** An absent raw
  state was answered with an empty JSON object, which describes a *present*
  object with every attribute null. Flatmap state, written by Terraform 0.11,
  fell through the same branch and was quietly emptied; it is refused now.
- **A cross-type move dropped identity and was never validated.** The hook's
  output went to Terraform unchecked, and identity was carried only by the
  same-type pass-through, so a moved resource arrived at its new type without
  one.
- **The magic cookie was compared against itself,** so any value was accepted
  and the "this binary is a plugin" guard never fired. The provider-detection
  error also printed to stdout, which carries only the go-plugin handshake
  line -- so the explanation became the thing Terraform reported as garbage.
- **A list resource with no managed resource of the same name is now
  reported.** Terraform resolves a list resource's results against the managed
  type of the same name and refuses to list when there is none. Nothing checked
  it, and the architecture documentation, the end-to-end test and the
  list-resource fixtures all demonstrated the shape that fails.
- **An attribute's `description_kind` never reached the wire,** so a
  description written as Markdown was published as plain text.
- Identity attributes may be a list of scalars, which Terraform allows and this
  refused. `PlanAction` may only defer for an unknown provider configuration,
  which is the only reason Terraform accepts. `GetFunctions` honours test-mode
  filtering, as `GetProviderSchema` already did. The derived-key cache is
  bounded; it was keyed on a per-call random salt, so it never hit and grew for
  the life of the process. The ephemeral handlers raise a typed error instead of
  a bare `ValueError`, which reached Terraform as "Internal Provider Error" with
  the explanation stripped.

- **A required write-only attribute no longer breaks apply.** Applying a
  resource with a `required` + `write_only` attribute failed with
  `CtyAttributeValidationError: Missing required attribute` whenever the state
  class did not carry the attribute — which is the natural way to model a value
  that is never stored. Write-only attributes were nulled only where the key was
  already present, so a state dict that omitted it stayed omitted, and the cty
  object validator, which has no notion of write-only, rejected it. In a cty
  object every attribute exists in the type, so absent is not a state the value
  can be in; null is how "no value" is spelled, and it is now written
  unconditionally. This is what the architecture documentation already
  described: write-only attributes are nullified on outbound state regardless
  of `write_only_attributes_allowed`, so that an older Terraform cannot store
  the secret in plain text. It also removes the workaround of declaring the
  attribute on the state class purely to satisfy the validator.
- **The documentation link checker says what it checked.** It printed a file
  count, then nothing, then exited 0 — so "every link resolved" and "no link was
  looked at" were indistinguishable. It now reports
  `✅ 451 internal links across 78 files all resolve`, and fails when extraction
  finds no internal links at all rather than passing on having verified nothing.
- `assert_schema_state_parity` raises `AssertionError` directly instead of using
  a bare `assert`, which `python -O` strips. The check is meant to be
  unconditional, like the runtime one it complements.

## [0.6.2] - 2026-08-31

### Fixed

- **The development-mode wrapper moved the provider out of Terraform's working directory.** The script written by `pyvider install` ran `cd "$INSTALL_DIR"` before exec'ing the provider. Terraform launches the provider as a subprocess, so the provider inherits Terraform's working directory — and that is what every relative path in a configuration resolves against. The `cd` silently repointed all of them at the provider's own checkout: `path.module`, `path.root` and any bare `./file` resolved somewhere the practitioner had never named, and could even succeed by matching an unrelated file there, which is worse than failing. The filesystem state store was caught by the same thing, since its default root is `Path.cwd() / .pyvider/state`; practitioner state was being written inside the provider repository. Nothing in the script needed a particular directory — every path in it is absolute. The provider's own `pyvider.toml` was the one thing the `cd` was doing real work for, so it is now pinned explicitly with `PYVIDER_CONFIG_FILE` when the checkout has one, which is also more precise than the old behaviour: previously any `pyvider.toml` sitting in the Terraform directory would have been picked up instead.

## [0.6.1] - 2026-08-31

### Fixed

- **A broken lifecycle contract would not say which attribute broke it.** `is_valid_refinement` already walks the object and prefixes the offending attribute onto its reason, and `ResourceLifecycleContractError` carries that as `detail`, but none of it reached the practitioner. The error extends foundation's `StateError` rather than `PyviderError`, so it missed the `except (CtyValidationError, PyviderError)` clause that routes to the diagnostic builder — and the diagnostic builder is what appends the detail. It fell to the generic handler, which rebuilds the message from `str(e)` alone and reports only that "the final state returned by the resource's apply method is not a valid refinement of the planned state". The only way to find the attribute was to bisect the resource. It now names it.
- **The provider name in `[tool.pyvider]` was read under one spelling and written under another.** The resolver looked for `provider_name`; `pyvider.toml` and plating both look for `name`, the tutorial showed `provider_name`, and the two shipped provider repositories had one of each. A name written under the spelling the resolver did not want was not an error — it fell through to the default, `pyvider`, and the provider installed to `local/providers/pyvider/` under the binary name `terraform-provider-pyvider`. Since that is a valid provider in a valid location, nothing failed: Terraform simply never found the checkout where the examples asked for it, and resolved whatever else was in the plugin directory instead. One repository had been testing a nine-month-old prebuilt binary this way. `name` is now the documented key and `provider_name` is accepted as an alias, in `[tool.pyvider]`, in the top-level `[pyvider]` table, and in `pyvider.toml`.
- **`pyvider.toml` was consulted for the provider name only when `PYVIDER_CONFIG_FILE` pointed at it.** `PyviderConfig` loads that file from the working directory by default, so its `[pyvider] name` was inert in every ordinary checkout while appearing, in the file and in the tests, to work.
- **`pyvider install` now prints where the name came from,** and says so when it had to fall back to the default, since the failure has no other symptom at install time.

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
- **Resources can version their state schema and migrate it.** `UpgradeResourceState` was a documented pass-through, and correct only because `s_resource` accepted no version: the stored version could never differ from the advertised one, so the RPC was never asked to do anything. That held right up until a provider author changed a resource's state shape — a renamed attribute, a changed type, one attribute split into two — at which point they had no way to signal it, Terraform handed the old state to the new schema, and the result was a decode error at best and a silent mis-read at worst. The workaround was to tell practitioners to `terraform state rm` and re-import, which is the migration the provider was supposed to perform for them. Now `s_resource(..., version=N)` declares the version, and `BaseResource.upgrade_state(version, raw_state)` migrates data written under an older one, mirroring the `s_identity` / `upgrade_identity` pair that already existed for identity. `version` is the version the state was *written* under, so a resource that has migrated more than once can branch on it. The default stays 1, which is what every pyvider resource has advertised since the framework began, so existing providers are unchanged and the hook costs a resource that never bumps its version nothing.
- **An upgrade the current schema rejects fails the RPC instead of being written to state.** The hook returns plain Python and nothing else checked it, so a migration that dropped a required attribute or changed a type would have persisted state the provider cannot read back — the very failure the version bump exists to prevent. The result is now validated against the current schema, and a failure returns a diagnostic naming the resource and both versions with no `upgraded_state`, leaving the stored state alone.

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
- **`UpgradeResourceState` now resolves the resource it was asked about**, and reports an unregistered type as an error rather than passing the state through. It has to: the resource is what knows the version to compare against. This matches `UpgradeResourceIdentity` and terraform-plugin-framework, and Terraform only calls this RPC for types the provider advertised, so an unresolvable one is a provider bug.

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
