#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import define, field

if TYPE_CHECKING:
    import pyvider.protocols.tfprotov6.protobuf as pb


@define
class BaseContext:
    """A base context providing a universal diagnostics API."""

    diagnostics: list[pb.Diagnostic] = field(factory=list, init=False)

    @property
    def stop_requested(self) -> bool:
        """Whether Terraform has asked the provider to stop.

        Terraform's Stop is advisory: it asks in-flight work to wind up and then
        waits for it to return (internal/providers/provider.go:63-73). A resource
        doing something long-running -- polling an API, waiting for a machine to
        boot -- should check this between steps and return early, so an
        interrupted `terraform apply` ends with the resource accounted for
        instead of being cut off mid-call.
        """
        from pyvider.common.stop_signal import is_stop_requested

        return is_stop_requested()

    def _add_diagnostic(
        self,
        severity: pb.Diagnostic.Severity,
        summary: str,
        detail: str = "",
        path: str | None = None,
    ) -> None:
        """Internal helper to create and append a diagnostic."""
        from pyvider.protocols.tfprotov6 import protobuf as pb
        from pyvider.protocols.tfprotov6.handlers.utils import str_path_to_proto_path

        proto_path = str_path_to_proto_path(path) if path else None
        diag = pb.Diagnostic(
            severity=severity,
            summary=summary,
            detail=detail,
            attribute=proto_path,
        )
        self.diagnostics.append(diag)

    def add_error(
        self,
        summary: str,
        detail: str = "",
    ) -> None:
        """
        Adds a generic error diagnostic to the current operation.
        This will cause Terraform to fail the operation.
        """
        from pyvider.protocols.tfprotov6 import protobuf as pb

        self._add_diagnostic(pb.Diagnostic.ERROR, summary, detail)

    def add_warning(
        self,
        summary: str,
        detail: str = "",
    ) -> None:
        """
        Adds a generic warning diagnostic to the current operation.
        This will be displayed to the user but will not fail the operation.
        """
        from pyvider.protocols.tfprotov6 import protobuf as pb

        self._add_diagnostic(pb.Diagnostic.WARNING, summary, detail)

    def add_attribute_error(
        self,
        attribute_path: str,
        summary: str,
        detail: str = "",
    ) -> None:
        """
        Adds an error diagnostic that is specific to a particular attribute.
        This is the preferred way to report validation errors for a single field.
        """
        from pyvider.protocols.tfprotov6 import protobuf as pb

        self._add_diagnostic(pb.Diagnostic.ERROR, summary, detail, path=attribute_path)

    def add_attribute_warning(
        self,
        attribute_path: str,
        summary: str,
        detail: str = "",
    ) -> None:
        """
        Adds a warning diagnostic that is specific to a particular attribute.
        This is the preferred way to report non-blocking issues like deprecations.
        """
        from pyvider.protocols.tfprotov6 import protobuf as pb

        self._add_diagnostic(pb.Diagnostic.WARNING, summary, detail, path=attribute_path)


# 🐍🏗️🔚
