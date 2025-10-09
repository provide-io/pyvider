"""Tests for CLI utility helpers."""

from types import SimpleNamespace

import pytest

from provide.foundation.process import ProcessError

from pyvider.cli.utils import _place_terraform_provider_script, _run_command


class DummyTimer:
    def __enter__(self):
        self.elapsed = 0.5
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_run_command_logs_success(monkeypatch, tmp_path):
    log_dir = tmp_path / ".pyvider" / "logs"
    (tmp_path / "workspace").mkdir()

    outputs: list[str] = []
    log_capture: dict[str, str] = {}
    ensured_paths: list = []

    monkeypatch.setattr("pyvider.cli.utils.Path.home", lambda: tmp_path)
    monkeypatch.setattr("pyvider.cli.utils.Path.cwd", lambda: tmp_path / "workspace")
    monkeypatch.setattr("pyvider.cli.utils.ensure_dir", lambda path: ensured_paths.append(path))
    monkeypatch.setattr("pyvider.cli.utils.pout", lambda message, **kwargs: outputs.append(message))
    monkeypatch.setattr("pyvider.cli.utils.timed_block", lambda: DummyTimer())

    def fake_atomic(path, content):
        log_capture["path"] = str(path)
        log_capture["content"] = content
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    monkeypatch.setattr("pyvider.cli.utils.atomic_write_text", fake_atomic)

    def fake_run_command(command, cwd, env, check):
        assert command == ["echo", "hi"]
        assert cwd == tmp_path / "workspace"
        return SimpleNamespace(stdout="done", stderr="", returncode=0)

    monkeypatch.setattr("pyvider.cli.utils.run_command", fake_run_command)

    result = _run_command(["echo", "hi"], title="Echo")

    assert result == "done"
    assert ensured_paths == [log_dir]
    assert outputs[0].startswith("⏳ Echo")
    assert any("✅ Done (0.50s)" in msg for msg in outputs)
    assert log_capture["path"] == str(log_dir / "prep.log")
    assert "Command: echo hi" in log_capture["content"]
    assert "Duration: 0.50s" in log_capture["content"]


def test_run_command_raises_on_failure(monkeypatch, tmp_path):
    (tmp_path / "workspace").mkdir()
    outputs: list[str] = []

    monkeypatch.setattr("pyvider.cli.utils.Path.home", lambda: tmp_path)
    monkeypatch.setattr("pyvider.cli.utils.Path.cwd", lambda: tmp_path / "workspace")
    monkeypatch.setattr("pyvider.cli.utils.ensure_dir", lambda path: None)
    monkeypatch.setattr("pyvider.cli.utils.atomic_write_text", lambda path, content: None)
    monkeypatch.setattr("pyvider.cli.utils.timed_block", lambda: DummyTimer())
    monkeypatch.setattr("pyvider.cli.utils.pout", lambda message, **kwargs: outputs.append(message))

    def fake_run_command(command, cwd, env, check):
        return SimpleNamespace(stdout="out", stderr="err", returncode=3)

    monkeypatch.setattr("pyvider.cli.utils.run_command", fake_run_command)

    with pytest.raises(ProcessError) as exc:
        _run_command(["false"], title="Fail")

    assert "exit code 3" in str(exc.value)
    assert outputs[0].startswith("⏳ Fail")
    assert any("❌ FAILED" in msg for msg in outputs)


def test_place_terraform_provider_script(monkeypatch, tmp_path):
    plugin_dir = tmp_path / "plugins"
    ctx = SimpleNamespace(tf_plugin_dir=plugin_dir)
    install_dir = tmp_path / "project"
    install_dir.mkdir()

    monkeypatch.setattr("pyvider.cli.utils.Path.cwd", lambda: install_dir)

    captured: dict[str, str] = {}

    def fake_atomic(path, content):
        captured["path"] = str(path)
        captured["content"] = content
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    monkeypatch.setattr("pyvider.cli.utils.atomic_write_text", fake_atomic)

    _place_terraform_provider_script(ctx)

    target_path = plugin_dir / "terraform-provider-pyvider"
    assert captured["path"] == str(target_path)
    assert target_path.exists()
    assert f"INSTALL_DIR=\"{install_dir}\"" in captured["content"]
    assert "exec pyvider \"$@\"" in captured["content"]

def test_run_command_allows_non_zero_when_check_disabled(monkeypatch, tmp_path):
    (tmp_path / "workspace").mkdir()
    monkeypatch.setattr("pyvider.cli.utils.Path.home", lambda: tmp_path)
    monkeypatch.setattr("pyvider.cli.utils.Path.cwd", lambda: tmp_path / "workspace")
    monkeypatch.setattr("pyvider.cli.utils.ensure_dir", lambda path: None)
    monkeypatch.setattr("pyvider.cli.utils.atomic_write_text", lambda path, content: None)
    monkeypatch.setattr("pyvider.cli.utils.timed_block", lambda: DummyTimer())
    monkeypatch.setattr("pyvider.cli.utils.pout", lambda *args, **kwargs: None)

    def fake_run_command(command, cwd, env, check):
        return SimpleNamespace(stdout="out", stderr="err", returncode=5)

    monkeypatch.setattr("pyvider.cli.utils.run_command", fake_run_command)

    result = _run_command(["cmd"], check=False)
    assert result == "out"

def test_run_command_logs_unexpected_exception(monkeypatch, tmp_path):
    (tmp_path / "workspace").mkdir()
    outputs: list[str] = []

    monkeypatch.setattr("pyvider.cli.utils.Path.home", lambda: tmp_path)
    monkeypatch.setattr("pyvider.cli.utils.Path.cwd", lambda: tmp_path / "workspace")
    monkeypatch.setattr("pyvider.cli.utils.ensure_dir", lambda path: None)
    monkeypatch.setattr("pyvider.cli.utils.atomic_write_text", lambda path, content: None)
    monkeypatch.setattr("pyvider.cli.utils.timed_block", lambda: DummyTimer())
    monkeypatch.setattr("pyvider.cli.utils.pout", lambda message, **kwargs: outputs.append(message))

    def failing_run_command(*_args, **_kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr("pyvider.cli.utils.run_command", failing_run_command)

    with pytest.raises(RuntimeError):
        _run_command(["explode"], title="Explode")

    assert any("❌ ERROR" in msg for msg in outputs)
    assert any("Failed to run command" in msg for msg in outputs)
