#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tunable defaults for pluggable state-store backends.

Every configurable value used by the state-store subsystem lives here so that
backends, the manager, and the protocol handlers share one source of truth
instead of scattering literals across call sites.
"""

from __future__ import annotations

from typing import Final

# Wire chunking. Terraform negotiates a chunk size during ConfigureStateStore;
# this value is used when the client does not supply one.
# Core proposes this size and validates what comes back, so the two constants
# are its, not ours: `chunks.DefaultStateStoreChunkSize` is 8 MB and
# `chunks.MaxStateStoreChunkSize` is 128 MB, above which Core refuses to
# negotiate at all ("Failed to negotiate acceptable chunk size").
DEFAULT_STATE_STORE_CHUNK_SIZE: Final[int] = 8 << 20  # 8 MB
MAX_STATE_STORE_CHUNK_SIZE: Final[int] = 128 << 20  # 128 MB

# Lease duration for a state lock, in seconds. Zero means no expiry: the lock is
# held until it is explicitly unlocked.
#
# Terraform acquires a state lock once per operation and releases it with
# UnlockState when the operation ends. Nothing renews it in between -- the
# pluggable state store client sends Lock and Unlock and no third thing
# (terraform/internal/states/remote/remote_grpc.go:122-130), and there is no TTL
# anywhere under internal/states or internal/backend/pluggable. So a lease that
# lapses on its own is a lock that can be taken out from under a running apply,
# and the holder's own UnlockState is then refused because the lock id no longer
# matches.
#
# This defaulted to five minutes, which is shorter than an ordinary apply. The
# stale-lock problem it was guarding against is the one every Terraform backend
# has, and it has a standard answer: `terraform force-unlock <ID>`, which arrives
# here as UnlockState with that id. Expiry remains available for an operator who
# decides they want it, via PYVIDER_STATE_STORE_LOCK_TTL or an explicit
# ttl_seconds, and it warns when used.
DEFAULT_LOCK_TTL_SECONDS: Final[float] = 0.0

# Backend identifiers understood by the manager.
BACKEND_MEMORY: Final[str] = "memory"
BACKEND_FILESYSTEM: Final[str] = "filesystem"
DEFAULT_BACKEND: Final[str] = BACKEND_MEMORY

# Environment overrides.
ENV_BACKEND: Final[str] = "PYVIDER_STATE_STORE_BACKEND"
ENV_PATH: Final[str] = "PYVIDER_STATE_STORE_PATH"
ENV_LOCK_TTL: Final[str] = "PYVIDER_STATE_STORE_LOCK_TTL"

# Filesystem backend layout, relative to the working directory when
# ``PYVIDER_STATE_STORE_PATH`` is unset.
DEFAULT_STATE_ROOT_DIRNAME: Final[str] = ".pyvider"
DEFAULT_STATE_SUBDIRNAME: Final[str] = "state"

STATE_FILE_SUFFIX: Final[str] = ".tfstate"
LOCK_FILE_SUFFIX: Final[str] = ".tflock"
TEMP_FILE_SUFFIX: Final[str] = ".tmp"

# Directory and file permissions. State payloads routinely contain credentials,
# so they are owner-only.
STATE_DIR_MODE: Final[int] = 0o700
STATE_FILE_MODE: Final[int] = 0o600

# 🐍🏗️🔚
