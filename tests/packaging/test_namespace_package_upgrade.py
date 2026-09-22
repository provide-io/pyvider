# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""The 0.8 release repairs the historical shared ``pyvider`` root ownership."""

from __future__ import annotations

import csv
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tomllib
from typing import cast
import urllib.error
import urllib.parse
import urllib.request
from zipfile import ZipFile

from packaging.markers import Marker
from packaging.tags import sys_tags
from packaging.utils import parse_wheel_filename
import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
ROOT_INITIALIZER = "pyvider/__init__.py"
ROOT_TYPING_MARKER = "pyvider/py.typed"
PRESEED_ENV = "PYVIDER_NAMESPACE_WHEELHOUSE"
TARGET_DISTRIBUTIONS = {"pyvider", "pyvider-cty", "pyvider-rpcplugin"}
TOOLCHAIN_REQUIREMENTS = (
    "packaging==26.3",
    "pip==26.2.1",
    "setuptools==84.0.0",
    "wheel==0.48.0",
)


@dataclass(frozen=True)
class PublishedWheel:
    distribution: str
    version: str
    filename: str
    url: str
    sha256: str
    size: int


PUBLISHED_WHEELS = (
    PublishedWheel(
        distribution="pyvider",
        version="0.7.0",
        filename="pyvider-0.7.0-py3-none-any.whl",
        url=(
            "https://files.pythonhosted.org/packages/df/c7/"
            "ebda0b20968e41966bddd83ef9230effdfba6d5a259636dff795c5d29513/"
            "pyvider-0.7.0-py3-none-any.whl"
        ),
        sha256="d7f024441307310a4d121b90b424fed91e6af657a51b160612bc7b245034856c",
        size=299_880,
    ),
    PublishedWheel(
        distribution="pyvider-cty",
        version="0.6.1",
        filename="pyvider_cty-0.6.1-py3-none-any.whl",
        url=(
            "https://files.pythonhosted.org/packages/38/9f/"
            "014fbb7c371ae700dd573acb335069f6f89ad24542ebbd92add546d6a309/"
            "pyvider_cty-0.6.1-py3-none-any.whl"
        ),
        sha256="9d1135f5e8f0ac95f12c1d08331fcab45327d59652f4b16b6f71dd0b829a0673",
        size=299_140,
    ),
    PublishedWheel(
        distribution="pyvider-rpcplugin",
        version="0.5.4",
        filename="pyvider_rpcplugin-0.5.4-py3-none-any.whl",
        url=(
            "https://files.pythonhosted.org/packages/07/f4/"
            "00954b3cda959afece3f470568454551043fa1204e6a15df187cd3f752f4/"
            "pyvider_rpcplugin-0.5.4-py3-none-any.whl"
        ),
        sha256="764a248d26b35eecd2aa3d45f67af1dcfa07fdb14c512204eb8ce496f61c8feb",
        size=107_670,
    ),
    PublishedWheel(
        distribution="pyvider-cty",
        version="0.6.2",
        filename="pyvider_cty-0.6.2-py3-none-any.whl",
        url=(
            "https://files.pythonhosted.org/packages/d9/03/"
            "bc6f474342705421d5f9f53cd0d9fd103d7ac4ac354cab72f68e17979ada/"
            "pyvider_cty-0.6.2-py3-none-any.whl"
        ),
        sha256="50797dfd3a647218f260a5fcc9a56667fc3c6a00b07b147718c1452e9d542e85",
        size=298_813,
    ),
    PublishedWheel(
        distribution="pyvider-rpcplugin",
        version="0.5.5",
        filename="pyvider_rpcplugin-0.5.5-py3-none-any.whl",
        url=(
            "https://files.pythonhosted.org/packages/7a/20/"
            "7f360ef256c8fdbc38954a02e0f048db859001d002a88b3fd0a30f52e75a/"
            "pyvider_rpcplugin-0.5.5-py3-none-any.whl"
        ),
        sha256="251a40173cc36931a4c85023403b5f54a887f2af3a6cc69891b7f4ca874a2cad",
        size=107_146,
    ),
)


