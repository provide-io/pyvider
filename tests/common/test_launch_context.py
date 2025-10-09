"""Tests for launch context detection helpers."""

import types

import pytest

import pyvider.common.launch_context as lc
from pyvider.common.launch_context import (
    LaunchContext,
    LaunchMethod,
    _analyze_cache_structure,
    _analyze_executable,
    _get_module_name,
    _get_pspf_details,
    _is_direct_script_launch,
    _is_editable_install,
    _is_module_launch,
    _is_pspf_launch,
    detect_launch_context,
    log_launch_context,
)


def test_detect_launch_context_collects_environment(monkeypatch):
    monkeypatch.setitem(lc.os.environ, "TF_PLUGIN_MAGIC_COOKIE", "1")
    monkeypatch.setitem(lc.os.environ, "PSPF_TOKEN", "secret")
    monkeypatch.setattr(lc.sys, "argv", ["/app/__main__.py"])
    monkeypatch.setattr(lc.sys, "executable", "/opt/python")
    monkeypatch.setattr(lc.sys, "version", "3.x-test")
    monkeypatch.setattr(lc.sys, "platform", "posix")
    monkeypatch.setattr(lc.sys, "path", ["one", "two", "three"])
    monkeypatch.setattr(lc.os, "getcwd", lambda: "/workspace")
    monkeypatch.setattr(lc, "_detect_launch_method", lambda exe, py: (LaunchMethod.UNKNOWN, {"reason": "patched"}))

    context = detect_launch_context()

    assert context.is_terraform_invoked is True
    assert context.details == {"reason": "patched"}
    assert context.environment_info["terraform_cookie_present"] is True
    assert "pspf_env_vars" in context.environment_info
    assert context.working_directory == "/workspace"


def test_is_pspf_launch_detects_cache_path():
    assert _is_pspf_launch("terraform-provider-pyvider", "/tmp/.cache/pspf/python") is True


def test_is_module_launch_with_main(monkeypatch):
    monkeypatch.setattr(lc.sys, "argv", ["/tmp/pyvider/__main__.py"])
    assert _is_module_launch() is True


def test_is_editable_install_detects_src(monkeypatch):
    dummy_pyvider = types.SimpleNamespace(
        __file__="/repo/src/pyvider/__init__.py",
        __path__=["/repo/src/pyvider"],
    )
    monkeypatch.setattr(lc, "pyvider", dummy_pyvider, raising=False)
    assert _is_editable_install("/repo/.venv/bin/pyvider") is True


def test_get_module_name_defaults(monkeypatch):
    monkeypatch.setattr(lc.sys, "argv", ["pyvider"])
    assert _get_module_name() == "pyvider"


def test_analyze_executable_reports_files(tmp_path):
    script = tmp_path / "main.py"
    script.write_text("print('hi')")
    info = _analyze_executable(str(script))
    assert info["exists"] is True
    assert info["is_file"] is True
    assert info["suffix"] == ".py"


def test_analyze_cache_structure_lists_directories(tmp_path, monkeypatch):
    bin_dir = tmp_path / "cache" / "bin"
    bin_dir.mkdir(parents=True)
    (tmp_path / "cache" / "metadata").mkdir(parents=True)
    python_path = bin_dir / "python"
    python_path.write_text("")

    monkeypatch.setattr(lc.sys, "executable", str(python_path))

    details = _get_pspf_details()
    assert "metadata_path" in details

    structure = _analyze_cache_structure(python_path)
    assert structure["python_bin_dir"].endswith("bin")
    assert "metadata" in structure["contents"]


def test_log_launch_context_uses_logger(monkeypatch):
    captured = []
    context = LaunchContext(
        method=LaunchMethod.UNKNOWN,
        executable_path="/tmp/app",
        python_executable="/usr/bin/python",
        working_directory="/tmp",
        environment_info={},
        is_terraform_invoked=False,
        details={},
    )

    monkeypatch.setattr(lc, "detect_launch_context", lambda: context)

    result = log_launch_context(captured.append)

    assert result is context
    assert any("Launch Context" in entry for entry in captured)


def test_is_direct_script_launch_handles_py_extension():
    assert _is_direct_script_launch("/tmp/tool.py") is True

def test_detect_launch_method_prefers_direct_script(monkeypatch):
    monkeypatch.setattr(lc, "_is_pspf_launch", lambda exe, py: False)
    monkeypatch.setattr(lc, "_is_module_launch", lambda: False)
    monkeypatch.setattr(lc, "_is_editable_install", lambda exe: False)
    method, details = lc._detect_launch_method("/tmp/script.py", "/usr/bin/python")

    assert method is LaunchMethod.SCRIPT_DIRECT
    assert details["script_path"] == "/tmp/script.py"


def test_detect_launch_method_prefers_pspf(monkeypatch):
    monkeypatch.setattr(lc, "_is_pspf_launch", lambda exe, py: True)
    monkeypatch.setattr(lc, "_get_pspf_details", lambda: {"cache": "info"})
    method, details = lc._detect_launch_method("/tmp/provider", "/tmp/cache/python")

    assert method is LaunchMethod.PSPF_PACKAGE
    assert details["cache"] == "info"


def test_detect_launch_method_handles_editable(monkeypatch):
    monkeypatch.setattr(lc, "_is_pspf_launch", lambda exe, py: False)
    monkeypatch.setattr(lc, "_is_module_launch", lambda: False)
    monkeypatch.setattr(lc, "_is_editable_install", lambda exe: True)
    monkeypatch.setattr(lc, "_get_editable_install_details", lambda exe: {"executable_path": exe})

    method, details = lc._detect_launch_method("/repo/.venv/bin/pyvider", "/usr/bin/python")

    assert method is LaunchMethod.EDITABLE_INSTALL
    assert details["executable_path"] == "/repo/.venv/bin/pyvider"
