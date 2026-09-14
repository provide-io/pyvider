# Provider-Native Linting Through Staging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the approved provider-native lint author API, seven first-party rules, packaged OpenTofu and TofuSoup proof, checked recording and manifest, and a verified Cloudflare Pages feature preview.

**Architecture:** `pyvider.lint` owns immutable protocol-neutral findings, selectors, contexts, and a shared fail-open runner. Each validation handler invokes that runner only after successful semantic validation, then an isolated tfprotov6 compatibility adapter emits ordinary warning diagnostics. `pyvider-components` supplies seven pure rules without protocol imports. The actual provider builds a package from exact Pyvider/component source revisions and drives it both through OpenTofu v1.13.0-beta1 and TofuSoup's direct client; its checked artifacts are synchronized into the Hugo site and deployed only to a feature-branch Pages preview.

**Tech Stack:** Python 3.11+, attrs, pytest/pytest-asyncio, Pyvider tfprotov6, TofuSoup, Flavorpack, OpenTofu v1.13.0-beta1, asciinema v2, GitHub Actions, Hugo, Cloudflare Pages/Wrangler.

---

## Execution contract

Use these isolated worktrees throughout:

- Pyvider: `/Users/tim/.config/superpowers/worktrees/pyvider/provider-linting`
- Components: `/Users/tim/.config/superpowers/worktrees/pyvider-components/provider-linting`
- Actual provider: `/Users/tim/.config/superpowers/worktrees/terraform-provider-pyvider/provider-linting`
- Website: `/Users/tim/.config/superpowers/worktrees/site-pyvider-com/provider-linting`

The untouched baselines recorded before this plan were:

- Pyvider: `2384 passed, 3 skipped, 2 xfailed`
- Components: `353 passed`
- Packaged provider: `87 passed`
- Hugo production build: success, 23 pages and 155 static files

For every numbered task below, the primary agent must perform this exact subagent-driven gate before checking off the task:

1. Dispatch a fresh implementer with the complete task text and require `superpowers:test-driven-development`.
2. Require the implementer to show the focused test failing for the expected missing behavior before production edits, make it pass, run the named regression checks, self-review, and commit.
3. Dispatch a fresh independent spec-compliance reviewer. Resolve every finding with the implementer and repeat spec review until approved.
4. Dispatch a fresh independent code-quality reviewer. Resolve every finding with the implementer and repeat quality review until approved.
5. Record the approved commit SHA and update this plan's checkboxes.

