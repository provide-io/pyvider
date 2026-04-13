#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from typing import Never

import pytest

from pyvider.schema.exceptions import (
    PvsAttributeError,
    PvsBlockError,
    PvsSchemaDefinitionError,
    PvsValidationError,
    PyviderSchemaError,
    SchemaConversionError,
)


def test_pyvider_schema_error() -> Never:
    with pytest.raises(PyviderSchemaError):
        raise PyviderSchemaError("test error")


def test_schema_conversion_error() -> Never:
    with pytest.raises(SchemaConversionError):
        raise SchemaConversionError("test conversion error")


def test_schema_conversion_error_str() -> None:
    err = SchemaConversionError("test conversion error")
    assert str(err) == "test conversion error"

    err = SchemaConversionError("test conversion error", schema_name="my_schema")
    assert str(err) == "[Schema: my_schema] test conversion error"

    err = SchemaConversionError("test conversion error", detail="some detail")
    assert str(err) == "test conversion error (Detail: some detail)"

    err = SchemaConversionError("test conversion error", schema_name="my_schema", detail="some detail")
    assert str(err) == "[Schema: my_schema] test conversion error (Detail: some detail)"


def test_pvs_validation_error() -> Never:
    with pytest.raises(PvsValidationError):
        raise PvsValidationError("test validation error")


def test_pvs_schema_definition_error() -> Never:
    with pytest.raises(PvsSchemaDefinitionError):
        raise PvsSchemaDefinitionError("test schema definition error")


def test_pvs_attribute_error() -> Never:
    with pytest.raises(PvsAttributeError):
        raise PvsAttributeError("test attribute error")


def test_pvs_block_error() -> Never:
    with pytest.raises(PvsBlockError):
        raise PvsBlockError("test block error")


# 🐍🏗️🔚
