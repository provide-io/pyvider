#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import pytest

from pyvider.proto.v6.tfplugin6_pb2 import Schema


@pytest.fixture
def sample_v6_proto() -> Schema:
    return Schema(description="Sample schema", version=6)


# 🐍🏗️🔚
