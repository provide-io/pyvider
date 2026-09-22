#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Verify that a release wheel contains and runs the public lint API."""

from __future__ import annotations

import argparse
import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from email.parser import BytesParser
import hashlib
import json
from pathlib import Path
import re
import sys
import time
from urllib.parse import quote, unquote, urlencode, urlparse
from urllib.request import Request, urlopen
import zipfile

REQUIRED_WHEEL_PATHS = {
    "pyvider/lint/__init__.py",
    "pyvider/lint/model.py",
    "pyvider/lint/selector.py",
    "pyvider/lint/_runner.py",
    "pyvider/protocols/tfprotov6/handlers/_linting.py",
}


@dataclass(frozen=True)
class RegistryArtifact:
    """One artifact declared by registry release metadata."""

    filename: str
    sha256: str
    url: str
    packagetype: str


URLFetcher = Callable[[Request], tuple[bytes, str]]

WHEEL_FILENAME = re.compile(r"^pyvider-(?P<version>[^-]+)-.+\.whl$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REGISTRY_ARTIFACT_HOSTS = {
    "pypi.org": {"files.pythonhosted.org"},
    "test.pypi.org": {"test-files.pythonhosted.org"},
}


def normalize_version(value: str) -> str:
    """Normalize a release tag's optional leading ``v``."""
    version = value.removeprefix("v")
    if not version or version != version.strip() or any(character in version for character in "/\\?#"):
        raise SystemExit(f"invalid expected version: {value!r}")
    return version


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as artifact:
        for chunk in iter(lambda: artifact.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _registry_origin(registry_base_url: str) -> tuple[str, str]:
    parsed = urlparse(registry_base_url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port is not None
        or parsed.path not in {"", "/"}
        or parsed.params
        or parsed.query
        or parsed.fragment
    ):
        raise SystemExit(f"unsafe registry base URL: {registry_base_url}")
    return parsed.scheme, parsed.hostname


def _validate_artifact_url(url: str, *, filename: str, registry_base_url: str) -> None:
    _, registry_host = _registry_origin(registry_base_url)
    parsed = urlparse(url)
    allowed_hosts = {registry_host, *REGISTRY_ARTIFACT_HOSTS.get(registry_host, set())}
    if (
        parsed.scheme != "https"
        or parsed.hostname not in allowed_hosts
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port is not None
        or unquote(Path(parsed.path).name) != filename
    ):
        raise SystemExit(f"unsafe registry artifact URL for {filename}: {url}")


def _local_artifact_digests(dist_dir: Path, *, expected_version: str) -> dict[str, str]:
    if not dist_dir.is_dir():
        raise SystemExit(f"release artifact directory does not exist: {dist_dir}")
    files = sorted(
        path
        for path in dist_dir.iterdir()
        if path.is_file() and (path.name.endswith(".whl") or path.name.endswith(".tar.gz"))
    )
    wheels = [path for path in files if path.name.endswith(".whl")]
    sdists = [path for path in files if path.name.endswith(".tar.gz")]
    if len(wheels) != 1 or len(sdists) != 1 or len(files) != 2:
        raise SystemExit(
            f"expected exactly one wheel and one sdist in {dist_dir}, found "
            f"{len(wheels)} wheel(s) and {len(sdists)} sdist(s)"
        )
    verify_wheel(wheels[0], expected_version=expected_version)
    expected_sdist = f"pyvider-{expected_version}.tar.gz"
    if sdists[0].name != expected_sdist:
        raise SystemExit(f"expected sdist {expected_sdist}, found {sdists[0].name}")
    return {path.name: _sha256_file(path) for path in files}


def _metadata_artifacts(
    metadata: dict[str, object],
    *,
    expected_version: str,
    registry_base_url: str,
) -> dict[str, RegistryArtifact]:
    info = metadata.get("info")
    urls = metadata.get("urls")
    if not isinstance(info, dict) or info.get("version") != expected_version:
        actual = info.get("version") if isinstance(info, dict) else None
        raise SystemExit(f"registry metadata version mismatch: expected {expected_version}, got {actual!r}")
    if not isinstance(urls, list):
        raise SystemExit("registry metadata has no artifact list")

    artifacts: dict[str, RegistryArtifact] = {}
    for entry in urls:
        if not isinstance(entry, dict):
            raise SystemExit("registry metadata contains an invalid artifact entry")
        filename = entry.get("filename")
        packagetype = entry.get("packagetype")
        digests = entry.get("digests")
        url = entry.get("url")
        sha256 = digests.get("sha256") if isinstance(digests, dict) else None
        if (
            not isinstance(filename, str)
            or Path(filename).name != filename
            or not isinstance(packagetype, str)
            or not isinstance(url, str)
            or not isinstance(sha256, str)
            or SHA256.fullmatch(sha256) is None
        ):
            raise SystemExit("registry metadata contains invalid artifact fields")
        if filename in artifacts:
            raise SystemExit(f"registry metadata contains duplicate artifact: {filename}")
        _validate_artifact_url(url, filename=filename, registry_base_url=registry_base_url)
        artifacts[filename] = RegistryArtifact(filename, sha256, url, packagetype)
    return artifacts


def verify_registry_metadata(
    metadata: dict[str, object],
    *,
    dist_dir: Path,
    expected_version: str,
    registry_base_url: str,
) -> dict[str, RegistryArtifact]:
    """Compare registry metadata with locally built release artifacts."""
    version = normalize_version(expected_version)
    local = _local_artifact_digests(dist_dir, expected_version=version)
    registry = _metadata_artifacts(
        metadata,
        expected_version=version,
        registry_base_url=registry_base_url,
    )
    if set(registry) != set(local):
        missing = sorted(set(local) - set(registry))
        extra = sorted(set(registry) - set(local))
        raise SystemExit(
            "registry artifact filename set does not match release artifacts: "
            f"missing={missing}, extra={extra}"
        )
    for filename, digest in local.items():
        if registry[filename].sha256 != digest:
            raise SystemExit(
                f"registry artifact digest mismatch for {filename}: "
                f"expected {digest}, got {registry[filename].sha256}"
            )
    return registry


def _fetch_url(request: Request) -> tuple[bytes, str]:
    with urlopen(request, timeout=30) as response:
        return response.read(), response.geturl()


def verify_registry_release(
    *,
    registry_base_url: str,
    dist_dir: Path,
    expected_version: str,
    download_dir: Path,
    metadata_nonce: str = "",
    fetch: URLFetcher | None = None,
) -> dict[str, object]:
    """Verify registry metadata and download its exact wheel."""
    version = normalize_version(expected_version)
    scheme, registry_host = _registry_origin(registry_base_url)
    nonce = metadata_nonce or str(time.time_ns())
    metadata_url = f"{scheme}://{registry_host}/pypi/pyvider/{quote(version, safe='')}/json?" + urlencode(
        {"verify_nonce": nonce}
    )
    headers = {"Cache-Control": "no-cache", "Pragma": "no-cache", "Accept": "application/json"}
    fetch_url = fetch or _fetch_url
    raw_metadata, final_metadata_url = fetch_url(Request(metadata_url, headers=headers))
    final_metadata = urlparse(final_metadata_url)
    if (
        final_metadata.scheme != "https"
        or final_metadata.hostname != registry_host
        or final_metadata.username is not None
        or final_metadata.password is not None
    ):
        raise SystemExit(f"unsafe registry metadata redirect: {final_metadata_url}")
    try:
        parsed_metadata = json.loads(raw_metadata.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit("registry returned invalid JSON metadata") from exc
    if not isinstance(parsed_metadata, dict):
        raise SystemExit("registry returned non-object JSON metadata")
    artifacts = verify_registry_metadata(
        parsed_metadata,
        dist_dir=dist_dir,
        expected_version=version,
        registry_base_url=registry_base_url,
    )
    wheels = [artifact for artifact in artifacts.values() if artifact.filename.endswith(".whl")]
    if len(wheels) != 1:
        raise SystemExit(f"expected exactly one registry wheel, found {len(wheels)}")
    wheel = wheels[0]
    downloaded_bytes, final_artifact_url = fetch_url(Request(wheel.url, headers=headers))
    _validate_artifact_url(final_artifact_url, filename=wheel.filename, registry_base_url=registry_base_url)
    downloaded_digest = _sha256_bytes(downloaded_bytes)
    if downloaded_digest != wheel.sha256:
        raise SystemExit(
            f"downloaded wheel digest mismatch for {wheel.filename}: "
            f"expected {wheel.sha256}, got {downloaded_digest}"
        )

    download_dir.mkdir(parents=True, exist_ok=True)
    target = download_dir / wheel.filename
    temporary = download_dir / f".{wheel.filename}.part"
    temporary.write_bytes(downloaded_bytes)
    temporary.replace(target)
    verify_wheel(target, expected_version=version)
    return {
        "artifacts": {filename: artifact.sha256 for filename, artifact in sorted(artifacts.items())},
        "registry": f"{scheme}://{registry_host}",
        "version": version,
        "wheel": str(target.resolve()),
    }


def _resolved_path(value: str) -> Path:
    return Path(value).resolve()


async def verify_lint_behavior() -> dict[str, object]:
    """Exercise the installed public lint model, selector, and runner."""
    import pyvider
    from pyvider.lint import LintContext, LintFinding, LintSelector
    from pyvider.lint._runner import run_lints

    class Component:
        async def lint(self, ctx: object) -> tuple[LintFinding, ...]:
            return (
                LintFinding(
                    rule="release/pyvider:smoke",
                    groups=("release/pyvider:all",),
                    summary="Release verifier finding",
                    detail="The public runner executed the installed lint hook.",
                    attribute_path="name",
                ),
            )

    selector = LintSelector.parse(("release/pyvider:all",))
    context = LintContext({"name": "release"}, selector)
    if not context.enabled("release/pyvider:smoke", "release/pyvider:all"):
        raise SystemExit("public LintContext selector contract failed")
    result = await run_lints(
        Component(),
        context.config,
        context.selector,
        kind="provider",
        name="release-smoke",
        operation="verify-release",
    )
    if result.failed or len(result.findings) != 1:
        raise SystemExit(f"unexpected lint result: {result!r}")
    return {"version": pyvider.__version__, "findings": 1, "failed": False}


async def verify_installed(*, expected_version: str) -> dict[str, object]:
    """Verify the version, origin, and lint behavior of installed Pyvider."""
    import pyvider

    if pyvider.__version__ != expected_version:
        raise SystemExit(f"expected {expected_version}, got {pyvider.__version__}")
    origin = _resolved_path(pyvider.__file__)
    if _resolved_path(sys.prefix) not in origin.parents:
        raise SystemExit(f"pyvider imported outside isolated environment: {origin}")
    result = await verify_lint_behavior()
    result["origin"] = str(origin)
    return result


def verify_wheel(path: Path, *, expected_version: str | None = None) -> dict[str, str]:
    """Require lint modules and consistent wheel, metadata, and release versions."""
    match = WHEEL_FILENAME.fullmatch(path.name)
    if match is None:
        raise SystemExit(f"invalid pyvider wheel filename: {path.name}")
    filename_version = match.group("version")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        missing = REQUIRED_WHEEL_PATHS - set(names)
        metadata_names = [name for name in names if name.endswith(".dist-info/METADATA")]
    if missing:
        raise SystemExit("wheel missing: " + ", ".join(sorted(missing)))
    if len(metadata_names) != 1:
        raise SystemExit(f"expected exactly one wheel METADATA file, found {len(metadata_names)}")
    with zipfile.ZipFile(path) as archive:
        metadata = BytesParser().parsebytes(archive.read(metadata_names[0]))
    if metadata.get("Name") != "pyvider":
        raise SystemExit(f"wheel METADATA project is not pyvider: {metadata.get('Name')!r}")
    metadata_version = metadata.get("Version")
    if metadata_version != filename_version:
        raise SystemExit(
            f"wheel filename version {filename_version} does not match METADATA version {metadata_version}"
        )
    if expected_version is not None:
        normalized_expected = normalize_version(expected_version)
        if filename_version != normalized_expected:
            raise SystemExit(f"expected version {normalized_expected}, wheel version {filename_version}")
    return {"version": filename_version, "wheel": str(path.resolve())}


def main(argv: list[str] | None = None) -> int:
    """Run one release verification mode from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--wheel", type=Path, help="inspect a built wheel archive")
    mode.add_argument("--registry-base-url", help="verify a published registry release")
    mode.add_argument("--verify-installed", action="store_true", help="verify the installed distribution")
    parser.add_argument("--expected-version", help="expected release or installed version")
    parser.add_argument("--dist-dir", type=Path, help="directory containing the original wheel and sdist")
    parser.add_argument("--download-dir", type=Path, help="destination for the verified registry wheel")
    parser.add_argument("--metadata-nonce", default="", help="unique cache-busting registry metadata token")
    args = parser.parse_args(argv)

    if args.wheel is not None:
        result = verify_wheel(args.wheel, expected_version=args.expected_version)
        print(json.dumps(result, sort_keys=True))
        return 0

    if not args.expected_version:
        parser.error("--expected-version is required for installed and registry verification")
    if args.registry_base_url is not None:
        if args.dist_dir is None or args.download_dir is None:
            parser.error("registry verification requires --dist-dir and --download-dir")
        result = verify_registry_release(
            registry_base_url=args.registry_base_url,
            dist_dir=args.dist_dir,
            expected_version=args.expected_version,
            download_dir=args.download_dir,
            metadata_nonce=args.metadata_nonce,
        )
        print(json.dumps(result, sort_keys=True))
        return 0

    result = asyncio.run(verify_installed(expected_version=args.expected_version))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
