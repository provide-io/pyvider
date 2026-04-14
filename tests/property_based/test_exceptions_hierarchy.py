#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Any
import warnings

from hypothesis import HealthCheck, given, settings, strategies as st
import pytest

# Import the exceptions module itself to access its __all__ attribute
import pyvider.exceptions as pyvider_exceptions_module

# Helper to get all defined exceptions from the __all__ list
# Ensure pyvider.exceptions.__all__ is correctly populated and accessible
if not hasattr(pyvider_exceptions_module, "__all__") or not pyvider_exceptions_module.__all__:
    raise ImportError(
        "The pyvider.exceptions module does not define __all__ or it's empty. "
        "Cannot dynamically discover exceptions to test."
    )

ALL_PYVIDER_EXCEPTIONS = []
for exc_name_in_all in pyvider_exceptions_module.__all__:
    try:
        exc_class_from_module = getattr(pyvider_exceptions_module, exc_name_in_all)
        # Ensure it's actually an exception class (subclass of BaseException)
        # and not some other variable accidentally put into __all__
        if isinstance(exc_class_from_module, type) and issubclass(exc_class_from_module, BaseException):
            ALL_PYVIDER_EXCEPTIONS.append(exc_class_from_module)
        else:
            warnings.warn(
                f"'{exc_name_in_all}' from pyvider.exceptions.__all__ "
                f"is not an exception class (type: {type(exc_class_from_module).__name__}). Skipping.",
                UserWarning,
                stacklevel=2,
            )
    except AttributeError:
        warnings.warn(
            f"Could not find '{exc_name_in_all}' in pyvider.exceptions module as listed in __all__. Skipping.",
            UserWarning,
            stacklevel=2,
        )

if not ALL_PYVIDER_EXCEPTIONS:
    raise ImportError(
        "No valid exception classes were found from pyvider.exceptions.__all__. "
        "Please check the exceptions module and its __all__ definition."
    )


@pytest.mark.parametrize("exc_class", ALL_PYVIDER_EXCEPTIONS)
def test_exception_instantiation_and_str(exc_class: type[Exception]) -> None:
    """Tests basic instantiation and string conversion of all exceptions."""
    try:
        exceptions_with_specific_constructors = [
            pyvider_exceptions_module.InvalidTypeError,
            pyvider_exceptions_module.UnsupportedTypeError,
            pyvider_exceptions_module.SchemaValidationError,
            pyvider_exceptions_module.SerializationError,
            pyvider_exceptions_module.DeserializationError,
            pyvider_exceptions_module.ValidationError,
            pyvider_exceptions_module.AttributeValidationError,
            pyvider_exceptions_module.FunctionError,
            pyvider_exceptions_module.FunctionRegistrationError,
            pyvider_exceptions_module.FunctionValidationError,
            pyvider_exceptions_module.SchemaError,
            pyvider_exceptions_module.SchemaRegistrationError,
            pyvider_exceptions_module.SchemaParseError,
            pyvider_exceptions_module.SchemaConversionError,
        ]

        if exc_class in exceptions_with_specific_constructors:
            try:
                instance = exc_class()  # type: ignore
                assert (
                    exc_class.__name__ in str(instance)
                    or "PyviderError" in str(instance)
                    or "unknown" in str(instance)
                    or "error" in str(instance).lower()
                ), f"Default str representation for {exc_class.__name__} seems off: {instance!s}"
            except TypeError:
                pass  # Covered by specific hypothesis tests
            except AttributeError:
                pass  # Covered by specific hypothesis tests
        else:
            instance = exc_class("Test message for " + exc_class.__name__)
            assert "Test message for " + exc_class.__name__ in str(instance)
            # Some exceptions now inherit from foundation errors instead of PyviderError
            from provide.foundation.errors import FoundationError

            assert isinstance(instance, (pyvider_exceptions_module.PyviderError, FoundationError))
            assert isinstance(instance, Exception)
    except TypeError as e:
        print(f"Note: {exc_class.__name__} could not be instantiated generically for str test: {e}")


