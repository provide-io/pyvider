# Contributing to pyvider

Thanks for contributing to pyvider — the Python-native Terraform provider framework. This guide covers day-to-day development, quality gates, and PR expectations.

See `CLAUDE.md` for the detailed architectural rules that govern code review.

## Prerequisites

- Python 3.11+
- `uv` (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Terraform 1.5+ or OpenTofu 1.6+ (for end-to-end provider testing)

## Development Setup

```bash
git clone https://github.com/provide-io/pyvider
cd pyvider
uv sync
```

## Quality Gates

Before opening a PR:

```bash
make quality         # ruff lint + format, mypy strict, pytest with coverage gate
make test            # unit + integration
```

Requirements:

- **100% branch coverage** on `src/pyvider/**` (enforced).
- **mypy strict mode**. No `type: ignore` without an inline justification.
- **ruff** lint + format must pass.
- Files ≤ 500 lines.
- SPDX headers on every source/config file (`Apache-2.0`).

## Commits

- Conventional prefixes: `feat(hub): …`, `fix(schema): …`, `refactor(tfprotov6): …`, `test(resources): …`, `docs: …`, `chore: …`.
- Subject ≤ 72 chars.
- Do not mention AI assistance. No `Co-Authored-By:` trailers.
- Canonical email: `code@tim.life` or `code@provide.io`.

## Pull Requests

1. Run `make quality` (must pass).
1. For protocol / schema changes, run the tfprotov6 integration tests explicitly.
1. PR description notes any breaking schema or resource-API changes.
