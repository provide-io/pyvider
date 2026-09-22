#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Contracts for release artifact and registry verification."""

import json
from pathlib import Path
import re

import pytest
import yaml

ROOT = Path(__file__).parents[2]


def load_workflow() -> dict[str, object]:
    return yaml.safe_load((ROOT / ".github/workflows/release.yml").read_text())


def needs(job: dict[str, object]) -> set[str]:
    value = job.get("needs", [])
    return {value} if isinstance(value, str) else set(value)


def sparse_checkout_for(job_name: str) -> str:
    job = load_workflow()["jobs"][job_name]
    checkout = next(step for step in job["steps"] if step.get("uses", "").startswith("actions/checkout@"))
    return str(checkout.get("with", {}).get("sparse-checkout", ""))


def run_commands_for(job_name: str) -> str:
    job = load_workflow()["jobs"][job_name]
    return "\n".join(str(step.get("run", "")) for step in job["steps"])


def test_provider_linting_is_prepared_as_0_8_0() -> None:
    assert (ROOT / "VERSION").read_text(encoding="utf-8") == "0.8.0\n"

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(r"(?ms)^## \[0\.8\.0\] - 2026-09-21\n(?P<section>.*?)(?=^## |\Z)", changelog)
    assert match is not None
    section = match.group("section")
    normalized_section = " ".join(section.split())

    required = (
        "`LintFinding`",
        "`LintSelector`",
        "`LintContext`",
        "provider, resource, data source, ephemeral resource, list resource, action, and state store",
        "`PYVIDER_LINT`",
        "compatibility",
        "OpenTofu",
    )
    assert all(value in normalized_section for value in required)

    normalized_lower = normalized_section.lower()
    assert "[lint].rules" in normalized_section
    assert "default-off" in normalized_lower or "default off" in normalized_lower
    assert "exclusions" in normalized_lower
    assert "explicitly empty" in normalized_lower and "disables" in normalized_lower
    assert "fail-open" in normalized_lower
    assert "attribute-targeted" in normalized_lower


def test_release_dag_verifies_each_published_artifact() -> None:
    jobs = load_workflow()["jobs"]
    assert needs(jobs["verify-wheel"]) == {"release"}
    assert needs(jobs["publish-testpypi"]) == {"verify-wheel"}
    assert needs(jobs["verify-testpypi"]) == {"publish-testpypi"}
    assert needs(jobs["publish-pypi"]) == {"verify-testpypi"}
    assert needs(jobs["verify-pypi"]) == {"publish-pypi"}
    assert needs(jobs["sign-and-upload"]) == {"verify-pypi", "sbom"}


def test_wheel_verification_runs_for_release_and_dry_run_in_isolation() -> None:
    job = load_workflow()["jobs"]["verify-wheel"]
    condition = str(job["if"])
    commands = run_commands_for("verify-wheel")

    assert "github.event_name == 'release'" in condition
    assert "github.event_name == 'workflow_dispatch'" in condition
    assert "inputs.release_tag == ''" in condition
    assert "cp scripts/verify_lint_release.py" in commands
    assert "pip install" in commands
    assert '--wheel "$wheel"' in commands
    assert "python -I" in commands
    assert '--expected-version "$VERSION"' in commands


@pytest.mark.parametrize("job_name", ["verify-testpypi", "verify-pypi"])
def test_registry_verification_is_isolated(job_name: str) -> None:
    rendered = json.dumps(load_workflow()["jobs"][job_name])
    assert "scripts/verify_lint_release.py" in rendered
    assert '"persist-credentials": false' in rendered
    assert "python -I" in rendered
    assert sparse_checkout_for(job_name).strip() == "scripts/verify_lint_release.py"
    assert "src" not in sparse_checkout_for(job_name)
    assert ".verify-venv" in rendered
    assert "retry" in rendered.lower()
    assert "300" in rendered


def test_registry_verification_uses_explicit_indexes_and_exact_version() -> None:
    testpypi = run_commands_for("verify-testpypi")
    pypi = run_commands_for("verify-pypi")

    assert "pyvider==${VERSION}" in testpypi
    assert "--index-url https://test.pypi.org/simple/" in testpypi
    assert "--extra-index-url https://pypi.org/simple/" in testpypi
    assert "pyvider==${VERSION}" in pypi
    assert "--index-url https://pypi.org/simple/" in pypi
    assert "test.pypi.org" not in pypi


@pytest.mark.parametrize("job_name", ["verify-testpypi", "verify-pypi"])
def test_registry_retries_refresh_pyvider_index_metadata(job_name: str) -> None:
    assert "--refresh-package pyvider" in run_commands_for(job_name)


def test_wheel_verification_requires_exactly_one_wheel() -> None:
    commands = run_commands_for("verify-wheel")
    assert "${#wheels[@]}" in commands
    assert "exactly one wheel" in commands.lower()
    assert "-print -quit" not in commands


@pytest.mark.parametrize("job_name", ["verify-testpypi", "verify-pypi"])
def test_registry_verification_has_read_only_permissions(job_name: str) -> None:
    job = load_workflow()["jobs"][job_name]
    assert job["permissions"] == {"contents": "read"}