The initial aggregate-red commands below are only collection/surface checks; they do not authorize a bulk implementation. Within every task, the implementer must use this micro-cycle for each independently named test or parameter family: add exactly one failing expectation, run `uv run pytest path/to/test.py::exact_test_name -q` (or the repository's exact `python3 -m unittest module.Class.test_name -v` equivalent), paste the expected assertion/import failure into the task report, implement only enough production code for that expectation, rerun the same node green, then proceed to the next expectation. Documentation/source checkers follow the same one-assertion red/green cycle. A task report without the observed red command and reason for every production behavior is rejected by the spec reviewer.

Tasks sharing a repository run sequentially. Cross-repository ordering is Pyvider → components → actual provider → website. Do not edit `/Users/tim/code/tf/opentofu`.

Before Task 1, commit this plan on `codex/provider-linting` with `git add docs/superpowers/plans/2026-09-13-provider-linting.md && git commit -m 'docs: plan provider-native linting'`, then require `git status --porcelain` to be empty in all four worktrees. This makes the plan itself part of the clean Pyvider revision later archived by Task 8.

### Normative interfaces used by every task

These names/signatures are the cross-task contract. Private helper decomposition may vary, but no implementer may rename or reinterpret these interfaces without first updating the plan and passing spec review.

```python
# pyvider.lint
ConfigT = TypeVar("ConfigT")

@define(frozen=True, slots=True)
class LintFinding:
    rule: str
    groups: tuple[str, ...]
    summary: str
    detail: str
    attribute_path: str | None = None

@define(frozen=True, slots=True)
class LintSelector:
    include: frozenset[str] = frozenset()
    exclude: frozenset[str] = frozenset()

    @classmethod
    def parse(cls, values: Iterable[object]) -> "LintSelector": ...
    @property
    def is_disabled(self) -> bool: ...
    def as_tokens(self) -> tuple[str, ...]: ...
    def enabled(self, rule: str, *groups: str) -> bool: ...

@define(frozen=True, slots=True)
class LintContext(Generic[ConfigT]):
    config: ConfigT
    selector: LintSelector
    def enabled(self, rule: str, *groups: str) -> bool: ...

# pyvider.lint._runner
@define(frozen=True, slots=True)
class LintRunResult:
    findings: tuple[LintFinding, ...] = ()
    failed: bool = False

async def run_lints(
    component: object,
    config: object | None,
    selector: LintSelector,
    *,
    kind: str,
    name: str,
    operation: str,
) -> LintRunResult: ...

# pyvider.protocols.tfprotov6.handlers._linting
async def lint_diagnostics(
    component: object,
    config: object | None,
    *,
    kind: str,
    name: str,
    operation: str,
) -> list[pb.Diagnostic]: ...
```

The bodies represented by type-stub ellipses above are fully constrained by the task assertions: addresses use `RULE_ADDRESS.fullmatch`; blank text/path raises `ValueError`; `parse` trims strings, strips one leading `!` into exclusion, logs/ignores non-string, blank, and grammar-invalid values, de-duplicates through frozensets, and removes same-level conflicts from `exclude`; `is_disabled` is true only when both sets are empty; `as_tokens` returns sorted includes followed by sorted exclusions prefixed with `!`; context delegates `enabled`; the runner skips absent config/disabled selectors/missing hooks, validates every returned type, defensively selects findings, catches all hook failures, and never logs config; the adapter reads only the startup `lint_selector`, maps warnings and top-level paths, and emits one generic failure warning.

The exact public hook on all seven bases is `async def lint(self, ctx: LintContext[Any]) -> Sequence[LintFinding]`, narrowed with the class's config type where available. The seven implementation conditions are exactly: `api_insecure_skip_verify is True`; parsed octal permissions have `& 0o002`; lowercase URL starts with `http://`; `include_hidden is True`; `ttl_seconds > 3600`; `timeout_seconds > 300`; and `not Path(str(path)).expanduser().is_absolute()`. `None`, framework unknowns, unparsable permissions, and values whose comparison raises produce no finding.

The exact executable interfaces are:

```text
ci/build-provider-linting-stack.py --pyvider-source PATH --components-source PATH --output-dir PATH
ci/run-provider-linting-rpcs.py --binary PATH --selector SELECTOR --format json-lines
ci/install-opentofu-beta.sh --version 1.13.0-beta1 --cache-dir PATH
ci/generate-provider-linting-proof.py --cast PATH --build-provenance PATH --output PATH
ci/verify-provider-linting-proof.py MANIFEST CAST
scripts/sync-provider-linting-proof.py --repository OWNER/REPO --run-id INTEGER --artifact NAME --expected-provider-sha SHA
scripts/verify-provider-linting-proof.py MANIFEST CAST
scripts/check-linting-site.py PUBLIC_DIR
scripts/check-pages-preview-target.py PROJECTS_JSON PROJECT_NAME FEATURE_BRANCH
scripts/smoke-linting-preview.py BASE_PREVIEW_URL
```

Each CLI must use `argparse` (shell installer excepted), return zero only after all assertions succeed, return nonzero with a concise stderr reason on invalid input, and avoid serializing absolute source paths into proof artifacts.

The exact test-node families are `test_lint_finding_*`, `test_lint_context_*`, `test_selector_*`, `test_lint_config_*`, `test_register_runtime_config_*`, `test_run_lints_*`, `test_data_source_lint_*`, `test_base_lint_hook[provider|resource|data_source|ephemeral|list|action|state_store]`, `test_handler_lint_contract[provider|resource|data_source|ephemeral|list|action|state_store]`, `test_security_lint_rule[insecure_tls|world_writable_directory|insecure_http|include_hidden_files]`, `test_reliability_lint_rule[long_lived_lease|long_action_timeout|relative_state_store_path]`, `test_build_stack_*`, `test_packaged_lint_rpc[provider|resource|data_source|ephemeral|list|action|state_store]`, `test_opentofu_lint_*`, `test_proof_*`, `test_sync_*`, `test_linting_site_*`, and `test_preview_*`. Parameter IDs must use the strings shown so every micro-cycle has an addressable node such as `tests/conformance/test_provider_linting.py::test_packaged_lint_rpc[action]`.

## Task 1: Public lint model, selector, and configuration precedence

**Repository:** Pyvider

**Files:**

- Create: `src/pyvider/lint/__init__.py`
- Create: `src/pyvider/lint/model.py`
- Create: `src/pyvider/lint/selector.py`
- Modify: `src/pyvider/common/config.py`
- Modify: `src/pyvider/cli/provide_command.py`
- Modify: `src/pyvider/hub/components.py`
- Create: `tests/lint/test_model.py`
- Create: `tests/lint/test_selector.py`
- Create: `tests/lint/test_config.py`
- Create: `tests/cli/test_lint_selector_registration.py`

- [x] Write model tests that construct immutable `LintFinding` and `LintContext` values, reject a non-matching rule or group address, reject blank summary/detail/attribute paths, normalize `groups` to a tuple, and prove `ctx.enabled()` delegates to its selector.
- [x] Write selector tests copied semantically from OpenTofu `internal/tfdiags/lint_test.go`: exact rule include, exact rule exclude, any included group, any excluded group, global `all`, namespaced `provide-io/pyvider:all`, same-level include/exclude conflict with inclusion winning, whitespace trimming, duplicate removal, malformed-entry logging/ignore, unknown valid selectors as no-ops, and no selectors as disabled.
- [x] Run `uv run pytest tests/lint/test_model.py tests/lint/test_selector.py -q` and observe collection/import failure because `pyvider.lint` does not exist.
- [x] Implement the immutable public objects with the exact OpenTofu grammar:

  ```python
  RULE_ADDRESS = re.compile(r"^([a-z0-9]+[a-z0-9_\-/]*:)?[a-z0-9]+[a-z0-9_\-]*$")

  @define(frozen=True, slots=True)
  class LintFinding:
      rule: str = field(validator=_valid_address)
      groups: tuple[str, ...] = field(converter=tuple, validator=_valid_addresses)
      summary: str = field(validator=_not_blank)
      detail: str = field(validator=_not_blank)
      attribute_path: str | None = field(default=None, validator=_optional_not_blank)

  @define(frozen=True, slots=True)
  class LintSelector:
      include: frozenset[str] = field(factory=frozenset, converter=frozenset)
      exclude: frozenset[str] = field(factory=frozenset, converter=frozenset)

      def enabled(self, rule: str, *groups: str) -> bool:
          if rule in self.include:
              return True
          if rule in self.exclude:
              return False
          if any(group in self.include for group in groups):
              return True
          if any(group in self.exclude for group in groups):
              return False
          return "all" in self.include
  ```

  Parsing treats `provide-io/pyvider:all` as an ordinary group selected by each finding's declared group list; only unqualified `all` is the global fallback.
- [x] Write one config test at a time, running it red before implementation, for `[lint].rules`, `PYVIDER_LINT` comma parsing, explicit empty environment disablement, malformed permissiveness, and `PYVIDER_LINT > [lint].rules > ()`. A non-array TOML `rules` value must log one warning and resolve to disabled; it must not be silently accepted or raise.
- [x] Run `uv run pytest tests/lint/test_config.py -q` and observe failures because `PyviderConfig` has no `lint_rules`.
- [x] Add `lint_rules: tuple[str, ...]` to `PyviderConfig` and load it after TOML parsing with this source decision:

  ```python
  raw_env = os.environ.get("PYVIDER_LINT")
  if raw_env is not None:
      raw_rules: object = raw_env.split(",") if raw_env else ()
  else:
      lint_table = self._config_data.get("lint", {})
      raw_rules = lint_table.get("rules", ()) if isinstance(lint_table, dict) else ()
  selector = LintSelector.parse(raw_rules if isinstance(raw_rules, list | tuple) else ())
  object.__setattr__(self, "lint_rules", selector.as_tokens())
  ```

  Do not use `get_env` for `PYVIDER_LINT`, because an explicitly empty value must remain distinguishable from an absent variable.
- [x] Add `tests/cli/test_lint_selector_registration.py::test_register_runtime_config_publishes_selector_before_server_start`, run `uv run pytest tests/cli/test_lint_selector_registration.py::test_register_runtime_config_publishes_selector_before_server_start -q`, and observe failure because no `lint_selector` singleton exists. Extract a small `_register_runtime_config(config: PyviderConfig)` helper in `provide_command.py`, call it immediately after `config = PyviderConfig()` and before discovery/protocol/server construction, and register `LintSelector.parse(config.lint_rules)` as `hub.register("singleton", "lint_selector", selector)`. Add the corresponding typed singleton overload in `hub/components.py`. Rerun the same command and expect pass.
- [x] Add a second test that calls the registration helper with `PYVIDER_LINT=''`, proves it replaces an earlier selector with `LintSelector()`, and clean up the singleton in a fixture so no global test state leaks. Run it red, implement only the replacement/cleanup behavior needed, and rerun green.
- [x] Run `uv run pytest tests/lint tests/common/test_config.py tests/common/test_config_file_precedence.py -q`; expect all selected tests to pass.
- [x] Run `we run lint && we run typecheck`; expect exit 0.
- [x] Commit with `git add src/pyvider/lint src/pyvider/common/config.py src/pyvider/cli/provide_command.py src/pyvider/hub/components.py tests/lint tests/cli/test_lint_selector_registration.py && git commit -m 'feat: add provider lint model and selectors'`.

Approved implementation commits: `789f8cd66493e8d5f1fc4b37498616e82cb4ed31`, `a212a4e7e54b569e411373801f42b3c7150c7bcb`. Independent spec review: approved. Independent code-quality review: approved. Fresh full-suite evidence: 2,419 passed, 3 skipped, 2 xfailed; lint and typecheck passed.

## Task 2: Shared runner and first data-source validation path

**Repository:** Pyvider

**Files:**

- Create: `src/pyvider/lint/_runner.py`
- Create: `src/pyvider/protocols/tfprotov6/handlers/_linting.py`
- Modify: `src/pyvider/data_sources/base.py`
- Modify: `src/pyvider/protocols/tfprotov6/handlers/validate_data_resource_config.py`
- Create: `tests/lint/test_runner.py`
- Create: `tests/tfprotov6/handlers/test_provider_linting_data_source.py`
- Modify: `tests/data_sources/test_base_data_source.py`

- [x] Add a default-hook test proving `await ConcreteDataSource().lint(ctx) == ()`.
- [x] Add runner unit tests proving: a disabled selector never calls the hook; `config is None` never calls it; selected findings survive; returned findings are defensively re-filtered; a non-`LintFinding` result and a raised hook become one failure result; exception logs include component kind/name/operation but no configuration value.
- [x] Add handler tests with a fake `provide-io/pyvider:insecure-http` finding proving exact enablement, group enablement, exact exclusion, warning severity, summary `Insecure HTTP endpoint (provide-io/pyvider:insecure-http)`, detail preservation, top-level `url` attribute path, existing validation errors unchanged, no hook after semantic error, no hook for unknown config, and fail-open `Provider linting did not complete` without traceback/secret text. Explicitly unregister `provider_context` in these cases: validation must work before `ConfigureProvider`, and lint selection must come only from the startup `lint_selector` singleton.
- [x] Run `uv run pytest tests/lint/test_runner.py tests/tfprotov6/handlers/test_provider_linting_data_source.py tests/data_sources/test_base_data_source.py -q` and observe failures for the missing hook, runner, and adapter.
- [x] Implement a protocol-neutral result and runner:

  ```python
  @define(frozen=True, slots=True)
  class LintRunResult:
      findings: tuple[LintFinding, ...] = ()
      failed: bool = False

  async def run_lints(component, config, selector, *, kind, name, operation):
      if config is None or selector.is_disabled:
          return LintRunResult()
      try:
          lint = getattr(component, "lint", None)
          if lint is None:
              return LintRunResult()
          findings = tuple(await lint(LintContext(config, selector)))
          if not all(isinstance(item, LintFinding) for item in findings):
              raise TypeError("lint() must return only LintFinding values")
          return LintRunResult(tuple(item for item in findings if selector.enabled(item.rule, *item.groups)))
      except Exception as exc:
          logger.error("Provider linting failed", component_kind=kind, component_name=name,
                       operation=operation, error_type=type(exc).__name__)
          return LintRunResult(failed=True)
  ```

- [x] Isolate all protobuf knowledge in `_linting.py`: read `hub.get_component("singleton", "lint_selector")`; if it is absent or has the wrong type, log one structured warning without configuration values and use `LintSelector()` so every validation RPC remains fail-open before `ConfigureProvider`. Call `run_lints`, construct `pb.Diagnostic.WARNING`, append the rule ID to the summary, and map the single top-level attribute name to `pb.AttributePath.Step(attribute_name=...)`. A failed hook run returns exactly one generic compatibility warning. Never read `provider_context` for lint selection.
- [x] In `ValidateDataResourceConfigHandler`, append lint diagnostics only in the `else` branch after `validation_errors` is empty.
- [x] Rerun `uv run pytest tests/lint/test_runner.py tests/tfprotov6/handlers/test_provider_linting_data_source.py tests/data_sources/test_base_data_source.py -q`; expect all pass.
- [x] Run `uv run pytest tests/tfprotov6/handlers/test_validate_data_resource_config.py tests/tfprotov6/test_read_data_source_integration.py -q`; expect all pass.
- [x] Commit with message `feat: run provider lints on data source validation`.

Approved implementation commits: `3ee4a78a50c769c7e9a9da687d461aae84614fd9`, `8628d9e47e0666a8aad2a9379d0128e35cb55721`. Independent spec review: approved. Independent code-quality review: approved after hardening rendered-log secrecy, descriptor lookup isolation, and registry restoration. Fresh full-suite evidence: 2,439 passed, 3 skipped, 2 xfailed; lint and typecheck passed.

## Task 3: Seven base hooks and seven-handler contract

**Repository:** Pyvider

**Files:**

- Modify: `src/pyvider/providers/base.py`
- Modify: `src/pyvider/resources/base.py`
- Modify: `src/pyvider/data_sources/base.py`
- Modify: `src/pyvider/ephemerals/base.py`
- Modify: `src/pyvider/list_resources/base.py`
- Modify: `src/pyvider/actions/base.py`
- Modify: `src/pyvider/state_stores/base.py`
- Modify: `src/pyvider/protocols/tfprotov6/handlers/validate_provider_config.py`
- Modify: `src/pyvider/protocols/tfprotov6/handlers/validate_resource_config.py`
- Modify: `src/pyvider/protocols/tfprotov6/handlers/validate_data_resource_config.py`
- Modify: `src/pyvider/protocols/tfprotov6/handlers/validate_ephemeral_resource_config.py`
- Modify: `src/pyvider/protocols/tfprotov6/handlers/config_handlers.py`
- Modify: `src/pyvider/protocols/tfprotov6/handlers/action_handlers.py`
- Modify: `src/pyvider/protocols/tfprotov6/handlers/state_store_handlers.py`
- Create: `tests/lint/test_base_hooks.py`
- Create: `tests/tfprotov6/handlers/test_provider_linting_contract.py`

- [x] Parameterize a base-hook test across all seven base classes and assert the default async hook returns an empty tuple.
- [x] Cover `BaseProvider`, `BaseResource`, `BaseDataSource`, `BaseEphemeralResource`, `BaseListResource`, `BaseAction`, and `BaseStateStore` explicitly; functions remain out of scope.
- [x] Parameterize real handler contract cases for provider, managed resource, data source, ephemeral resource, list resource, action, and state store. Each case must prove decoded config reaches `lint`, disabled selection does not invoke it, semantic errors prevent invocation, exact rule/group selection works, exact exclusion works, emitted warning location is the named top-level attribute, and the path works with no `provider_context` registered.
- [x] Add explicit tests for duck-typed pre-lint components: `getattr(component, "lint", None)` missing means no findings, preserving backwards compatibility for decorated components that do not inherit a current base class.
- [x] Run `uv run pytest tests/lint/test_base_hooks.py tests/tfprotov6/handlers/test_provider_linting_contract.py -q` and observe failures for six missing hooks/integrations.
- [x] Add the identical supported hook to every base:

  ```python
  async def lint(self, ctx: LintContext[ConfigType]) -> Sequence[LintFinding]:
      """Return opt-in advisory findings for a semantically valid configuration."""
      return ()
  ```

  `BaseProvider` and `BaseStateStore` use `LintContext[Any]`; no existing `validate()` signature changes.
- [x] Refactor `_linting.py` to expose one `lint_diagnostics(component, config, *, kind, name, operation)` helper and call it from each handler only after its existing validation errors are known empty. Provider linting occurs after unmarshal plus `check_required_attributes`; list/action/state-store linting occurs after their own `validate()` returns no messages.
- [x] Preserve handler behavior for unknown types and exceptions. Do not move linting into plan/apply/read/open/invoke/configure handlers and do not add cross-phase deduplication.
- [x] Rerun `uv run pytest tests/lint/test_base_hooks.py tests/tfprotov6/handlers/test_provider_linting_contract.py -q`; expect all pass.
- [x] Run:

  ```shell
  uv run pytest \
    tests/tfprotov6/handlers/test_validate_provider_config.py \
    tests/tfprotov6/handlers/test_validate_resource_config.py \
    tests/tfprotov6/handlers/test_validate_data_resource_config.py \
    tests/tfprotov6/handlers/test_validate_ephemeral_resource_config.py \
    tests/actions/test_action_rpcs.py \
    tests/actions/test_config_generation_hooks.py \
    tests/state_stores/test_state_store_rpcs.py -q
  ```

  Expect all pass.
- [x] Run `we run test && we run lint && we run typecheck`; expect the Pyvider baseline plus new tests to pass.
- [x] Commit with message `feat: lint every configuration validation path`.

Approved implementation commits: `3b2e37c3b9f88085b8a05db4329d6600913bbb4e`, `291ca3d6cc47fbebba780e452a105c17a76f4007`, `9eacda77551d9e42f223a7ebbae3e9647d987584`. Independent spec review: approved. Independent code-quality review: approved after restoring nonfatal, secret-safe provider test-mode inspection. Fresh full-suite evidence: 2,461 passed, 3 skipped, 2 xfailed; 104 named handler regressions, lint, and typecheck passed.

## Task 4: Pyvider author documentation and public API contract

**Repository:** Pyvider

**Files:**

- Create: `docs/core-concepts/provider-linting.md`
- Modify: `mkdocs.yml`
- Modify: `src/pyvider/lint/__init__.py`
- Create: `tests/lint/test_public_api.py`
- Modify: `scripts/check_doc_links.py` only if the existing checker requires explicit allowlisting

- [x] Write an import-contract test for `from pyvider.lint import LintContext, LintFinding, LintSelector` and a documentation test that checks the page contains `async def lint`, `PYVIDER_LINT`, `[lint]`, validation/deprecation/warning distinctions, unknown-safe guidance, the compatibility bridge, and native protocol migration language.
- [x] Run `uv run pytest tests/lint/test_public_api.py -q` and observe the documentation assertion fail.
- [x] Write the page with this minimal author example:

  ```python
  async def lint(self, ctx: LintContext[HTTPAPIConfig]) -> Sequence[LintFinding]:
      rule = "example/acme:insecure-http"
      groups = ("example/acme:all", "example/acme:security")
      if not ctx.enabled(rule, *groups) or not ctx.config.url.startswith("http://"):
          return ()
      return (LintFinding(rule, groups, "Insecure HTTP endpoint",
              "Use HTTPS or suppress this rule when plaintext is intentional.", "url"),)
  ```

- [x] State that the author API is supported, OpenTofu's built-in linter retains OpenTofu's experimental status, and ordinary warning transport is a temporary compatibility adapter because tfprotov6 has no provider-lint message or selection hints.
- [x] Add the page to `mkdocs.yml` navigation and public exports to `pyvider.lint.__all__`.
- [x] Run `uv run pytest tests/lint/test_public_api.py -q && we run docs.build`; expect pass.
- [x] Run `we run test && we run lint && we run typecheck`; expect pass.
- [x] Commit with message `docs: document provider-native linting`.

Approved implementation commits: `b6ee5ebad872e0bb62ae6929c928f41c0fe1aa86`, `07662126511ca2781d787543ec924cbfd5e973ef`. Independent spec review: approved. Independent code-quality review: approved after replacing source-string navigation matching with semantic YAML parsing. Fresh full-suite evidence: 2,477 passed, 3 skipped, 2 xfailed; 16 focused tests, docs build, 451-link check, lint, and typecheck passed.

## Task 5: Four security rules in first-party components

**Repository:** pyvider-components

**Files:**

- Modify: `src/pyvider/components/provider.py`
- Modify: `src/pyvider/components/resources/local_directory.py`
- Modify: `src/pyvider/components/data_sources/http_api.py`
- Modify: `src/pyvider/components/list_resources/file_contents.py`
- Create: `src/pyvider/components/lint_rules.py`
- Create: `tests/test_provider_lint_rules_security.py`

- [x] Define the exact test prefix `uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting` for every command in Tasks 5–7; do not commit an absolute path or alter `uv.lock`. Before the first red test, run `uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting python -c 'import pyvider; print(pyvider.__file__)'` and require the printed path to begin with `/Users/tim/.config/superpowers/worktrees/pyvider/provider-linting/`.
- [x] Add table-driven tests for provider `api_insecure_skip_verify is True`, local-directory POSIX other-write bit, HTTP URL beginning `http://`, and file-content `include_hidden is True`. For each rule assert trigger, nearby safe value, omitted value, unknown/`None`, exact selection, security group selection, exact exclusion from `provide-io/pyvider:all`, summary, remediation detail, groups, and attribute path.
- [x] Use these immutable constants:

  ```python
  ALL = "provide-io/pyvider:all"
  SECURITY = "provide-io/pyvider:security"
  INSECURE_TLS = "provide-io/pyvider:insecure-tls"
  WORLD_WRITABLE_DIRECTORY = "provide-io/pyvider:world-writable-directory"
  INSECURE_HTTP = "provide-io/pyvider:insecure-http"
  INCLUDE_HIDDEN_FILES = "provide-io/pyvider:include-hidden-files"
  ```

- [x] Run `uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting pytest tests/test_provider_lint_rules_security.py -q` and observe missing `lint()` findings.
- [x] Implement pure hooks. Guard each calculation with `ctx.enabled(rule, ALL, SECURITY)`. Use `permissions is not None and int(permissions, 8) & 0o002`, case-insensitive URL scheme comparison, and identity comparison for booleans. Do no filesystem or network I/O.
- [x] Ensure every detail says why the choice may be intentional, names the safer setting, and gives exact suppression syntax `!<rule-id>`.
- [x] Rerun `uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting pytest tests/test_provider_lint_rules_security.py -q`, then run the same prefixed command with `pytest -q`; expect all component tests pass.
- [x] Run `uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting ruff check src tests && uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting mypy src`; expect pass.
- [x] Commit with message `feat: add first-party security lint rules`.

Approved component commit: `05c84b1d83b2c3e0dcbd6e877260a21090d55c16`. Independent spec and code-quality reviews: approved. Fresh evidence against the reviewed Pyvider source: 4 focused and 357 full-suite tests passed; Ruff and mypy passed. Because uv's shared namespace initializer preceded the editable root, commands also set `PYTHONPATH=/Users/tim/.config/superpowers/worktrees/pyvider/provider-linting/src`; `pyvider.lint.__file__` verified the reviewed checkout.

## Task 6: Three reliability rules in first-party components

**Repository:** pyvider-components

**Files:**

- Modify: `src/pyvider/components/ephemerals/lease.py`
- Modify: `src/pyvider/components/actions/wait_for_file.py`
- Modify: `src/pyvider/components/state_stores/filesystem_store.py`
- Modify: `src/pyvider/components/lint_rules.py`
- Create: `tests/test_provider_lint_rules_reliability.py`

- [x] Add table-driven tests for lease `ttl_seconds > 3600`, action `timeout_seconds > 300`, and filesystem-store relative `path`. Cover thresholds 3600/3601 and 300/301, absolute and relative paths, omitted/unknown values, exact and reliability-group selection, exact exclusion, and metadata.
- [x] Run `uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting pytest tests/test_provider_lint_rules_reliability.py -q` and observe missing findings.
- [x] Add constants `RELIABILITY`, `LONG_LIVED_LEASE`, `LONG_ACTION_TIMEOUT`, and `RELATIVE_STATE_STORE_PATH`, and implement pure hooks guarded by `ctx.enabled(rule, ALL, RELIABILITY)`. Determine relativity with `Path(str(value)).expanduser().is_absolute()` without touching the path.
- [x] Rerun `uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting pytest tests/test_provider_lint_rules_reliability.py -q`, then run the same prefixed command with `pytest -q`; expect all pass.
- [x] Run `uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting ruff check src tests && uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting mypy src`; expect pass.
- [x] Commit with message `feat: add first-party reliability lint rules`.

Approved component commit: `a43ae40cb97767bc5080d313c044aa3b9bc97fdf`. Independent spec and code-quality reviews: approved. Fresh evidence against reviewed Pyvider: 35 focused and 392 full-suite tests passed; Ruff and mypy passed.

## Task 7: Component rule documentation and generated provider docs

**Repository:** pyvider-components

**Files:**

- Create: `docs/guides/provider-linting.md`
- Modify: `mkdocs.yml`
- Modify: `src/pyvider/components/provider.plating/docs/pyvider.tmpl.md`
- Modify: `src/pyvider/components/resources/local_directory.plating/docs/pyvider_local_directory.tmpl.md`
- Modify: `src/pyvider/components/data_sources/http_api.plating/docs/pyvider_http_api.tmpl.md`
- Modify: `src/pyvider/components/ephemerals/lease.plating/docs/pyvider_lease.tmpl.md`
- Modify: `src/pyvider/components/list_resources/file_contents.plating/docs/pyvider_file_content.tmpl.md`
- Modify: `src/pyvider/components/actions/wait_for_file.plating/docs/pyvider_wait_for_file.tmpl.md`
- Modify: `src/pyvider/components/state_stores/filesystem_store.plating/docs/pyvider_filesystem_store.tmpl.md`
- Modify: `README.md`
- Create: `tests/test_lint_rule_documentation.py`

- [x] Add a test that extracts every rule constant and asserts the guide and matching component template contain its ID, trigger attribute, group, remediation, and exact suppression command.
- [x] Run `uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting pytest tests/test_lint_rule_documentation.py -q` and observe missing documentation failures.
- [x] Document all seven rules, provider `[lint]` configuration, environment override and explicit empty disablement. Keep action/list/state-store reachability claims separate from OpenTofu core.
- [x] Rebuild generated flavor/plating helpers using the repository's current Plating path: `uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting plating plate --output-dir docs`; inspect and retain only intended generated documentation changes.
- [x] Run `uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting pytest tests/test_lint_rule_documentation.py -q && uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting mkdocs build --strict`; expect pass.
- [x] Run `uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting pytest -q && uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting ruff check src tests && uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting mypy src`; expect pass.
- [x] Commit with message `docs: catalog first-party lint rules`.

Approved component commits: `db6f2fa9705d61d1b566f98e23a84fd3b9c830a6`, `b6f59c9c7f54ceed97d718bb145230144410665a`, `489082a9ea20641a50a72026f038f32dda4f72f1`. Independent spec review: approved. Independent code-quality review: approved after adding a tested two-pass generation wrapper, complete derived-output ignores, accurate case-insensitive/reachability language, and sibling-navigation restoration. Fresh evidence: 31 focused and 423 full-suite tests passed; all seven generated target pages inspected; strict MkDocs, Ruff, and mypy passed.

## Task 8: Reproducible coordinated packaged build and seven-RPC proof

**Repository:** terraform-provider-pyvider

**Files:**

- Create: `ci/build-provider-linting-stack.py`
- Create: `ci/run-provider-linting-rpcs.py`
- Create: `tests/conformance/test_provider_linting.py`
- Modify: `tests/conformance/conftest.py`
- Create: `tests/test_linting_stack_build.py`
- Modify: `Makefile`

- [ ] Add one build-script unit test at a time and run each red before implementing it. Prove the script rejects missing/non-Git/dirty source repositories; resolves `git rev-parse HEAD`; materializes each clean revision with `git archive <sha>` into an isolated temporary build context; injects local `[tool.uv.sources]` and `[tool.flavor.build].dependencies` only in that context; runs `uv lock`, `flavor pack`, and `flavor inspect --json --provenance`; writes `dist/provider-linting-build-provenance.json`; copies only the PSP/versioned binary/provenance out; and leaves the checkout's `pyproject.toml`/`uv.lock` byte-identical.
- [ ] Run `uv run pytest tests/test_linting_stack_build.py -q` and observe the script import failure.
- [ ] Implement the build script with `tempfile.TemporaryDirectory`, `git archive` piped into `tar -x -C`, `tomllib` plus `tomli-w`, and `subprocess.run(check=True)`. The temporary project must contain `_stack/pyvider` and `_stack/pyvider-components` materialized from the recorded clean SHAs; local source requirements are stripped from exported lock data by Flavorpack while `[tool.flavor.build].dependencies` supplies their wheels. The provenance JSON must include schema version, provider-repository HEAD, Pyvider SHA, components SHA, archive SHA256 values, exact build commands, Flavorpack inspection output, PSP SHA256, binary SHA256, platform, and UTC timestamp.
- [ ] Add `make build-linting-stack PYVIDER_SOURCE=/Users/tim/.config/superpowers/worktrees/pyvider/provider-linting COMPONENTS_SOURCE=/Users/tim/.config/superpowers/worktrees/pyvider-components/provider-linting` and refuse absent variables. The target must produce `dist/terraform-provider-pyvider.psp` and the current platform's versioned binary.
- [ ] Write direct packaged-provider tests that spawn a new provider process with `child_env({"PYVIDER_LINT": selector})`, call all seven Validate RPCs with triggering configs, and assert exact severity, rule ID summary, detail, and top-level attribute step. Include default-off, exact, group, `all`, namespaced `all`, exclusion, empty override, and fail-open cases. Add each selector/RPC expectation as its own parameterized case; run the new case red, implement the minimum fixture/driver behavior, then rerun green before adding the next case.
- [ ] Add provenance assertions that the launched executable is the exact path named in `PYVIDER_CONFORMANCE_PSP`, its SHA256 equals both build provenance and the freshly computed value, the provenance SHAs equal `git rev-parse HEAD` in the two reviewed clean source worktrees, and `flavor inspect --json --provenance` contains the locally built `pyvider` and `pyvider-components` distributions. The test must not import component classes to generate configs; build dynamic values from schemas returned by the packaged process.
- [ ] Run the test before the coordinated build and observe the expected missing/outdated-package failure.
- [ ] Add this exact no-rebuild Make target and a Make dry-run test proving its output contains neither `flavor pack` nor a `build` prerequisite:

  ```make
  PYVIDER_CONFORMANCE_TESTS ?= tests/conformance

  .PHONY: test-conformance-binary
  test-conformance-binary:
	@test -n "$(PYVIDER_CONFORMANCE_PSP)" || (echo "PYVIDER_CONFORMANCE_PSP is required" >&2; exit 2)
	@test -f "$(PYVIDER_CONFORMANCE_PSP)" || (echo "missing provider binary: $(PYVIDER_CONFORMANCE_PSP)" >&2; exit 2)
	@$(MAKE) clean-workenv
	@ci/warm-workenv.sh "$(PYVIDER_CONFORMANCE_PSP)"
	@PYVIDER_CONFORMANCE_REQUIRED=1 PYVIDER_CONFORMANCE_PSP="$(PYVIDER_CONFORMANCE_PSP)" uv run pytest $(PYVIDER_CONFORMANCE_TESTS) -q
  ```

- [ ] Run:

  ```shell
  make build-linting-stack \
    PYVIDER_SOURCE=/Users/tim/.config/superpowers/worktrees/pyvider/provider-linting \
    COMPONENTS_SOURCE=/Users/tim/.config/superpowers/worktrees/pyvider-components/provider-linting
  make test-conformance-binary \
    PYVIDER_CONFORMANCE_PSP="$PWD/dist/$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')/terraform-provider-pyvider_v$(cat VERSION)" \
    PYVIDER_CONFORMANCE_TESTS=tests/conformance/test_provider_linting.py
  ```

  Expect all seven RPC cases pass against the rebuilt binary.
- [ ] Run `lint_binary="$PWD/dist/$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')/terraform-provider-pyvider_v$(cat VERSION)"` followed by `make test-conformance-binary PYVIDER_CONFORMANCE_PSP="$lint_binary"`; expect the existing 87-test packaged suite plus the new lint suite pass against that same explicit checksum. Never use `make test-conformance` for coordinated-stack verification because it rebuilds the binary from the ordinary lock.
- [ ] Commit with message `test: prove seven lint paths in packaged provider`.

## Task 9: OpenTofu v1.13.0-beta1 four-path E2E

**Repository:** terraform-provider-pyvider

**Files:**

- Create: `ci/install-opentofu-beta.sh`
- Create: `tests/e2e/provider-linting/main.tf`
- Create: `tests/e2e/provider-linting/pyvider.toml`
- Create: `tests/e2e/test_provider_linting_opentofu.py`
- Create: `tests/test_install_opentofu_beta.py`
- Modify: `Makefile`

- [ ] Test the installer against a local fake release directory: it must select v1.13.0-beta1 for the host OS/architecture, verify the matching line from `tofu_1.13.0-beta1_SHA256SUMS`, reject checksum mismatch, and print the installed binary path.
- [ ] Run `uv run pytest tests/test_install_opentofu_beta.py -q` and observe the missing script failure.
- [ ] Implement the pinned installer using `curl --fail --location`, the official release archive and SHA256SUMS, `shasum -a 256 -c`, and an explicit cache directory. Never accept `latest`.
- [ ] Create one valid HCL fixture containing the triggering provider, managed resource, data source, and ephemeral resource configurations. Use only local paths and a non-contacted `http://127.0.0.1` URL; `validate` must not perform the data-source read.
- [ ] Add E2E tests that install the packaged binary into a temporary filesystem mirror, run `tofu init`, and parse `tofu validate -json` for: default-off; `[lint].rules`; `PYVIDER_LINT=provide-io/pyvider:all`; environment overriding file; explicit empty environment disabling file; security group; exact rule; and exact exclusion.
- [ ] Assert the four expected IDs and attribute ranges/expressions in JSON. Assert action/list/state-store IDs are absent and document that as the current core boundary, not a skip that claims coverage.
- [ ] Run the E2E test with `PYVIDER_CONFORMANCE_PSP` unset and observe the expected explicit-package failure. Add a `test-linting-opentofu-binary` target that requires the same explicit `PYVIDER_CONFORMANCE_PSP` and provenance file from Task 8 and has no build prerequisite. Then run:

  ```shell
  lint_binary="$PWD/dist/$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')/terraform-provider-pyvider_v$(cat VERSION)"
  make test-linting-opentofu-binary PYVIDER_CONFORMANCE_PSP="$lint_binary"
  ```

  Expect all OpenTofu JSON assertions pass and `tofu version` contain `v1.13.0-beta1`; assert the binary checksum still equals `provider-linting-build-provenance.json` before and after the run.
- [ ] Commit with message `test: prove provider lints through OpenTofu beta`.

## Task 10: Checked cast, proof manifest, and CI artifact

**Repository:** terraform-provider-pyvider

**Files:**

- Create: `ci/provider-linting-demo.sh`
- Create: `ci/generate-provider-linting-proof.py`
- Create: `ci/verify-provider-linting-proof.py`
- Create: `ci/record-provider-linting.sh`
- Modify: `ci/record-to-cast.py`
- Modify: `ci/retime-cast.py`
- Create: `tests/proof/test_provider_linting_proof.py`
- Modify: `.github/workflows/build-provider.yml`
- Create generated: `provider-linting.cast`
- Create generated: `provider-linting-proof.json`

- [ ] Add proof-verifier tests for valid fixture, missing command, missing rule, ANSI stripping, cast checksum mismatch, provider checksum mismatch, unknown observation channel, absolute user path leakage, token-like key leakage, and non-beta Tofu version.
- [ ] Run `uv run pytest tests/proof/test_provider_linting_proof.py -q` and observe missing verifier/generator failures.
- [ ] Define manifest schema version 1 with keys `generated_at`, `ci`, `components`, `opentofu`, `provider_binary`, `commands`, `rules`, and `cast`. Each rule object has `id`, `kind`, and an `observed_via` list: provider/resource/data-source/ephemeral use `["opentofu", "tofusoup"]`; list/action/state-store use `["tofusoup"]`.
- [ ] Make `provider-linting-demo.sh` execute and visibly echo these real commands:

  ```shell
  tofu version
  tofu validate
  PYVIDER_LINT=provide-io/pyvider:all tofu validate -lint=all
  PYVIDER_LINT='provide-io/pyvider:all,!provide-io/pyvider:insecure-http' tofu validate
  soup stir provider-linting
  uv run python ci/run-provider-linting-rpcs.py --binary "$PYVIDER_CONFORMANCE_PSP" --selector provide-io/pyvider:all --format json-lines
  ```

  The `soup stir` line is retained as a real lifecycle demonstration. The explicit final command is the honest TofuSoup direct-driver proof for all seven RPCs and must visibly emit one deterministic JSON line per rule containing `rule_id`, `kind`, `severity`, `attribute`, `observed_via`, and `provider_sha256`; never relabel `soup stir` as reaching action/list/state-store validation.
- [ ] Reuse `record-to-cast.py` and `retime-cast.py` through `record-provider-linting.sh`; parameterize title/size only as needed without breaking `record-conformance.sh`.
- [ ] Generate the manifest only after every command exits zero. Record the provider source SHA, exact clean Pyvider/components Git SHAs and archive hashes from `provider-linting-build-provenance.json`, versions, official Tofu archive checksum, the one explicit packaged-binary path's checksum, command list, seven rules/kinds/channel lists, cast checksum, GitHub run identity when present, and UTC timestamp. Reject secrets and machine-local paths. Before and after recording, recompute the binary checksum and require it to match build provenance.
- [ ] Parse the complete cast, strip terminal controls, and assert all six commands, the seven JSON-line observations and rule IDs, default-off evidence, exact-exclusion evidence, OpenTofu four-path statement, and TofuSoup seven-path pass summary.
- [ ] Extend the existing default-branch `.github/workflows/build-provider.yml` `workflow_dispatch` inputs with `provider_linting_proof` (boolean, default false), `pyvider_ref`, and `components_ref`. Add one conditional Linux proof job that checks out those public repositories at exact refs under `.stack/`, uses `ci/build-provider-linting-stack.py`, captures the one explicit binary path/checksum, installs v1.13.0-beta1, drives that same binary through `test-conformance-binary` and `test-linting-opentofu-binary`, records/verifies proof, and uploads one artifact named `provider-linting-proof` containing the cast, manifest, and build provenance. Use pinned action SHAs. This workflow already exists on the default branch, so it can be dispatched with `--ref codex/provider-linting`; do not create a new workflow file that GitHub cannot dispatch before merge.
- [ ] Run locally:

  ```shell
  lint_binary="$PWD/dist/$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')/terraform-provider-pyvider_v$(cat VERSION)"
  PYVIDER_CONFORMANCE_PSP="$lint_binary" ci/record-provider-linting.sh
  uv run python ci/verify-provider-linting-proof.py provider-linting-proof.json provider-linting.cast
  uv run pytest tests/proof/test_provider_linting_proof.py -q
  ```

  Expect all checks pass.
- [ ] Commit with message `ci: publish checked provider linting proof`.
- [ ] Do not push or dispatch yet. Task 11 must land the provider documentation first so the later CI run is tied to the final reviewed provider source revision rather than a stale intermediate commit.

## Task 11: Actual-provider reproduction documentation

**Repository:** terraform-provider-pyvider

**Files:**

- Create: `docs/guides/provider-linting-proof.md`
- Modify: `mkdocs.yml`
- Modify: `README.md`
- Create: `tests/proof/test_provider_linting_docs.py`

- [ ] Add a docs test asserting the guide names both exact fixtures, both artifacts, v1.13.0-beta1, the four-vs-seven capability boundary, all reproduction targets, and these exact upstream links: `https://github.com/opentofu/opentofu/blob/main/rfc/20260406-linting.md`, `https://github.com/opentofu/opentofu/issues/4310`, `https://github.com/opentofu/opentofu/pull/4337`, and `https://github.com/opentofu/opentofu/releases/tag/v1.13.0-beta1`.
- [ ] Run `uv run pytest tests/proof/test_provider_linting_docs.py -q` and observe missing documentation failure.
- [ ] Document local coordinated build, OpenTofu JSON suite, TofuSoup direct suite, cast generation, manifest verification, and CI artifact retrieval. Say Pyvider's API is supported; say OpenTofu calls its built-in feature experimental; say ordinary warnings are the temporary compatibility bridge.
- [ ] Run `uv run pytest tests/proof/test_provider_linting_docs.py -q && uv run mkdocs build --strict`; expect pass.
- [ ] Reuse `lint_binary` from Task 8 and run `make test-conformance-binary PYVIDER_CONFORMANCE_PSP="$lint_binary"`, `make test-linting-opentofu-binary PYVIDER_CONFORMANCE_PSP="$lint_binary"`, and `uv run pytest tests/proof -q`; expect pass without any `flavor pack` rebuild.
- [ ] Commit with message `docs: explain packaged linting proof`.
- [ ] Push the reviewed Pyvider and components feature branches to `gh-origin`, capture their exact public commit SHAs with `git rev-parse HEAD`, then push the provider feature branch to `gh-origin`. Set `provider_sha` to the just-pushed provider HEAD and `dispatch_after` to the current UTC timestamp. Dispatch the already-default-branch workflow exactly with:

  ```shell
  gh workflow run build-provider.yml \
    --repo provide-io/terraform-provider-pyvider \
    --ref codex/provider-linting \
    -f provider_linting_proof=true \
    -f pyvider_ref="$pyvider_sha" \
    -f components_ref="$components_sha"
  ```

- [ ] Retrieve runs with `gh run list --repo provide-io/terraform-provider-pyvider --workflow build-provider.yml --branch codex/provider-linting --event workflow_dispatch --commit "$provider_sha" --json databaseId,createdAt,headSha,status,conclusion`, filter to entries created at or after `dispatch_after`, and require exactly one match before assigning its numeric `databaseId` to `proof_run_id`. Run `gh run watch "$proof_run_id" --repo provide-io/terraform-provider-pyvider --exit-status`; require green.
- [ ] Set `proof_dir=$(mktemp -d /tmp/pyvider-linting-proof.XXXXXX)`, download only that run with `gh run download "$proof_run_id" --repo provide-io/terraform-provider-pyvider --name provider-linting-proof --dir "$proof_dir"`, rerun the verifier, and assert the manifest's provider source SHA equals `provider_sha`, its Pyvider/components SHAs equal the two dispatched refs, and the binary checksum equals the checked build provenance.
- [ ] Replace `provider-linting.cast` and `provider-linting-proof.json` with the verified files from that exact run and commit only those two files as `chore: record final provider linting proof`. Because a tracked manifest cannot contain the hash of the commit that contains itself, enforce the non-self-referential invariant: the manifest's provider source SHA must equal this artifact-only commit's first parent, and `git diff --name-only HEAD^ HEAD` must list only those two artifacts. Record both the provider source SHA and artifact commit SHA for the site.

## Task 12: Verified website proof synchronization

**Repository:** site-pyvider-com

**Files:**

- Create: `scripts/sync-provider-linting-proof.py`
- Create: `scripts/verify-provider-linting-proof.py`
- Create: `tests/test_provider_linting_proof.py`
- Create from verified CI artifact: `static/casts/provider-linting.cast`
- Create from verified CI artifact: `static/proofs/provider-linting-proof.json`

- [ ] Add stdlib `unittest` tests using a local fake `gh run download` result. Prove the sync requires repository `provide-io/terraform-provider-pyvider`, an explicit numeric run ID, artifact name `provider-linting-proof`, successful manifest validation, matching cast checksum, matching seven-rule catalog, and no destination changes on any failure.
- [ ] Run `python3 -m unittest tests/test_provider_linting_proof.py -v` and observe missing script failures.
- [ ] Implement the shared verifier without third-party dependencies. Implement sync as download-to-temporary-directory → verify → copy both current destination files into a rollback directory → `os.replace` both verified temporary files → on any exception restore both originals (or remove both new files when no originals existed) before re-raising. Add an injected second-`os.replace` failure test and assert both destination bytes are unchanged. Never accept “latest successful run.”
- [ ] Rerun `python3 -m unittest tests/test_provider_linting_proof.py -v`; expect pass.
- [ ] Run `python3 scripts/sync-provider-linting-proof.py --repository provide-io/terraform-provider-pyvider --run-id "$proof_run_id" --artifact provider-linting-proof --expected-provider-sha "$provider_sha"` against the exact green provider workflow run ID from Task 11. The script must assert the manifest provider source SHA equals `provider_sha`, then run:

  ```shell
  python3 scripts/verify-provider-linting-proof.py \
    static/proofs/provider-linting-proof.json \
    static/casts/provider-linting.cast
  ```

  Expect a zero exit and all seven IDs reported.
- [ ] Commit with message `build: sync verified provider linting proof`.

## Task 13: Evergreen linting page and homepage entry point

**Repository:** site-pyvider-com

**Files:**

- Create: `content/linting.md`
- Modify: `layouts/index.html`
- Create: `layouts/partials/linting.html`
- Modify: `layouts/partials/nav.html`
- Modify: `static/css/site.css`
- Create: `scripts/check-linting-site.py`
- Create: `tests/test_linting_site.py`

- [ ] Add source/render tests requiring all seven IDs, enable/exclude/disable commands, `[lint]` example, the four exact OpenTofu URLs listed in Task 11, exact provider fixture and proof-manifest links, OpenTofu-vs-TofuSoup matrix, supported API language, OpenTofu experimental language, compatibility-bridge language, and shortcode target `provider-linting.cast`.
- [ ] Run `python3 -m unittest tests/test_linting_site.py -v` and observe missing-page failures.
- [ ] Build `/linting/` as an evergreen page using the existing cast shortcode:

  ```go-html-template
  {{< cast id="provider-linting" file="provider-linting.cast"
      title="$ tofu validate -lint=all · provider rules · seven RPC proof"
      rows="34" speed="1.5" idleTimeLimit="3" >}}
  ```

- [ ] Include copyable commands for enable, group selection, exact exclusion, `PYVIDER_LINT=''`, and persistent TOML. Include the seven-rule table and explicitly state OpenTofu reaches provider/resource/data-source/ephemeral validation while TofuSoup directly proves all seven against the same package.
- [ ] Add a concise homepage section/link and navigation link; use existing visual tokens rather than a separate design system.
- [ ] Implement `scripts/check-linting-site.py PUBLIC_DIR` to parse rendered HTML and static assets, not Markdown alone.
- [ ] Run:

  ```shell
  site_out=$(mktemp -d /tmp/pyvider-linting-site.XXXXXX)
  hugo --environment production --minify --destination "$site_out"
  python3 scripts/check-linting-site.py "$site_out"
  python3 -m unittest discover -s tests -v
  ```

  Expect the production build and all rendered checks to pass.
- [ ] Commit with message `feat: publish provider linting proof page`.

## Task 14: Final four-repository verification and independent review

**Repositories:** all four

**Files:** No planned production edits; fixes discovered by review belong in their owning repository and receive focused regression tests.

- [ ] Dispatch one fresh final reviewer with the approved design, this plan, all four worktree paths, and all commit ranges. Require requirement-by-requirement verification of public API, seven hooks/handlers, seven rules, configuration precedence, packaged provenance, OpenTofu four-path evidence, TofuSoup seven-path evidence, recording/manifest integrity, docs language, and production-deployment exclusion.
- [ ] Resolve every final-review finding via the original owning-task implementer when practical; rerun focused tests and repeat final review until approved.
- [ ] Run Pyvider verification:

  ```shell
  we run test
  we run lint
  we run typecheck
  we run docs.build
  ```

- [ ] Run components verification after rebuilding generated Plating output:

  ```shell
  uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting plating plate --output-dir docs
  uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting pytest -q
  uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting ruff check src tests
  uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting mypy src
  uv run --with-editable /Users/tim/.config/superpowers/worktrees/pyvider/provider-linting mkdocs build --strict
  ```

- [ ] Rebuild the actual provider from the final reviewed SHAs, then run:

  ```shell
  make build-linting-stack \
    PYVIDER_SOURCE=/Users/tim/.config/superpowers/worktrees/pyvider/provider-linting \
    COMPONENTS_SOURCE=/Users/tim/.config/superpowers/worktrees/pyvider-components/provider-linting
  lint_binary="$PWD/dist/$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')/terraform-provider-pyvider_v$(cat VERSION)"
  make test-conformance-binary PYVIDER_CONFORMANCE_PSP="$lint_binary"
  make test-linting-opentofu-binary PYVIDER_CONFORMANCE_PSP="$lint_binary"
  uv run pytest tests/proof -q
  uv run python ci/verify-provider-linting-proof.py provider-linting-proof.json provider-linting.cast
  uv run mkdocs build --strict
  ```

- [ ] If final review changes Pyvider or components, push the new reviewed SHAs. If it changes provider source/docs, commit those changes. Dispatch `build-provider.yml` again exactly as in Task 11, require a unique green numeric run ID for the final provider source SHA, update the provider's two checked proof artifacts in one artifact-only commit, and enforce the parent-SHA/two-file invariant again.
- [ ] Resync the site from that final green numeric CI run (never the earlier run), assert the manifest provider source/Pyvider/components SHAs match the final reviewed code commits, then run proof verification, all site unit tests, Hugo production build, and rendered checker.
- [ ] Confirm `git status --short` in every worktree contains only intended tracked changes or is clean after commits; inspect `git diff main...HEAD --check` in all four repositories.
- [ ] Confirm `/Users/tim/code/tf/opentofu` is unmodified and no command or workflow targets the production `pyvider.com` branch/deployment.

## Task 15: Cloudflare Pages feature-preview deployment and live smoke proof

**Repository:** site-pyvider-com

**Files:**

- Create: `scripts/smoke-linting-preview.py`
- Create: `scripts/check-pages-preview-target.py`
- Create: `tests/test_linting_preview_smoke.py`
- Create: `docs/deployment.md`

- [ ] Add HTTP smoke-check tests against a local server fixture. Require status 200 for `/linting/`, `/casts/provider-linting.cast`, and `/proofs/provider-linting-proof.json`; all seven IDs; enable/exclude/disable commands; four upstream URLs; and the cast player target. In the same test file, test `check-pages-preview-target.py` with fixture JSON for exactly one `pyvider-one` project, missing/duplicate project rejection, empty Git branch rejection, production-branch rejection, and distinct feature-branch acceptance.
- [ ] Run `python3 -m unittest tests/test_linting_preview_smoke.py -v` and observe missing smoke script failures.
- [ ] Implement the smoke checker with stdlib `urllib`, a required base preview URL, explicit timeouts, no redirect to `https://pyvider.com`, and clear assertion output. Implement the Pages target checker with stdlib `json`; it prints the selected production branch only after all assertions pass.
- [ ] Run site unit/render verification again and commit with message `test: verify linting staging preview`.
- [ ] Push the site feature branch to `origin` for provenance. Query the real Pages configuration immediately before deployment, save it, and pass it with the actual Git branch to the tested gate. Build the exact directory to be deployed, run the rendered checker against that same directory, and deploy only after the gate exits zero:

  ```shell
  site_branch=$(git branch --show-current)
  pages_json=$(mktemp /tmp/pyvider-pages-projects.XXXXXX.json)
  npx wrangler pages project list --json > "$pages_json"
  python3 scripts/check-pages-preview-target.py "$pages_json" pyvider-one "$site_branch"
  deploy_dir=$(mktemp -d /tmp/pyvider-linting-deploy.XXXXXX)
  hugo --environment production --minify --destination "$deploy_dir"
  python3 scripts/check-linting-site.py "$deploy_dir"
  npx wrangler pages deploy "$deploy_dir" \
    --project-name pyvider-one \
    --branch "$site_branch" \
    --commit-dirty=true
  ```

  Do not assume `main` is production: the preceding JSON assertion is the deployment gate. Do not invoke a production deployment and do not change the production custom domain.
- [ ] Capture the exact `*.pages.dev` feature-preview URL from Wrangler, then run `python3 scripts/smoke-linting-preview.py "$PREVIEW_URL"`; expect every URL and rendered-content assertion to pass with fresh HTTP 200 evidence.
- [ ] Open the preview for human inspection, report the preview URL, final four repository SHAs, CI proof run ID, Tofu checksum, provider checksum, cast checksum, test totals, and smoke results.
- [ ] Use `superpowers:finishing-a-development-branch` to present integration choices without merging, opening PRs, deleting worktrees, or deploying production unless the user selects that action.

## Completion audit

Before marking the goal complete, the primary agent must map every completion criterion in `docs/superpowers/specs/2026-09-13-provider-linting-design.md` to fresh evidence from Task 14 or 15. A successful unit suite is not evidence for packaged provenance, a local Hugo build is not evidence for deployed HTTP status, and `soup stir` is not evidence for RPCs OpenTofu core does not call. Completion requires the final reviewer approval, final CI artifact verification, and live preview smoke output together.
