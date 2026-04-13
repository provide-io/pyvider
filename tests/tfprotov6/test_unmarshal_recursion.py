#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from pathlib import Path

import pytest

from pyvider.conversion import unmarshal_value
from pyvider.cty import CtyDynamic
import pyvider.protocols.tfprotov6.protobuf as pb

# Path to the dumped data that causes the crash.
# This makes the test a perfect replication of the real-world failure.
DEBUG_DUMP_FILE = Path("/tmp/pyvider_debug_dump.msgpack")


@pytest.mark.skipif(not DEBUG_DUMP_FILE.exists(), reason="Debug dump file not found")
@pytest.mark.asyncio
async def test_unmarshal_captured_payload_avoids_recursion() -> None:
    """
    This test reads the captured failing payload and attempts to unmarshal it,
    which will trigger the RecursionError with the broken code.
    """
    # 1. Read the raw msgpack data from the captured file.
    packed_data = DEBUG_DUMP_FILE.read_bytes()
    dynamic_value_in = pb.DynamicValue(msgpack=packed_data)

    # 2. The target schema is dynamic, as it is for an `Any` type-hinted function arg.
    target_schema = CtyDynamic()

    # 3. Call the unmarshal function, which is the site of the recursion.
    try:
        result_cty_val = unmarshal_value(dynamic_value_in, target_schema)
        assert result_cty_val is not None, "Unmarshalling returned None"
        assert not result_cty_val.is_null, "Unmarshalled value should not be null"
    except RecursionError:
        pytest.fail("unmarshal_value caused a RecursionError with the captured payload.")


# 🐍🏗️🔚
