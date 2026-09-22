#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for the release-time lint API verifier."""

import asyncio
import hashlib
import json
from pathlib import Path
import re
from urllib.request import Request
import zipfile

import pytest

import pyvider
from scripts.verify_lint_release import (
    REQUIRED_WHEEL_PATHS,
    verify_installed,
    verify_lint_behavior,
    verify_registry_metadata,
    verify_registry_release,
    verify_wheel,
)


def write_wheel(
    tmp_path: Path,
    names: set[str] = REQUIRED_WHEEL_PATHS,
    *,
    filename_version: str = "0.8.0",
    metadata_version: str = "0.8.0",
) -> Path:
    wheel = tmp_path / f"pyvider-{filename_version}-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        for name in names:
            archive.writestr(name, "")
        archive.writestr(
            f"pyvider-{metadata_version}.dist-info/METADATA",
            f"Metadata-Version: 2.4\nName: pyvider\nVersion: {metadata_version}\n",
        )
    return wheel


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_release_artifacts(tmp_path: Path) -> tuple[Path, Path, Path]:
    dist = tmp_path / "dist"
    dist.mkdir()
    wheel = write_wheel(dist)
    sdist = dist / "pyvider-0.8.0.tar.gz"
    sdist.write_bytes(b"sdist bytes")
    return dist, wheel, sdist


def registry_metadata(wheel: Path, sdist: Path) -> dict[str, object]:
    return {
        "info": {"version": "0.8.0"},
        "urls": [
            {
                "filename": wheel.name,
                "packagetype": "bdist_wheel",
                "digests": {"sha256": sha256(wheel)},
                "url": f"https://files.pythonhosted.org/packages/{wheel.name}",
            },
            {
                "filename": sdist.name,
                "packagetype": "sdist",
                "digests": {"sha256": sha256(sdist)},
                "url": f"https://files.pythonhosted.org/packages/{sdist.name}",
            },
        ],
    }


def test_wheel_requires_every_lint_module(tmp_path: Path) -> None:
    wheel = write_wheel(tmp_path, REQUIRED_WHEEL_PATHS - {"pyvider/lint/model.py"})
    with pytest.raises(SystemExit, match=r"pyvider/lint/model\.py"):
        verify_wheel(wheel)


def test_complete_wheel_contract_passes(tmp_path: Path) -> None:
    result = verify_wheel(write_wheel(tmp_path), expected_version="v0.8.0")
    assert result["version"] == "0.8.0"


def test_wheel_rejects_filename_metadata_version_mismatch(tmp_path: Path) -> None:
    wheel = write_wheel(tmp_path, filename_version="0.8.0", metadata_version="0.8.1")

    with pytest.raises(SystemExit, match=r"filename version 0\.8\.0.*METADATA version 0\.8\.1"):
        verify_wheel(wheel)


def test_wheel_rejects_release_tag_version_mismatch(tmp_path: Path) -> None:
    wheel = write_wheel(tmp_path)

    with pytest.raises(SystemExit, match=r"expected version 0\.8\.1.*wheel version 0\.8\.0"):
        verify_wheel(wheel, expected_version="v0.8.1")


def test_installed_contract_runs_one_selected_finding() -> None:
    result = asyncio.run(verify_lint_behavior())
    assert result == {"version": pyvider.__version__, "findings": 1, "failed": False}


def test_installed_contract_rejects_version_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pyvider, "__version__", "0.0.0")
    with pytest.raises(SystemExit, match=r"expected 0\.8\.0"):
        asyncio.run(verify_installed(expected_version="0.8.0"))


def test_registry_metadata_requires_exact_artifact_names_and_digests(tmp_path: Path) -> None:
    dist, wheel, sdist = write_release_artifacts(tmp_path)

    artifacts = verify_registry_metadata(
        registry_metadata(wheel, sdist),
        dist_dir=dist,
        expected_version="0.8.0",
        registry_base_url="https://pypi.org",
    )

    assert set(artifacts) == {wheel.name, sdist.name}
    assert artifacts[wheel.name].sha256 == sha256(wheel)


