#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from pyvider.exceptions.foundation import (
    CapabilityError,
    ConfigurationError,
    DataSourceError,
    FunctionError,  # This is pyvider.exceptions.foundation.FunctionError
    InvalidTypeError,
    PyviderError,
    UnsupportedTypeError,
    ValueError as FoundationValueError,  # Alias to avoid conflict with builtin ValueError
)


class TestFoundationExceptions:
    def test_simple_foundation_exceptions(self) -> None:
        """Test simple exceptions from foundation.py for instantiation."""
        assert str(PyviderError("test")) == "test"
        assert str(CapabilityError("test")) == "test"
        assert str(FoundationValueError("test")) == "test"
        assert str(ConfigurationError("test")) == "test"
        assert str(DataSourceError("test")) == "test"
        assert str(FunctionError("test")) == "test"

    def test_invalid_type_error_init(self) -> None:
        err_default = InvalidTypeError()
        # Note: f-string curly braces must be doubled for the heredoc if this whole block
        # were inside an agent f-string. Here, it's a direct literal.
        assert str(err_default) == "Invalid type: expected 'unknown', got 'unknown'."

        err_custom = InvalidTypeError(expected_type="int", actual_type="str")
        assert str(err_custom) == "Invalid type: expected 'int', got 'str'."

    def test_unsupported_type_error_init(self) -> None:
        err_default = UnsupportedTypeError()
        assert str(err_default) == "Unsupported type encountered: 'unknown'."

        err_custom = UnsupportedTypeError(type_name="MyType")
        assert str(err_custom) == "Unsupported type encountered: 'MyType'."


# 🐍🏗️🔚
