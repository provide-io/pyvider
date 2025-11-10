#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from provide.foundation.utils.versioning import get_version

__path__ = __import__("pkgutil").extend_path(__path__, __name__)

__version__ = get_version("pyvider", caller_file=__file__)

__all__ = [
    "__version__",
]

# 🐍🏗️🔚