@given(st.text(min_size=1, max_size=100))
def test_pyvider_error_with_message(message: str) -> None:
    err = pyvider_exceptions_module.PyviderError(message)
    assert str(err) == message


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(
    message=st.text(),
    source_val=st.one_of(st.integers(), st.text(), st.none()),
    target_type_val=st.one_of(st.just(int), st.just(str), st.none()),
)
def test_conversion_error(message: str, source_val: Any, target_type_val: type[Any] | None) -> None:
    err = pyvider_exceptions_module.ConversionError(
        message, source_value=source_val, target_type=target_type_val
    )
    assert message in str(err)
    assert err.source_value == source_val
    assert err.target_type == target_type_val
    if source_val is not None:
        assert f"source_type={type(source_val).__name__}" in str(err)
    if target_type_val is not None:
        assert (
            f"target_type={target_type_val.__name__ if hasattr(target_type_val, '__name__') else str(target_type_val)}"
            in str(err)
        )


@given(st.text())
def test_framework_configuration_error(message: str) -> None:
    err = pyvider_exceptions_module.FrameworkConfigurationError(message)
    assert str(err) == message


@given(st.text())
def test_plugin_error(message: str) -> None:
    err = pyvider_exceptions_module.PluginError(message)
    assert str(err) == message


@given(st.text())
def test_pyvider_value_error(message: str) -> None:
    err = pyvider_exceptions_module.PyviderValueError(message)
    assert str(err) == message


@given(expected=st.text(min_size=1), actual=st.text(min_size=1))
def test_invalid_type_error(expected: str, actual: str) -> None:
    err = pyvider_exceptions_module.InvalidTypeError(expected_type=expected, actual_type=actual)
    assert f"Invalid type: expected '{expected}', got '{actual}'." == str(err)
    err_override = pyvider_exceptions_module.InvalidTypeError(message_override="Custom message")
    assert str(err_override) == "Custom message"


@given(type_name=st.text(min_size=1))
def test_unsupported_type_error(type_name: str) -> None:
    err = pyvider_exceptions_module.UnsupportedTypeError(type_name=type_name)
    assert f"Unsupported type encountered: '{type_name}'." == str(err)
    err_override = pyvider_exceptions_module.UnsupportedTypeError(message_override="Custom message")
    assert str(err_override) == "Custom message"


@given(st.text())
def test_component_configuration_error(message: str) -> None:
    err = pyvider_exceptions_module.ComponentConfigurationError(message)
    assert str(err) == message


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(
    message=st.text(),
    func_name=st.one_of(st.none(), st.text(min_size=1)),
    arg_idx=st.one_of(st.none(), st.integers(min_value=0)),
)
def test_function_error(message: str, func_name: str | None, arg_idx: int | None) -> None:
    err = pyvider_exceptions_module.FunctionError(message, function_name=func_name, argument_index=arg_idx)
    expected_prefix = f"Function '{func_name}'" if func_name else "Function"
    assert str(err) == f"{expected_prefix} error: {message}"
    assert err.function_name == func_name
    assert err.argument_index == arg_idx
    proto_like = err.to_proto()
    assert proto_like["text"] == str(err)
    assert proto_like["argument_index"] == arg_idx


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(message=st.text(), func_name=st.one_of(st.none(), st.text(min_size=1)))
def test_function_registration_error(message: str, func_name: str | None) -> None:
    err = pyvider_exceptions_module.FunctionRegistrationError(message, function_name=func_name)
    expected_prefix = f"Function '{func_name}'" if func_name else "Function"
    assert str(err) == f"{expected_prefix} registration error: {message}"


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(
    message=st.text(),
    func_name=st.one_of(st.none(), st.text(min_size=1)),
    arg_name=st.one_of(st.none(), st.text(min_size=1)),
    arg_idx=st.one_of(st.none(), st.integers(min_value=0)),
)
def test_function_validation_error(
    message: str, func_name: str | None, arg_name: str | None, arg_idx: int | None
) -> None:
    err = pyvider_exceptions_module.FunctionValidationError(
        message, function_name=func_name, argument_name=arg_name, argument_index=arg_idx
    )
    base_message_part = message
    if arg_name and func_name:
        assert (
            str(err)
            == f"Function '{func_name}' validation error for argument '{arg_name}': {base_message_part}"
        )
    elif arg_name:
        assert str(err) == f"Argument '{arg_name}' validation error: {base_message_part}"
    else:
        expected_prefix = f"Function '{func_name}'" if func_name else "Function"
        assert str(err) == f"{expected_prefix} validation error: {base_message_part}"


