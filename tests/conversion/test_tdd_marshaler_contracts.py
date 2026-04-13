#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from pyvider.conversion.marshaler import (
    _apply_schema_marks_iterative as _apply_schema_marks,
)
from pyvider.cty import CtyMark, CtyString
from pyvider.schema import a_str, s_resource


def test_apply_schema_marks_adds_sensitive_mark() -> None:
    """
    TDD Contract: Verifies that the marshalling process automatically
    adds a 'sensitive' mark to a value when the schema dictates it.
    """
    # GIVEN a schema with a sensitive attribute
    schema = s_resource({"api_key": a_str(sensitive=True)})

    # AND an unmarked CtyValue corresponding to that attribute
    unmarked_value = CtyString().validate("my-secret")
    assert not unmarked_value.has_mark(CtyMark("sensitive"))

    # WHEN the schema marks are applied
    # We test the internal helper function directly here
    marked_value = _apply_schema_marks(unmarked_value, schema.block.attributes["api_key"])

    # THEN the resulting value must have the sensitive mark
    assert marked_value.has_mark(CtyMark("sensitive"))


# 🐍🏗️🔚
