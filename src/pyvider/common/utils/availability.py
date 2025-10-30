#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Utility module for checking library availability."""

from provide.foundation import logger

try:
    import importlib.util

    HAS_MSGPACK = importlib.util.find_spec("msgpack") is not None
    if HAS_MSGPACK:
        logger.debug("✅ msgpack library is available")
    else:
        logger.warning("⚠️ msgpack library not found. msgpack features will be unavailable.")
except Exception as e:
    HAS_MSGPACK = False
    logger.error(f"❌ Error checking msgpack availability: {e}")

# 🐍🏗️🔚