@given(st.text())
def test_grpc_error(message: str) -> None:
    assert str(pyvider_exceptions_module.GRPCError(message)) == message
    assert str(pyvider_exceptions_module.GRPCConnectionError(message)) == message
    assert str(pyvider_exceptions_module.NetworkError(message)) == message
    assert str(pyvider_exceptions_module.RateLimitError(message)) == message


@given(st.text())
def test_provider_error(message: str) -> None:
    assert str(pyvider_exceptions_module.ProviderError(message)) == message
    assert str(pyvider_exceptions_module.ProviderConfigurationError(message)) == message
    assert str(pyvider_exceptions_module.ProviderInitializationError(message)) == message


@given(st.text())
def test_registry_error(message: str) -> None:
    assert str(pyvider_exceptions_module.ComponentRegistryError(message)) == message
    assert str(pyvider_exceptions_module.ValidatorRegistrationError(message)) == message


@given(st.text())
def test_resource_error(message: str) -> None:
    assert str(pyvider_exceptions_module.ResourceError(message)) == message
    assert str(pyvider_exceptions_module.DataSourceError(message)) == message
    assert str(pyvider_exceptions_module.CapabilityError(message)) == message
    assert str(pyvider_exceptions_module.ResourceValidationError(message)) == message
    assert str(pyvider_exceptions_module.ResourceNotFoundError(message)) == message
    assert str(pyvider_exceptions_module.ResourceOperationError(message)) == message


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(message=st.text(), schema_name=st.one_of(st.none(), st.text(min_size=1)))
def test_schema_error(message: str, schema_name: str | None) -> None:
    err = pyvider_exceptions_module.SchemaError(message, schema_name=schema_name)
    expected_prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
    assert str(err) == f"{expected_prefix} error: {message}"


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(
    message=st.text(),
    schema_name=st.one_of(st.none(), st.text(min_size=1)),
    detail=st.one_of(st.none(), st.text()),
)
def test_schema_validation_error(message: str, schema_name: str | None, detail: str | None) -> None:
    err = pyvider_exceptions_module.SchemaValidationError(message, schema_name=schema_name, detail=detail)
    # The constructor for SchemaValidationError in schema.py now builds the full message.
    assert message in str(err)
    if detail:
        assert detail in str(err)
    if schema_name:
        assert f"Schema '{schema_name}'" in str(err)


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(message=st.text(), schema_name=st.one_of(st.none(), st.text(min_size=1)))
def test_schema_registration_error(message: str, schema_name: str | None) -> None:
    err = pyvider_exceptions_module.SchemaRegistrationError(message, schema_name=schema_name)
    expected_prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
    assert str(err) == f"{expected_prefix} registration error: {message}"


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(message=st.text(), schema_name=st.one_of(st.none(), st.text(min_size=1)))
def test_schema_parse_error(message: str, schema_name: str | None) -> None:
    err = pyvider_exceptions_module.SchemaParseError(message, schema_name=schema_name)
    expected_prefix = f"Schema '{schema_name}'" if schema_name else "Schema"
    assert str(err) == f"{expected_prefix} parse error: {message}"


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(
    message=st.text(),
    schema_name=st.one_of(st.none(), st.text(min_size=1)),
    source_val=st.text(),
    target_type_val=st.just(int),
)
def test_schema_conversion_error(
    message: str, schema_name: str | None, source_val: Any, target_type_val: type[Any]
) -> None:
    err = pyvider_exceptions_module.SchemaConversionError(
        message, schema_name=schema_name, source_value=source_val, target_type=target_type_val
    )
    base_message = message
    if schema_name:
        assert f"Schema '{schema_name}' conversion failed: {base_message}" in str(err)
    else:
        assert base_message in str(err)
    assert f"source_type={type(source_val).__name__}" in str(err)
    assert "target_type=int" in str(err)


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(
    message=st.text(),
    type_name=st.one_of(st.none(), st.text(min_size=1)),
    source_val=st.one_of(st.none(), st.text(), st.integers()),
    detail=st.one_of(st.none(), st.text()),
)
def test_serialization_error(message: str, type_name: str | None, source_val: Any, detail: str | None) -> None:
    err = pyvider_exceptions_module.SerializationError(
        message, type_name=type_name, source_value=source_val, detail=detail
    )
    expected_type_name_in_msg = type_name or "unknown"
    base_constructed_message = f"Serialization failed for type '{expected_type_name_in_msg}': {message}"
    if detail:
        base_constructed_message += f" - Detail: {detail}"

    expected_context_parts = []
    if source_val is not None:
        expected_context_parts.append(f"source_type={type(source_val).__name__}")
    if type_name is not None:
        expected_context_parts.append(f"target_type={type_name}")

    expected_full_message = base_constructed_message
    if expected_context_parts:
        expected_full_message += f" ({', '.join(expected_context_parts)})"

    assert str(err) == expected_full_message
    assert err.type_name == type_name
    assert err.detail == detail
    assert err.source_value == source_val
    assert err.target_type == type_name


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(
    message=st.text(),
    type_name=st.one_of(st.none(), st.text(min_size=1)),
    source_val=st.one_of(st.none(), st.text(), st.integers()),
    detail=st.one_of(st.none(), st.text()),
)
def test_deserialization_error(
    message: str, type_name: str | None, source_val: Any, detail: str | None
) -> None:
    err = pyvider_exceptions_module.DeserializationError(
        message, type_name=type_name, source_value=source_val, detail=detail
    )
    expected_type_name_in_msg = type_name or "unknown"
    base_constructed_message = f"Deserialization failed for type '{expected_type_name_in_msg}': {message}"
    if detail:
        base_constructed_message += f" - Detail: {detail}"

    expected_context_parts = []
    if source_val is not None:
        expected_context_parts.append(f"source_type={type(source_val).__name__}")
    if type_name is not None:
        expected_context_parts.append(f"target_type={type_name}")

    expected_full_message = base_constructed_message
    if expected_context_parts:
        expected_full_message += f" ({', '.join(expected_context_parts)})"

    assert str(err) == expected_full_message
    assert err.type_name == type_name
    assert err.detail == detail
    assert err.source_value == source_val
    assert err.target_type == type_name


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(
    message=st.text(),
    context=st.one_of(st.none(), st.text(min_size=1)),
    detail=st.one_of(st.none(), st.text()),
)
def test_validation_error(message: str, context: str | None, detail: str | None) -> None:
    err = pyvider_exceptions_module.ValidationError(message, context=context, detail=detail)
    expected_context_str = f"Context: {context} - " if context else ""
    expected_detail_str = f" - Detail: {detail}" if detail else ""
    assert str(err) == f"{expected_context_str}{message}{expected_detail_str}"


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(
    message=st.text(),
    attr_name=st.text(min_size=1),
    context=st.one_of(st.none(), st.text(min_size=1)),
    detail=st.one_of(st.none(), st.text()),
)
def test_attribute_validation_error(
    message: str, attr_name: str | None, context: str | None, detail: str | None
) -> None:
    err = pyvider_exceptions_module.AttributeValidationError(
        message, attribute_name=attr_name, context=context, detail=detail
    )
    base_message = f"Attribute '{attr_name}' validation failed: {message}"
    expected_context_str = f"Context: {context} - " if context else ""
    expected_detail_str = f" - Detail: {detail}" if detail else ""
    assert str(err) == f"{expected_context_str}{base_message}{expected_detail_str}"


