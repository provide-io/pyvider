#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from provide.foundation import logger

try:
    import importlib.util

    HAS_MSGPACK = importlib.util.find_spec("msgpack") is not None
    if HAS_MSGPACK:
        logger.info("📦 msgpack library loaded successfully.")
    else:
        logger.warning("⚠️ msgpack library not found. msgpack features will be unavailable.")
except Exception as e:
    HAS_MSGPACK = False
    logger.error(f"❌ Error checking msgpack availability: {e}")

# 🐍🏗️🔚