def _run(
    command: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, env=env, check=False, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    return result


def _materialize(spec: PublishedWheel, destination: Path) -> Path:
    preseeded = os.environ.get(PRESEED_ENV)
    if preseeded:
        source = Path(preseeded).expanduser().resolve() / spec.filename
        if not source.is_file():
            raise AssertionError(f"{PRESEED_ENV} is missing {spec.filename}: {source}")
        payload = source.read_bytes()
    else:
        try:
            # Every URL names immutable files.pythonhosted.org bytes and is
            # checked below before the wheel is admitted to the test.
            with urllib.request.urlopen(spec.url, timeout=60) as response:  # nosec B310
                payload = response.read(spec.size + 1)
        except urllib.error.URLError as exc:
            raise AssertionError(
                f"could not fetch pinned {spec.filename}; set {PRESEED_ENV} "
                f"to a complete local wheelhouse: {exc}"
            ) from exc

    assert len(payload) == spec.size, f"{spec.filename}: unexpected size {len(payload)}"
    assert hashlib.sha256(payload).hexdigest() == spec.sha256, (
        f"{spec.filename}: SHA-256 does not match the pinned public artifact"
    )
    wheel = destination / spec.filename
    wheel.write_bytes(payload)
    return wheel


@pytest.fixture(scope="module")
def locked_wheel_specs() -> dict[str, tuple[PublishedWheel, ...]]:
    return {
        "runtime": _exported_wheel_specs("--no-dev"),
        "toolchain": _exported_wheel_specs("--only-group", "packaging-proof"),
    }


def _exported_wheel_specs(*selection: str) -> tuple[PublishedWheel, ...]:
    exported = tomllib.loads(
        _run(
            [
                "uv",
                "export",
                "--frozen",
                "--offline",
                "--no-emit-project",
                "--format",
                "pylock.toml",
                *selection,
            ],
            cwd=REPOSITORY,
        ).stdout
    )
    supported_tags = set(sys_tags())
    specs: list[PublishedWheel] = []
    for package in exported["packages"]:
        if marker := package.get("marker"):
            if not Marker(marker).evaluate():
                continue
        compatible: list[tuple[str, dict[str, object]]] = []
        for wheel in package.get("wheels", []):
            filename = PurePosixPath(urllib.parse.urlparse(wheel["url"]).path).name
            _, _, _, wheel_tags = parse_wheel_filename(filename)
            if wheel_tags & supported_tags:
                compatible.append((filename, wheel))
        assert compatible, f"lock has no compatible wheel for {package['name']}=={package['version']}"
        filename, wheel = min(compatible, key=lambda item: item[0])
        specs.append(
            PublishedWheel(
                distribution=package["name"],
                version=package["version"],
                filename=filename,
                url=cast(str, wheel["url"]),
                sha256=cast(dict[str, str], wheel["hashes"])["sha256"],
                size=cast(int, wheel["size"]),
            )
        )
    return tuple(specs)


@pytest.fixture(scope="module")
def source_wheels(
    tmp_path_factory: pytest.TempPathFactory,
    locked_wheel_specs: dict[str, tuple[PublishedWheel, ...]],
) -> dict[tuple[str, str], Path]:
    destination = tmp_path_factory.mktemp("exact-namespace-wheelhouse")
    specs_by_filename: dict[str, PublishedWheel] = {}
    for spec in (*locked_wheel_specs["runtime"], *locked_wheel_specs["toolchain"], *PUBLISHED_WHEELS):
        existing = specs_by_filename.setdefault(spec.filename, spec)
        assert existing == spec, f"conflicting immutable artifact metadata for {spec.filename}"
    return {
        (spec.distribution, spec.version): _materialize(spec, destination)
        for spec in specs_by_filename.values()
    }


@pytest.fixture(scope="module")
def local_pyvider_wheel(
    tmp_path_factory: pytest.TempPathFactory,
    source_wheels: dict[tuple[str, str], Path],
) -> Path:
    build_root = tmp_path_factory.mktemp("pyvider-080-build")
    source = build_root / "source"
    shutil.copytree(REPOSITORY / "src", source / "src", ignore=shutil.ignore_patterns("*.egg-info"))
    for name in ("LICENSE", "README.md", "VERSION", "pyproject.toml"):
        shutil.copy2(REPOSITORY / name, source / name)

    source_wheelhouse = next(iter(source_wheels.values())).parent
    python, _ = _environment(build_root, source_wheelhouse)
    _resolver_install(
        python,
        source_wheelhouse,
        "uv",
        list(TOOLCHAIN_REQUIREMENTS),
        upgrade=False,
    )
    wheelhouse = build_root / "wheelhouse"
    _run(
        [
            "uv",
            "build",
            "--wheel",
            "--python",
            str(python),
            "--no-build-isolation",
            "--offline",
            "--no-cache",
            "--no-index",
            "--find-links",
            str(source_wheelhouse),
            "--out-dir",
            str(wheelhouse),
            "--no-create-gitignore",
        ],
        cwd=source,
        env=_offline_environment(build_root),
    )
    return next(wheelhouse.glob("pyvider-0.8.0-*.whl"))


def _record_paths(wheel: Path) -> set[str]:
    with ZipFile(wheel) as archive:
        record_name = next(name for name in archive.namelist() if name.endswith(".dist-info/RECORD"))
        return {row[0] for row in csv.reader(archive.read(record_name).decode().splitlines())}


def _installed_record_paths(record: Path) -> set[str]:
    with record.open(newline="") as rows:
        return {row[0] for row in csv.reader(rows)}


def _offline_environment(destination: Path) -> dict[str, str]:
    environment = os.environ.copy()
    environment.update(
        {
            "PIP_INDEX_URL": "https://offline.invalid/simple",
            "PIP_NO_INDEX": "1",
            "UV_CACHE_DIR": str(destination / "empty-uv-cache"),
            "UV_INDEX_URL": "https://offline.invalid/simple",
            "UV_NO_INDEX": "1",
            "UV_OFFLINE": "1",
        }
    )
    return environment


def _environment(destination: Path, wheelhouse: Path) -> tuple[Path, Path]:
    root = destination / "environment"
    _run(
        [
            "uv",
            "venv",
            "--python",
            sys.executable,
            "--no-project",
            "--no-python-downloads",
            "--offline",
            "--no-cache",
            str(root),
        ],
        env=_offline_environment(destination),
    )
    python = root / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    _resolver_install(python, wheelhouse, "uv", ["pip==26.2.1"], upgrade=False)
    purelib = Path(
        _run(
            [str(python), "-I", "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"],
            cwd=destination,
        ).stdout.strip()
    )
    return python, purelib


def _resolver_install(
    python: Path,
    wheelhouse: Path,
    manager: str,
    requirements: list[str],
    *,
    upgrade: bool,
) -> None:
    environment = _offline_environment(python.parent.parent)
    if manager == "uv":
        command = [
            "uv",
            "pip",
            "install",
            "--offline",
            "--no-cache",
            "--no-index",
            "--find-links",
            str(wheelhouse),
            "--python",
            str(python),
        ]
    elif manager == "pip":
        command = [
            str(python),
            "-m",
            "pip",
            "install",
            "--no-index",
            "--find-links",
            str(wheelhouse),
            "--no-cache-dir",
        ]
    else:
        raise AssertionError(f"unknown package manager: {manager}")
    if upgrade:
        command.append("--upgrade")
    _run([*command, *requirements], env=environment)


def _dependency_check(python: Path, manager: str) -> None:
    environment = _offline_environment(python.parent.parent)
    if manager == "uv":
        _run(["uv", "pip", "check", "--python", str(python)], env=environment)
    else:
        _run([str(python), "-m", "pip", "check"], env=environment)


def _stage_wheelhouse(
    destination: Path,
    source_wheels: dict[tuple[str, str], Path],
    runtime_specs: tuple[PublishedWheel, ...],
    target_versions: dict[str, str],
    *,
    local_pyvider_wheel: Path | None = None,
) -> Path:
    destination.mkdir()
    for spec in runtime_specs:
        if spec.distribution in TARGET_DISTRIBUTIONS:
            continue
        shutil.copy2(source_wheels[(spec.distribution, spec.version)], destination)
    for requirement in TOOLCHAIN_REQUIREMENTS:
        name, version = requirement.split("==", maxsplit=1)
        shutil.copy2(source_wheels[(name, version)], destination)
    for distribution, version in target_versions.items():
        if distribution == "pyvider" and local_pyvider_wheel is not None:
            shutil.copy2(local_pyvider_wheel, destination)
        else:
            shutil.copy2(source_wheels[(distribution, version)], destination)
    return destination


def _installed_versions(python: Path, cwd: Path) -> dict[str, str | None]:
    result = _run(
        [
            str(python),
            "-I",
            "-c",
            (
                "import importlib.util, json, pathlib, pyvider, pyvider.cty, pyvider.rpcplugin; "
                "lint = (importlib.import_module('pyvider.lint') "
                "if importlib.util.find_spec('pyvider.lint') is not None else None); "
                "print(json.dumps({'pyvider': pyvider.__version__, "
                "'cty': pyvider.cty.__version__, 'rpcplugin': pyvider.rpcplugin.__version__, "
                "'root': str(pathlib.Path(pyvider.__file__).resolve()), "
                "'lint': lint is not None}))"
            ),
        ],
        cwd=cwd,
    )
    return cast(dict[str, str | None], json.loads(result.stdout))


def _uninstall(python: Path, distribution: str, manager: str) -> None:
    if manager == "uv":
        _run(["uv", "pip", "uninstall", "--python", str(python), distribution])
        return
    if manager == "pip":
        _run([str(python), "-m", "pip", "uninstall", "--yes", distribution])
        return
    raise AssertionError(f"unknown package manager: {manager}")


def _assert_owner_survives(python: Path, purelib: Path, cwd: Path) -> None:
    assert (purelib / ROOT_INITIALIZER).is_file()
    assert (purelib / ROOT_TYPING_MARKER).is_file()
    result = _run(
        [
            str(python),
            "-I",
            "-c",
            "import pyvider, pyvider.lint; assert pyvider.__version__ == '0.8.0'",
        ],
        cwd=cwd,
    )
    assert result.stdout == ""


def _assert_contributor_survives(python: Path, distribution: str, cwd: Path) -> None:
    module, version = {
        "pyvider-cty": ("pyvider.cty", "0.6.2"),
        "pyvider-rpcplugin": ("pyvider.rpcplugin", "0.5.5"),
    }[distribution]
    result = _run(
        [
            str(python),
            "-I",
            "-c",
            f"import {module} as contributor; assert contributor.__version__ == {version!r}",
        ],
        cwd=cwd,
    )
    assert result.stdout == ""


def _runtime_dependencies() -> set[str]:
    pyproject = tomllib.loads((REPOSITORY / "pyproject.toml").read_text())
    return set(pyproject["project"]["dependencies"])


def test_runtime_dependencies_require_single_owner_namespace_releases() -> None:
    dependencies = _runtime_dependencies()

    assert "pyvider-cty>=0.6.2" in dependencies
    assert "pyvider-rpcplugin>=0.5.5" in dependencies


def test_lock_resolves_the_single_owner_namespace_releases() -> None:
    lock = tomllib.loads((REPOSITORY / "uv.lock").read_text())
    packages = {package["name"]: package for package in lock["package"]}
    pyvider_requirements = {
        requirement["name"]: requirement["specifier"]
        for requirement in packages["pyvider"]["metadata"]["requires-dist"]
    }

    assert pyvider_requirements["pyvider-cty"] == ">=0.6.2"
    assert pyvider_requirements["pyvider-rpcplugin"] == ">=0.5.5"
    assert packages["pyvider-cty"]["version"] == "0.6.2"
    assert packages["pyvider-rpcplugin"]["version"] == "0.5.5"


def test_packaging_proof_toolchain_is_exactly_locked() -> None:
    pyproject = tomllib.loads((REPOSITORY / "pyproject.toml").read_text())
    lock = tomllib.loads((REPOSITORY / "uv.lock").read_text())
    packages = {package["name"]: package for package in lock["package"]}

    assert set(pyproject["dependency-groups"]["packaging-proof"]) == {
        "pip==26.2.1",
        "setuptools==84.0.0",
        "wheel==0.48.0",
    }
    assert packages["pip"]["version"] == "26.2.1"
    assert packages["setuptools"]["version"] == "84.0.0"
    assert packages["wheel"]["version"] == "0.48.0"


def test_release_notes_explain_the_one_time_coordinated_upgrade() -> None:
    release_notes = (REPOSITORY / "CHANGELOG.md").read_text().split("## [0.7.0]", maxsplit=1)[0]
    normalized = " ".join(release_notes.split())

    assert "`pyvider-cty>=0.6.2`" in release_notes
    assert "`pyvider-rpcplugin>=0.5.5`" in release_notes
    assert "sole owner" in normalized
    assert "`pyvider/__init__.py`" in release_notes
    assert "`pyvider/py.typed`" in release_notes
    assert "one-time" in normalized
    assert "same operation" in normalized
    assert "reinstall Pyvider" in normalized


def test_published_wheels_can_be_preseeded_without_network(
    source_wheels: dict[tuple[str, str], Path],
    locked_wheel_specs: dict[str, tuple[PublishedWheel, ...]],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    preseed = next(iter(source_wheels.values())).parent
    monkeypatch.setenv(PRESEED_ENV, str(preseed))

    def unexpected_network_request(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("a preseeded wheel fixture must not access the network")

    monkeypatch.setattr(urllib.request, "urlopen", unexpected_network_request)
    all_specs = {
        spec.filename: spec
        for spec in (*locked_wheel_specs["runtime"], *locked_wheel_specs["toolchain"], *PUBLISHED_WHEELS)
    }
    materialized = [_materialize(spec, tmp_path) for spec in all_specs.values()]

    assert {wheel.name for wheel in materialized} == set(all_specs)


def test_only_pyvider_080_owns_the_shared_root_files(
    local_pyvider_wheel: Path,
    source_wheels: dict[tuple[str, str], Path],
) -> None:
    owner_record = _record_paths(local_pyvider_wheel)
    cty_record = _record_paths(source_wheels[("pyvider-cty", "0.6.2")])
    rpcplugin_record = _record_paths(source_wheels[("pyvider-rpcplugin", "0.5.5")])

    assert {ROOT_INITIALIZER, ROOT_TYPING_MARKER} <= owner_record
    assert ROOT_INITIALIZER not in cty_record
    assert ROOT_TYPING_MARKER not in cty_record
    assert ROOT_INITIALIZER not in rpcplugin_record
    assert ROOT_TYPING_MARKER not in rpcplugin_record


@pytest.mark.integration
@pytest.mark.parametrize(
    ("upgrade_manager", "uninstalls"),
    [
        ("uv", (("pyvider-cty", "uv"), ("pyvider-rpcplugin", "pip"))),
        ("pip", (("pyvider-rpcplugin", "pip"), ("pyvider-cty", "uv"))),
        ("uv", (("pyvider-cty", "pip"), ("pyvider-rpcplugin", "uv"))),
        ("pip", (("pyvider-rpcplugin", "uv"), ("pyvider-cty", "pip"))),
    ],
    ids=[
        "upgrade-uv-cty-uv-rpc-pip",
        "upgrade-pip-rpc-pip-cty-uv",
        "upgrade-uv-cty-pip-rpc-uv",
        "upgrade-pip-rpc-uv-cty-pip",
    ],
)
def test_published_stack_coordinated_upgrade_and_dependency_uninstalls(
    local_pyvider_wheel: Path,
    source_wheels: dict[tuple[str, str], Path],
    locked_wheel_specs: dict[str, tuple[PublishedWheel, ...]],
    monkeypatch: pytest.MonkeyPatch,
    upgrade_manager: str,
    uninstalls: tuple[tuple[str, str], tuple[str, str]],
    tmp_path: Path,
) -> None:
    preseed = next(iter(source_wheels.values())).parent
    monkeypatch.setenv(PRESEED_ENV, str(preseed))

    def unexpected_network_request(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("the coordinated upgrade proof must not access the network")

    monkeypatch.setattr(urllib.request, "urlopen", unexpected_network_request)
    all_specs = {
        spec.filename: spec
        for spec in (*locked_wheel_specs["runtime"], *locked_wheel_specs["toolchain"], *PUBLISHED_WHEELS)
    }
    cold_source = tmp_path / "cold-source"
    cold_source.mkdir()
    cold_wheels = {
        (spec.distribution, spec.version): _materialize(spec, cold_source) for spec in all_specs.values()
    }
    old_wheelhouse = _stage_wheelhouse(
        tmp_path / "old-wheelhouse",
        cold_wheels,
        locked_wheel_specs["runtime"],
        {"pyvider": "0.7.0", "pyvider-cty": "0.6.1", "pyvider-rpcplugin": "0.5.4"},
    )
    current_wheelhouse = _stage_wheelhouse(
        tmp_path / "current-wheelhouse",
        cold_wheels,
        locked_wheel_specs["runtime"],
        {"pyvider": "0.8.0", "pyvider-cty": "0.6.2", "pyvider-rpcplugin": "0.5.5"},
        local_pyvider_wheel=local_pyvider_wheel,
    )
    python, purelib = _environment(tmp_path, old_wheelhouse)

    # Resolve the complete published 0.7 stack from a checksum-verified local
    # wheelhouse. Its three wheels historically co-owned the root files, so the
    # healthy starting state intentionally resolves contributors first and the
    # dependent root owner second. Both phases still use normal dependency
    # resolution: no dependency is injected with --no-deps or an online seed.
    _resolver_install(
        python,
        old_wheelhouse,
        upgrade_manager,
        ["pyvider-cty==0.6.1", "pyvider-rpcplugin==0.5.4"],
        upgrade=False,
    )
    _resolver_install(python, old_wheelhouse, upgrade_manager, ["pyvider==0.7.0"], upgrade=False)
    assert _installed_versions(python, tmp_path) == {
        "pyvider": "0.7.0",
        "cty": "0.6.1",
        "rpcplugin": "0.5.4",
        "root": str((purelib / ROOT_INITIALIZER).resolve()),
        "lint": False,
    }

    # Exercise each real resolver's upgrade semantics. The three coordinated
    # pins are selected by package name, never installed as direct wheel paths.
    _resolver_install(
        python,
        current_wheelhouse,
        upgrade_manager,
        ["pyvider==0.8.0", "pyvider-cty==0.6.2", "pyvider-rpcplugin==0.5.5"],
        upgrade=True,
    )
    _dependency_check(python, upgrade_manager)
    assert _installed_versions(python, tmp_path) == {
        "pyvider": "0.8.0",
        "cty": "0.6.2",
        "rpcplugin": "0.5.5",
        "root": str((purelib / ROOT_INITIALIZER).resolve()),
        "lint": True,
    }

    records = {
        "pyvider": _installed_record_paths(next(purelib.glob("pyvider-0.8.0.dist-info/RECORD"))),
        "pyvider-cty": _installed_record_paths(next(purelib.glob("pyvider_cty-0.6.2.dist-info/RECORD"))),
        "pyvider-rpcplugin": _installed_record_paths(
            next(purelib.glob("pyvider_rpcplugin-0.5.5.dist-info/RECORD"))
        ),
    }
    assert {ROOT_INITIALIZER, ROOT_TYPING_MARKER} <= records["pyvider"]
    for contributor in ("pyvider-cty", "pyvider-rpcplugin"):
        assert ROOT_INITIALIZER not in records[contributor]
        assert ROOT_TYPING_MARKER not in records[contributor]

    for index, (distribution, manager) in enumerate(uninstalls):
        _uninstall(python, distribution, manager)
        _assert_owner_survives(python, purelib, tmp_path)
        if index == 0:
            _assert_contributor_survives(python, uninstalls[1][0], tmp_path)

    assert not list(purelib.glob("pyvider_cty-*.dist-info"))
    assert not list(purelib.glob("pyvider_rpcplugin-*.dist-info"))