def test_inheritance_structure() -> None:
    assert issubclass(pyvider_exceptions_module.ConversionError, pyvider_exceptions_module.PyviderError)
    assert issubclass(
        pyvider_exceptions_module.FrameworkConfigurationError, pyvider_exceptions_module.PyviderError
    )
    assert issubclass(pyvider_exceptions_module.PluginError, pyvider_exceptions_module.PyviderError)
    assert issubclass(pyvider_exceptions_module.PyviderValueError, pyvider_exceptions_module.PyviderError)
    assert issubclass(pyvider_exceptions_module.InvalidTypeError, pyvider_exceptions_module.PyviderValueError)
    assert issubclass(
        pyvider_exceptions_module.UnsupportedTypeError, pyvider_exceptions_module.PyviderValueError
    )
    assert issubclass(
        pyvider_exceptions_module.ComponentConfigurationError,
        pyvider_exceptions_module.FrameworkConfigurationError,
    )

    assert issubclass(pyvider_exceptions_module.GRPCError, pyvider_exceptions_module.PluginError)
    assert issubclass(pyvider_exceptions_module.GRPCConnectionError, pyvider_exceptions_module.GRPCError)

    assert issubclass(
        pyvider_exceptions_module.ProviderConfigurationError, pyvider_exceptions_module.ProviderError
    )
    assert issubclass(
        pyvider_exceptions_module.ProviderConfigurationError,
        pyvider_exceptions_module.ComponentConfigurationError,
    )

    assert issubclass(pyvider_exceptions_module.ResourceError, pyvider_exceptions_module.PluginError)
    assert issubclass(pyvider_exceptions_module.DataSourceError, pyvider_exceptions_module.ResourceError)
    assert issubclass(pyvider_exceptions_module.CapabilityError, pyvider_exceptions_module.PluginError)
    assert issubclass(
        pyvider_exceptions_module.ResourceValidationError, pyvider_exceptions_module.ResourceError
    )
    assert issubclass(
        pyvider_exceptions_module.ResourceValidationError, pyvider_exceptions_module.PyviderValueError
    )
    # Resource exceptions inherit from foundation errors
    from provide.foundation.errors import (
        ConfigurationError as FoundationConfigurationError,
        NotFoundError as FoundationNotFoundError,
        RuntimeError as FoundationRuntimeError,
        ValidationError as FoundationValidationError,
    )

    assert issubclass(pyvider_exceptions_module.ResourceNotFoundError, FoundationNotFoundError)
    assert issubclass(pyvider_exceptions_module.ResourceOperationError, FoundationRuntimeError)

    assert issubclass(pyvider_exceptions_module.SchemaError, pyvider_exceptions_module.PyviderError)
    assert issubclass(pyvider_exceptions_module.SchemaValidationError, FoundationValidationError)
    assert issubclass(pyvider_exceptions_module.SchemaRegistrationError, FoundationConfigurationError)
    assert issubclass(pyvider_exceptions_module.SchemaParseError, FoundationValidationError)
    assert issubclass(
        pyvider_exceptions_module.SchemaConversionError, pyvider_exceptions_module.ConversionError
    )

    assert issubclass(pyvider_exceptions_module.SerializationError, pyvider_exceptions_module.ConversionError)
    assert issubclass(
        pyvider_exceptions_module.DeserializationError, pyvider_exceptions_module.ConversionError
    )

    assert issubclass(pyvider_exceptions_module.ValidationError, FoundationValidationError)
    assert issubclass(
        pyvider_exceptions_module.AttributeValidationError, pyvider_exceptions_module.ValidationError
    )


# 🐍🏗️🔚
