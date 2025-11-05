#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Modern encryption module for Pyvider private state management.

This module provides secure encryption/decryption for Terraform provider private state
using AES-256-GCM with HKDF key derivation. Features include:

- Random salt per encryption (prevents rainbow table attacks)
- Version byte for algorithm flexibility
- Thread-safe key caching
- No global mutable state
- Foundation error integration
- Comprehensive logging

Encryption format:
    1 byte (version) + 16 bytes (salt) + 12 bytes (nonce) + N bytes (ciphertext+tag)

Version 0x01: HKDF-SHA256 + AES-256-GCM"""

from __future__ import annotations

import os
import struct
import threading
from typing import Final

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from provide.foundation import logger
from provide.foundation.errors import ConfigurationError, resilient

from pyvider.common.config import PyviderConfig

# Constants
VERSION_CURRENT: Final[int] = 0x01
VERSION_BYTE_SIZE: Final[int] = 1
SALT_SIZE: Final[int] = 16  # 128-bit salt
NONCE_SIZE: Final[int] = 12  # 96-bit nonce for AES-GCM
KEY_SIZE: Final[int] = 32  # AES-256
HKDF_INFO: Final[bytes] = b"pyvider-private-state-v1"

# Error messages
ERROR_NO_SECRET: Final[str] = (
    "Private state shared secret not configured. "
    "Set PYVIDER_PRIVATE_STATE_SHARED_SECRET environment variable "
    "or define 'private_state_shared_secret' in pyvider.toml"
)
ERROR_INVALID_CIPHERTEXT: Final[str] = (
    "Invalid ciphertext format. Data may be corrupted or encrypted with wrong key."
)
ERROR_DECRYPTION_FAILED: Final[str] = (
    "Decryption failed. Verify the shared secret hasn't changed and data isn't corrupted."
)
ERROR_UNSUPPORTED_VERSION: Final[str] = "Unsupported encryption version: {version:#x}"
ERROR_TOO_SHORT: Final[str] = (
    "Ciphertext too short. Expected at least {min_size} bytes, got {actual_size} bytes."
)


class EncryptionError(Exception):
    """Raised when encryption/decryption operations fail."""

    pass


class EncryptionManager:
    """
    Thread-safe encryption manager for Pyvider private state.

    Manages key derivation, caching, and encryption/decryption operations
    without using global mutable state.
    """

    def __init__(self) -> None:
        """Initialize the encryption manager."""
        self._key_cache: dict[bytes, bytes] = {}
        self._lock = threading.Lock()
        logger.debug(
            "Encryption manager initialized",
            operation="encryption_init",
        )

    @resilient()
    def _get_shared_secret(self) -> str:
        """
        Retrieve the shared secret from configuration.

        Returns:
            The shared secret string

        Raises:
            ConfigurationError: If shared secret is not configured
        """
        config = PyviderConfig()

        try:
            config.validate_required_fields()
            secret = config.private_state_shared_secret
        except Exception as e:
            logger.error(
                "Failed to retrieve private state shared secret",
                error=str(e),
                exc_info=True,
            )
            raise ConfigurationError(ERROR_NO_SECRET) from e

        if not secret:
            logger.error("Private state shared secret is empty")
            raise ConfigurationError(ERROR_NO_SECRET)

        logger.debug("Retrieved shared secret from configuration")
        return secret

    def _derive_key(self, salt: bytes) -> bytes:
        """
        Derive encryption key using HKDF-SHA256.

        Args:
            salt: Random salt for key derivation

        Returns:
            32-byte encryption key

        Raises:
            ConfigurationError: If shared secret retrieval fails
        """
        # Check cache first (thread-safe)
        with self._lock:
            if salt in self._key_cache:
                logger.debug("Using cached encryption key", salt_hash=salt[:8].hex())
                return self._key_cache[salt]

        # Derive new key
        secret = self._get_shared_secret()
        key_material = secret.encode("utf-8")

        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=KEY_SIZE,
            salt=salt,
            info=HKDF_INFO,
        )
        derived_key = hkdf.derive(key_material)

        # Cache the key (thread-safe)
        with self._lock:
            self._key_cache[salt] = derived_key
            logger.debug(
                "Derived and cached new encryption key",
                salt_hash=salt[:8].hex(),
                cache_size=len(self._key_cache),
            )

        return derived_key

    @resilient()
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypt plaintext using AES-256-GCM with random salt and nonce.

        Args:
            plaintext: Data to encrypt

        Returns:
            Encrypted data with format: version + salt + nonce + ciphertext+tag

        Raises:
            ConfigurationError: If shared secret is not configured
            EncryptionError: If encryption fails
        """
        if not plaintext:
            logger.debug("Encrypting empty data, returning empty bytes")
            return b""

        try:
            # Generate random salt and nonce
            salt = os.urandom(SALT_SIZE)
            nonce = os.urandom(NONCE_SIZE)

            # Derive key with this salt
            key = self._derive_key(salt)

            # Encrypt
            aesgcm = AESGCM(key)
            ciphertext = aesgcm.encrypt(nonce, plaintext, None)

            # Pack: version + salt + nonce + ciphertext
            result = struct.pack("B", VERSION_CURRENT) + salt + nonce + ciphertext

            logger.debug(
                "Private state encrypted successfully",
                operation="encrypt",
                plaintext_size=len(plaintext),
                ciphertext_size=len(result),
                version=VERSION_CURRENT,
            )

            return result

        except ConfigurationError:
            # Re-raise configuration errors as-is
            raise
        except Exception as e:
            logger.error(
                "Private state encryption failed",
                operation="encrypt",
                error_type=type(e).__name__,
                error_message=str(e),
                plaintext_size=len(plaintext),
                exc_info=True,
            )
            raise EncryptionError(f"Encryption operation failed: {e}") from e

    @resilient()
    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypt ciphertext using AES-256-GCM.

        Args:
            ciphertext: Encrypted data with format: version + salt + nonce + ciphertext+tag

        Returns:
            Decrypted plaintext

        Raises:
            ConfigurationError: If shared secret is not configured
            EncryptionError: If decryption fails or format is invalid
        """
        if not ciphertext:
            logger.debug("Decrypting empty data, returning empty bytes")
            return b""

        # Validate minimum size
        min_size = VERSION_BYTE_SIZE + SALT_SIZE + NONCE_SIZE
        if len(ciphertext) < min_size:
            error_msg = ERROR_TOO_SHORT.format(min_size=min_size, actual_size=len(ciphertext))
            logger.error("Ciphertext too short", expected=min_size, actual=len(ciphertext))
            raise EncryptionError(error_msg)

        try:
            # Unpack components
            offset = 0

            # Version byte
            version = struct.unpack("B", ciphertext[offset : offset + VERSION_BYTE_SIZE])[0]
            offset += VERSION_BYTE_SIZE

            if version != VERSION_CURRENT:
                error_msg = ERROR_UNSUPPORTED_VERSION.format(version=version)
                logger.error("Unsupported encryption version", version=version, expected=VERSION_CURRENT)
                raise EncryptionError(error_msg)

            # Salt
            salt = ciphertext[offset : offset + SALT_SIZE]
            offset += SALT_SIZE

            # Nonce
            nonce = ciphertext[offset : offset + NONCE_SIZE]
            offset += NONCE_SIZE

            # Ciphertext (remainder)
            encrypted_data = ciphertext[offset:]

            # Derive key with the stored salt
            key = self._derive_key(salt)

            # Decrypt
            aesgcm = AESGCM(key)
            plaintext = aesgcm.decrypt(nonce, encrypted_data, None)

            logger.debug(
                "Decrypted data",
                ciphertext_size=len(ciphertext),
                plaintext_size=len(plaintext),
                version=version,
            )

            return plaintext

        except ConfigurationError:
            # Re-raise configuration errors as-is
            raise
        except EncryptionError:
            # Re-raise our own errors
            raise
        except Exception as e:
            logger.error(
                "Decryption failed",
                error=str(e),
                ciphertext_size=len(ciphertext),
                exc_info=True,
            )
            raise EncryptionError(ERROR_DECRYPTION_FAILED) from e

    def clear_cache(self) -> None:
        """Clear the key cache (useful for testing or key rotation)."""
        with self._lock:
            cache_size = len(self._key_cache)
            self._key_cache.clear()
            logger.info("Cleared encryption key cache", keys_cleared=cache_size)


# Module-level singleton instance
_manager: EncryptionManager | None = None
_manager_lock = threading.Lock()


def _get_manager() -> EncryptionManager:
    """Get or create the singleton encryption manager instance."""
    global _manager

    if _manager is not None:
        return _manager

    with _manager_lock:
        if _manager is None:
            _manager = EncryptionManager()
            logger.debug("Created singleton encryption manager")

        return _manager


# Public API - convenience functions that delegate to the singleton manager


def encrypt(plaintext: bytes) -> bytes:
    """
    Encrypt plaintext using AES-256-GCM.

    Args:
        plaintext: Data to encrypt

    Returns:
        Encrypted data with version, salt, nonce, and ciphertext

    Raises:
        ConfigurationError: If shared secret is not configured
        EncryptionError: If encryption fails
    """
    return _get_manager().encrypt(plaintext)


def decrypt(ciphertext: bytes) -> bytes:
    """
    Decrypt ciphertext using AES-256-GCM.

    Args:
        ciphertext: Encrypted data

    Returns:
        Decrypted plaintext

    Raises:
        ConfigurationError: If shared secret is not configured
        EncryptionError: If decryption fails or format is invalid
    """
    return _get_manager().decrypt(ciphertext)


def clear_encryption_cache() -> None:
    """Clear the encryption key cache (useful for testing or key rotation)."""
    _get_manager().clear_cache()


def reset_encryption_manager() -> None:
    """Reset the singleton manager (for testing only)."""
    global _manager
    with _manager_lock:
        _manager = None
        logger.debug("Reset encryption manager singleton")


# Legacy compatibility (for CONFIG_KEY_NAME used in tests)
CONFIG_KEY_NAME = "private_state_shared_secret"

# 🐍🏗️🔚
