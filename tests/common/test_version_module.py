"""Tests covering lightweight package/version accessors."""

import importlib
import importlib.metadata
from pathlib import Path

import pytest


def test_package_init_exports_version() -> None:
    """Importing the top-level package should expose consistent version metadata."""
    import pyvider
    import pyvider._version as version_module

    assert pyvider.__all__ == ["__version__"]
    assert pyvider.__version__ == version_module.__version__


def test_find_project_root_discovers_version_file() -> None:
    """Project root discovery should locate the repository VERSION marker."""
    from pyvider._version import _find_project_root

    project_root = _find_project_root()
    assert project_root is not None
    assert (project_root / "VERSION").is_file()


def test_get_version_uses_metadata_when_version_file_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """When VERSION is absent, metadata lookup should provide the version."""
    import pyvider._version as version_module

    monkeypatch.setattr(version_module, "_find_project_root", lambda: None)
    monkeypatch.setattr(importlib.metadata, "version", lambda _: "9.9.9-test")

    assert version_module.get_version() == "9.9.9-test"


def test_get_version_falls_back_to_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """If metadata lookup fails, the function should return the development default."""
    import pyvider._version as version_module

    monkeypatch.setattr(version_module, "_find_project_root", lambda: None)

    def _raise(_: str) -> str:
        raise importlib.metadata.PackageNotFoundError

    monkeypatch.setattr(importlib.metadata, "version", _raise)

    assert version_module.get_version() == "0.0.0-dev"

def test_get_version_reads_version_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Happy path should read the VERSION file discovered in the project tree."""
    import pyvider._version as version_module

    project_root = tmp_path / "project"
    project_root.mkdir()
    version_file = project_root / "VERSION"
    version_file.write_text("1.2.3-test\n")

    monkeypatch.setattr(version_module, "_find_project_root", lambda: project_root)

    assert version_module.get_version() == "1.2.3-test"


def test_find_project_root_returns_none_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """The helper should gracefully return None when the VERSION marker is absent."""
    import pyvider._version as version_module

    class _Path(Path):
        _flavour = Path(".")._flavour

    fake_start = _Path("/tmp")

    monkeypatch.setattr(version_module, "Path", lambda *_: fake_start)
    monkeypatch.setattr(Path, "exists", lambda self: False)

    assert version_module._find_project_root() is None
