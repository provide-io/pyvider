#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Public test-support helpers for pyvider resource authors.

Exposes checks a resource author can run in their own test suite, to catch
mistakes at test time rather than during a real ``terraform apply``. This is
the dev-time complement to the runtime completeness check in
``protocols.tfprotov6.handlers.utils.complete_state_dict``: that function
raises ``IncompleteResourceStateError`` when a resource's returned state is
missing a schema attribute; this module lets a resource author catch the
same mismatch statically, against the class, before ever running the
resource.
"""

from pyvider.testing.schema_completeness import (
    assert_schema_state_parity,
    find_missing_state_fields,
)

__all__ = [
    "assert_schema_state_parity",
    "find_missing_state_fields",
]

# 🐍🏗️🔚