@pytest.mark.parametrize("change", ["missing", "extra"])
def test_registry_metadata_rejects_missing_or_extra_filename(tmp_path: Path, change: str) -> None:
    dist, wheel, sdist = write_release_artifacts(tmp_path)
    metadata = registry_metadata(wheel, sdist)
    urls = metadata["urls"]
    assert isinstance(urls, list)
    if change == "missing":
        urls.pop()
    else:
        urls.append(
            {
                "filename": "pyvider-0.8.0.zip",
                "packagetype": "sdist",
                "digests": {"sha256": "0" * 64},
                "url": "https://files.pythonhosted.org/packages/pyvider-0.8.0.zip",
            }
        )

    with pytest.raises(SystemExit, match="registry artifact filename set does not match"):
        verify_registry_metadata(
            metadata,
            dist_dir=dist,
            expected_version="0.8.0",
            registry_base_url="https://pypi.org",
        )


def test_registry_metadata_rejects_digest_mismatch(tmp_path: Path) -> None:
    dist, wheel, sdist = write_release_artifacts(tmp_path)
    metadata = registry_metadata(wheel, sdist)
    urls = metadata["urls"]
    assert isinstance(urls, list)
    urls[0]["digests"]["sha256"] = "0" * 64

    with pytest.raises(SystemExit, match=rf"digest mismatch.*{re.escape(wheel.name)}"):
        verify_registry_metadata(
            metadata,
            dist_dir=dist,
            expected_version="0.8.0",
            registry_base_url="https://pypi.org",
        )


@pytest.mark.parametrize(
    "url",
    [
        "http://files.pythonhosted.org/packages/pyvider-0.8.0-py3-none-any.whl",
        "file:///tmp/pyvider-0.8.0-py3-none-any.whl",
        "https://example.test/pyvider-0.8.0-py3-none-any.whl",
        "https://user@example.test/pyvider-0.8.0-py3-none-any.whl",
    ],
)
def test_registry_metadata_rejects_unsafe_artifact_url(tmp_path: Path, url: str) -> None:
    dist, wheel, sdist = write_release_artifacts(tmp_path)
    metadata = registry_metadata(wheel, sdist)
    urls = metadata["urls"]
    assert isinstance(urls, list)
    urls[0]["url"] = url

    with pytest.raises(SystemExit, match="unsafe registry artifact URL"):
        verify_registry_metadata(
            metadata,
            dist_dir=dist,
            expected_version="0.8.0",
            registry_base_url="https://pypi.org",
        )


def test_registry_release_downloads_and_verifies_exact_wheel_bytes(tmp_path: Path) -> None:
    dist, wheel, sdist = write_release_artifacts(tmp_path)
    metadata = registry_metadata(wheel, sdist)
    requests: list[Request] = []

    def fetch(request: Request) -> tuple[bytes, str]:
        requests.append(request)
        if "/json" in request.full_url:
            return json.dumps(metadata).encode(), request.full_url
        return wheel.read_bytes(), request.full_url

    result = verify_registry_release(
        registry_base_url="https://pypi.org",
        dist_dir=dist,
        expected_version="v0.8.0",
        download_dir=tmp_path / "download",
        metadata_nonce="run-1-attempt-2",
        fetch=fetch,
    )

    downloaded = Path(str(result["wheel"]))
    assert downloaded.read_bytes() == wheel.read_bytes()
    assert result["artifacts"] == {wheel.name: sha256(wheel), sdist.name: sha256(sdist)}
    assert "verify_nonce=run-1-attempt-2" in requests[0].full_url
    assert requests[0].get_header("Cache-control") == "no-cache"
    assert requests[0].get_header("Pragma") == "no-cache"


def test_registry_release_rejects_downloaded_digest_mismatch(tmp_path: Path) -> None:
    dist, wheel, sdist = write_release_artifacts(tmp_path)
    metadata = registry_metadata(wheel, sdist)

    def fetch(request: Request) -> tuple[bytes, str]:
        if "/json" in request.full_url:
            return json.dumps(metadata).encode(), request.full_url
        return b"different wheel bytes", request.full_url

    with pytest.raises(SystemExit, match="downloaded wheel digest mismatch"):
        verify_registry_release(
            registry_base_url="https://pypi.org",
            dist_dir=dist,
            expected_version="0.8.0",
            download_dir=tmp_path / "download",
            metadata_nonce="fresh",
            fetch=fetch,
        )

    assert not list((tmp_path / "download").glob("*.whl"))
