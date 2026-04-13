#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for BaseContext diagnostic helpers."""

from pyvider.common.context import BaseContext
from pyvider.protocols.tfprotov6 import protobuf as pb


def _step_value(step: pb.AttributePath.Step) -> str | int | None:
    if step.attribute_name:
        return step.attribute_name
    if step.element_key_string:
        return step.element_key_string
    if step.element_key_int is not None:
        return step.element_key_int
    return None


def test_add_error_and_warning_populates_diagnostics() -> None:
    ctx = BaseContext()

    ctx.add_error("Boom", "Critical failure")
    ctx.add_warning("Heads up", "Non-blocking issue")

    assert len(ctx.diagnostics) == 2
    error_diag, warning_diag = ctx.diagnostics

    assert error_diag.severity == pb.Diagnostic.ERROR
    assert error_diag.summary == "Boom"
    assert error_diag.detail == "Critical failure"
    assert list(error_diag.attribute.steps) == []

    assert warning_diag.severity == pb.Diagnostic.WARNING
    assert warning_diag.summary == "Heads up"
    assert warning_diag.detail == "Non-blocking issue"
    assert list(warning_diag.attribute.steps) == []


def test_attribute_diagnostics_attach_attribute_paths() -> None:
    ctx = BaseContext()

    ctx.add_attribute_error("settings[2]['name']", "Bad name", "Invalid value")
    ctx.add_attribute_warning("items[0].id", "Deprecated", "Use uuid instead")

    error_diag, warning_diag = ctx.diagnostics

    error_steps = [_step_value(step) for step in error_diag.attribute.steps]
    assert error_steps == ["settings", 2, "name"]
    assert error_diag.summary == "Bad name"
    assert error_diag.detail == "Invalid value"
    assert error_diag.severity == pb.Diagnostic.ERROR

    warning_steps = [_step_value(step) for step in warning_diag.attribute.steps]
    assert warning_steps == ["items", 0, "id"]
    assert warning_diag.summary == "Deprecated"
    assert warning_diag.severity == pb.Diagnostic.WARNING


def test_attribute_warning_with_dot_path() -> None:
    ctx = BaseContext()

    ctx.add_attribute_warning("config.value", "Heads up")

    (diag,) = ctx.diagnostics
    step_values = [_step_value(step) for step in diag.attribute.steps]
    assert step_values == ["config", "value"]
    assert diag.severity == pb.Diagnostic.WARNING


# 🐍🏗️🔚
