"""
Modern encryption module for Pyvider private state management.

This module provides secure encryption/decryption for Terraform provider private state
using AES-256-GCM with HKDF key derivation. Features include:

- Random salt per encryption (prevents rainbow table attacks)
- Version byte for algorithm flexibility
- Thread-safe key caching
- No global mutable state
- Foundation error integration
- Comprehensive logging

Encryption format:
    [1 byte: version][16 bytes: salt][12 bytes: nonce][N bytes: ciphertext+tag]

Version 0x01: HKDF-SHA256 + AES-256-GCM
"""

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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class EncryptionError(Exception):
    """Raised when encryption/decryption operations fail."""

    pass


class EncryptionManager:
    """
    Thread-safe encryption manager for Pyvider private state.

    Manages key derivation, caching, and encryption/decryption operations
    without using global mutable state.
    """

    def xǁEncryptionManagerǁ__init____mutmut_orig(self) -> None:
        """Initialize the encryption manager."""
        self._key_cache: dict[bytes, bytes] = {}
        self._lock = threading.Lock()
        logger.debug("Encryption manager initialized")

    def xǁEncryptionManagerǁ__init____mutmut_1(self) -> None:
        """Initialize the encryption manager."""
        self._key_cache: dict[bytes, bytes] = None
        self._lock = threading.Lock()
        logger.debug("Encryption manager initialized")

    def xǁEncryptionManagerǁ__init____mutmut_2(self) -> None:
        """Initialize the encryption manager."""
        self._key_cache: dict[bytes, bytes] = {}
        self._lock = None
        logger.debug("Encryption manager initialized")

    def xǁEncryptionManagerǁ__init____mutmut_3(self) -> None:
        """Initialize the encryption manager."""
        self._key_cache: dict[bytes, bytes] = {}
        self._lock = threading.Lock()
        logger.debug(None)

    def xǁEncryptionManagerǁ__init____mutmut_4(self) -> None:
        """Initialize the encryption manager."""
        self._key_cache: dict[bytes, bytes] = {}
        self._lock = threading.Lock()
        logger.debug("XXEncryption manager initializedXX")

    def xǁEncryptionManagerǁ__init____mutmut_5(self) -> None:
        """Initialize the encryption manager."""
        self._key_cache: dict[bytes, bytes] = {}
        self._lock = threading.Lock()
        logger.debug("encryption manager initialized")

    def xǁEncryptionManagerǁ__init____mutmut_6(self) -> None:
        """Initialize the encryption manager."""
        self._key_cache: dict[bytes, bytes] = {}
        self._lock = threading.Lock()
        logger.debug("ENCRYPTION MANAGER INITIALIZED")
    
    xǁEncryptionManagerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEncryptionManagerǁ__init____mutmut_1': xǁEncryptionManagerǁ__init____mutmut_1, 
        'xǁEncryptionManagerǁ__init____mutmut_2': xǁEncryptionManagerǁ__init____mutmut_2, 
        'xǁEncryptionManagerǁ__init____mutmut_3': xǁEncryptionManagerǁ__init____mutmut_3, 
        'xǁEncryptionManagerǁ__init____mutmut_4': xǁEncryptionManagerǁ__init____mutmut_4, 
        'xǁEncryptionManagerǁ__init____mutmut_5': xǁEncryptionManagerǁ__init____mutmut_5, 
        'xǁEncryptionManagerǁ__init____mutmut_6': xǁEncryptionManagerǁ__init____mutmut_6
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEncryptionManagerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁEncryptionManagerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁEncryptionManagerǁ__init____mutmut_orig)
    xǁEncryptionManagerǁ__init____mutmut_orig.__name__ = 'xǁEncryptionManagerǁ__init__'

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

    def xǁEncryptionManagerǁ_derive_key__mutmut_orig(self, salt: bytes) -> bytes:
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_1(self, salt: bytes) -> bytes:
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
            if salt not in self._key_cache:
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_2(self, salt: bytes) -> bytes:
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
                logger.debug(None, salt_hash=salt[:8].hex())
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_3(self, salt: bytes) -> bytes:
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
                logger.debug("Using cached encryption key", salt_hash=None)
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_4(self, salt: bytes) -> bytes:
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
                logger.debug(salt_hash=salt[:8].hex())
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_5(self, salt: bytes) -> bytes:
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
                logger.debug("Using cached encryption key", )
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_6(self, salt: bytes) -> bytes:
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
                logger.debug("XXUsing cached encryption keyXX", salt_hash=salt[:8].hex())
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_7(self, salt: bytes) -> bytes:
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
                logger.debug("using cached encryption key", salt_hash=salt[:8].hex())
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_8(self, salt: bytes) -> bytes:
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
                logger.debug("USING CACHED ENCRYPTION KEY", salt_hash=salt[:8].hex())
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_9(self, salt: bytes) -> bytes:
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
                logger.debug("Using cached encryption key", salt_hash=salt[:9].hex())
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_10(self, salt: bytes) -> bytes:
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
        secret = None
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_11(self, salt: bytes) -> bytes:
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
        key_material = None

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

    def xǁEncryptionManagerǁ_derive_key__mutmut_12(self, salt: bytes) -> bytes:
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
        key_material = secret.encode(None)

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

    def xǁEncryptionManagerǁ_derive_key__mutmut_13(self, salt: bytes) -> bytes:
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
        key_material = secret.encode("XXutf-8XX")

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

    def xǁEncryptionManagerǁ_derive_key__mutmut_14(self, salt: bytes) -> bytes:
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
        key_material = secret.encode("UTF-8")

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

    def xǁEncryptionManagerǁ_derive_key__mutmut_15(self, salt: bytes) -> bytes:
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

        hkdf = None
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_16(self, salt: bytes) -> bytes:
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
            algorithm=None,
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_17(self, salt: bytes) -> bytes:
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
            length=None,
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_18(self, salt: bytes) -> bytes:
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
            salt=None,
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_19(self, salt: bytes) -> bytes:
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
            info=None,
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_20(self, salt: bytes) -> bytes:
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_21(self, salt: bytes) -> bytes:
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_22(self, salt: bytes) -> bytes:
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_23(self, salt: bytes) -> bytes:
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

    def xǁEncryptionManagerǁ_derive_key__mutmut_24(self, salt: bytes) -> bytes:
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
        derived_key = None

        # Cache the key (thread-safe)
        with self._lock:
            self._key_cache[salt] = derived_key
            logger.debug(
                "Derived and cached new encryption key",
                salt_hash=salt[:8].hex(),
                cache_size=len(self._key_cache),
            )

        return derived_key

    def xǁEncryptionManagerǁ_derive_key__mutmut_25(self, salt: bytes) -> bytes:
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
        derived_key = hkdf.derive(None)

        # Cache the key (thread-safe)
        with self._lock:
            self._key_cache[salt] = derived_key
            logger.debug(
                "Derived and cached new encryption key",
                salt_hash=salt[:8].hex(),
                cache_size=len(self._key_cache),
            )

        return derived_key

    def xǁEncryptionManagerǁ_derive_key__mutmut_26(self, salt: bytes) -> bytes:
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
            self._key_cache[salt] = None
            logger.debug(
                "Derived and cached new encryption key",
                salt_hash=salt[:8].hex(),
                cache_size=len(self._key_cache),
            )

        return derived_key

    def xǁEncryptionManagerǁ_derive_key__mutmut_27(self, salt: bytes) -> bytes:
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
                None,
                salt_hash=salt[:8].hex(),
                cache_size=len(self._key_cache),
            )

        return derived_key

    def xǁEncryptionManagerǁ_derive_key__mutmut_28(self, salt: bytes) -> bytes:
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
                salt_hash=None,
                cache_size=len(self._key_cache),
            )

        return derived_key

    def xǁEncryptionManagerǁ_derive_key__mutmut_29(self, salt: bytes) -> bytes:
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
                cache_size=None,
            )

        return derived_key

    def xǁEncryptionManagerǁ_derive_key__mutmut_30(self, salt: bytes) -> bytes:
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
                salt_hash=salt[:8].hex(),
                cache_size=len(self._key_cache),
            )

        return derived_key

    def xǁEncryptionManagerǁ_derive_key__mutmut_31(self, salt: bytes) -> bytes:
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
                cache_size=len(self._key_cache),
            )

        return derived_key

    def xǁEncryptionManagerǁ_derive_key__mutmut_32(self, salt: bytes) -> bytes:
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
                )

        return derived_key

    def xǁEncryptionManagerǁ_derive_key__mutmut_33(self, salt: bytes) -> bytes:
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
                "XXDerived and cached new encryption keyXX",
                salt_hash=salt[:8].hex(),
                cache_size=len(self._key_cache),
            )

        return derived_key

    def xǁEncryptionManagerǁ_derive_key__mutmut_34(self, salt: bytes) -> bytes:
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
                "derived and cached new encryption key",
                salt_hash=salt[:8].hex(),
                cache_size=len(self._key_cache),
            )

        return derived_key

    def xǁEncryptionManagerǁ_derive_key__mutmut_35(self, salt: bytes) -> bytes:
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
                "DERIVED AND CACHED NEW ENCRYPTION KEY",
                salt_hash=salt[:8].hex(),
                cache_size=len(self._key_cache),
            )

        return derived_key

    def xǁEncryptionManagerǁ_derive_key__mutmut_36(self, salt: bytes) -> bytes:
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
                salt_hash=salt[:9].hex(),
                cache_size=len(self._key_cache),
            )

        return derived_key
    
    xǁEncryptionManagerǁ_derive_key__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEncryptionManagerǁ_derive_key__mutmut_1': xǁEncryptionManagerǁ_derive_key__mutmut_1, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_2': xǁEncryptionManagerǁ_derive_key__mutmut_2, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_3': xǁEncryptionManagerǁ_derive_key__mutmut_3, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_4': xǁEncryptionManagerǁ_derive_key__mutmut_4, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_5': xǁEncryptionManagerǁ_derive_key__mutmut_5, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_6': xǁEncryptionManagerǁ_derive_key__mutmut_6, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_7': xǁEncryptionManagerǁ_derive_key__mutmut_7, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_8': xǁEncryptionManagerǁ_derive_key__mutmut_8, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_9': xǁEncryptionManagerǁ_derive_key__mutmut_9, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_10': xǁEncryptionManagerǁ_derive_key__mutmut_10, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_11': xǁEncryptionManagerǁ_derive_key__mutmut_11, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_12': xǁEncryptionManagerǁ_derive_key__mutmut_12, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_13': xǁEncryptionManagerǁ_derive_key__mutmut_13, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_14': xǁEncryptionManagerǁ_derive_key__mutmut_14, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_15': xǁEncryptionManagerǁ_derive_key__mutmut_15, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_16': xǁEncryptionManagerǁ_derive_key__mutmut_16, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_17': xǁEncryptionManagerǁ_derive_key__mutmut_17, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_18': xǁEncryptionManagerǁ_derive_key__mutmut_18, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_19': xǁEncryptionManagerǁ_derive_key__mutmut_19, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_20': xǁEncryptionManagerǁ_derive_key__mutmut_20, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_21': xǁEncryptionManagerǁ_derive_key__mutmut_21, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_22': xǁEncryptionManagerǁ_derive_key__mutmut_22, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_23': xǁEncryptionManagerǁ_derive_key__mutmut_23, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_24': xǁEncryptionManagerǁ_derive_key__mutmut_24, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_25': xǁEncryptionManagerǁ_derive_key__mutmut_25, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_26': xǁEncryptionManagerǁ_derive_key__mutmut_26, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_27': xǁEncryptionManagerǁ_derive_key__mutmut_27, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_28': xǁEncryptionManagerǁ_derive_key__mutmut_28, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_29': xǁEncryptionManagerǁ_derive_key__mutmut_29, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_30': xǁEncryptionManagerǁ_derive_key__mutmut_30, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_31': xǁEncryptionManagerǁ_derive_key__mutmut_31, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_32': xǁEncryptionManagerǁ_derive_key__mutmut_32, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_33': xǁEncryptionManagerǁ_derive_key__mutmut_33, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_34': xǁEncryptionManagerǁ_derive_key__mutmut_34, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_35': xǁEncryptionManagerǁ_derive_key__mutmut_35, 
        'xǁEncryptionManagerǁ_derive_key__mutmut_36': xǁEncryptionManagerǁ_derive_key__mutmut_36
    }
    
    def _derive_key(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEncryptionManagerǁ_derive_key__mutmut_orig"), object.__getattribute__(self, "xǁEncryptionManagerǁ_derive_key__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _derive_key.__signature__ = _mutmut_signature(xǁEncryptionManagerǁ_derive_key__mutmut_orig)
    xǁEncryptionManagerǁ_derive_key__mutmut_orig.__name__ = 'xǁEncryptionManagerǁ_derive_key'

    @resilient()
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypt plaintext using AES-256-GCM with random salt and nonce.

        Args:
            plaintext: Data to encrypt

        Returns:
            Encrypted data with format: [version][salt][nonce][ciphertext+tag]

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
                "Encrypted data",
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
                "Encryption failed",
                error=str(e),
                plaintext_size=len(plaintext),
                exc_info=True,
            )
            raise EncryptionError(f"Encryption operation failed: {e}") from e

    @resilient()
    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypt ciphertext using AES-256-GCM.

        Args:
            ciphertext: Encrypted data with format: [version][salt][nonce][ciphertext+tag]

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

    def xǁEncryptionManagerǁclear_cache__mutmut_orig(self) -> None:
        """Clear the key cache (useful for testing or key rotation)."""
        with self._lock:
            cache_size = len(self._key_cache)
            self._key_cache.clear()
            logger.info("Cleared encryption key cache", keys_cleared=cache_size)

    def xǁEncryptionManagerǁclear_cache__mutmut_1(self) -> None:
        """Clear the key cache (useful for testing or key rotation)."""
        with self._lock:
            cache_size = None
            self._key_cache.clear()
            logger.info("Cleared encryption key cache", keys_cleared=cache_size)

    def xǁEncryptionManagerǁclear_cache__mutmut_2(self) -> None:
        """Clear the key cache (useful for testing or key rotation)."""
        with self._lock:
            cache_size = len(self._key_cache)
            self._key_cache.clear()
            logger.info(None, keys_cleared=cache_size)

    def xǁEncryptionManagerǁclear_cache__mutmut_3(self) -> None:
        """Clear the key cache (useful for testing or key rotation)."""
        with self._lock:
            cache_size = len(self._key_cache)
            self._key_cache.clear()
            logger.info("Cleared encryption key cache", keys_cleared=None)

    def xǁEncryptionManagerǁclear_cache__mutmut_4(self) -> None:
        """Clear the key cache (useful for testing or key rotation)."""
        with self._lock:
            cache_size = len(self._key_cache)
            self._key_cache.clear()
            logger.info(keys_cleared=cache_size)

    def xǁEncryptionManagerǁclear_cache__mutmut_5(self) -> None:
        """Clear the key cache (useful for testing or key rotation)."""
        with self._lock:
            cache_size = len(self._key_cache)
            self._key_cache.clear()
            logger.info("Cleared encryption key cache", )

    def xǁEncryptionManagerǁclear_cache__mutmut_6(self) -> None:
        """Clear the key cache (useful for testing or key rotation)."""
        with self._lock:
            cache_size = len(self._key_cache)
            self._key_cache.clear()
            logger.info("XXCleared encryption key cacheXX", keys_cleared=cache_size)

    def xǁEncryptionManagerǁclear_cache__mutmut_7(self) -> None:
        """Clear the key cache (useful for testing or key rotation)."""
        with self._lock:
            cache_size = len(self._key_cache)
            self._key_cache.clear()
            logger.info("cleared encryption key cache", keys_cleared=cache_size)

    def xǁEncryptionManagerǁclear_cache__mutmut_8(self) -> None:
        """Clear the key cache (useful for testing or key rotation)."""
        with self._lock:
            cache_size = len(self._key_cache)
            self._key_cache.clear()
            logger.info("CLEARED ENCRYPTION KEY CACHE", keys_cleared=cache_size)
    
    xǁEncryptionManagerǁclear_cache__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁEncryptionManagerǁclear_cache__mutmut_1': xǁEncryptionManagerǁclear_cache__mutmut_1, 
        'xǁEncryptionManagerǁclear_cache__mutmut_2': xǁEncryptionManagerǁclear_cache__mutmut_2, 
        'xǁEncryptionManagerǁclear_cache__mutmut_3': xǁEncryptionManagerǁclear_cache__mutmut_3, 
        'xǁEncryptionManagerǁclear_cache__mutmut_4': xǁEncryptionManagerǁclear_cache__mutmut_4, 
        'xǁEncryptionManagerǁclear_cache__mutmut_5': xǁEncryptionManagerǁclear_cache__mutmut_5, 
        'xǁEncryptionManagerǁclear_cache__mutmut_6': xǁEncryptionManagerǁclear_cache__mutmut_6, 
        'xǁEncryptionManagerǁclear_cache__mutmut_7': xǁEncryptionManagerǁclear_cache__mutmut_7, 
        'xǁEncryptionManagerǁclear_cache__mutmut_8': xǁEncryptionManagerǁclear_cache__mutmut_8
    }
    
    def clear_cache(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁEncryptionManagerǁclear_cache__mutmut_orig"), object.__getattribute__(self, "xǁEncryptionManagerǁclear_cache__mutmut_mutants"), args, kwargs, self)
        return result 
    
    clear_cache.__signature__ = _mutmut_signature(xǁEncryptionManagerǁclear_cache__mutmut_orig)
    xǁEncryptionManagerǁclear_cache__mutmut_orig.__name__ = 'xǁEncryptionManagerǁclear_cache'


# Module-level singleton instance
_manager: EncryptionManager | None = None
_manager_lock = threading.Lock()


def x__get_manager__mutmut_orig() -> EncryptionManager:
    """Get or create the singleton encryption manager instance."""
    global _manager

    if _manager is not None:
        return _manager

    with _manager_lock:
        if _manager is None:
            _manager = EncryptionManager()
            logger.debug("Created singleton encryption manager")

        return _manager


def x__get_manager__mutmut_1() -> EncryptionManager:
    """Get or create the singleton encryption manager instance."""
    global _manager

    if _manager is None:
        return _manager

    with _manager_lock:
        if _manager is None:
            _manager = EncryptionManager()
            logger.debug("Created singleton encryption manager")

        return _manager


def x__get_manager__mutmut_2() -> EncryptionManager:
    """Get or create the singleton encryption manager instance."""
    global _manager

    if _manager is not None:
        return _manager

    with _manager_lock:
        if _manager is not None:
            _manager = EncryptionManager()
            logger.debug("Created singleton encryption manager")

        return _manager


def x__get_manager__mutmut_3() -> EncryptionManager:
    """Get or create the singleton encryption manager instance."""
    global _manager

    if _manager is not None:
        return _manager

    with _manager_lock:
        if _manager is None:
            _manager = None
            logger.debug("Created singleton encryption manager")

        return _manager


def x__get_manager__mutmut_4() -> EncryptionManager:
    """Get or create the singleton encryption manager instance."""
    global _manager

    if _manager is not None:
        return _manager

    with _manager_lock:
        if _manager is None:
            _manager = EncryptionManager()
            logger.debug(None)

        return _manager


def x__get_manager__mutmut_5() -> EncryptionManager:
    """Get or create the singleton encryption manager instance."""
    global _manager

    if _manager is not None:
        return _manager

    with _manager_lock:
        if _manager is None:
            _manager = EncryptionManager()
            logger.debug("XXCreated singleton encryption managerXX")

        return _manager


def x__get_manager__mutmut_6() -> EncryptionManager:
    """Get or create the singleton encryption manager instance."""
    global _manager

    if _manager is not None:
        return _manager

    with _manager_lock:
        if _manager is None:
            _manager = EncryptionManager()
            logger.debug("created singleton encryption manager")

        return _manager


def x__get_manager__mutmut_7() -> EncryptionManager:
    """Get or create the singleton encryption manager instance."""
    global _manager

    if _manager is not None:
        return _manager

    with _manager_lock:
        if _manager is None:
            _manager = EncryptionManager()
            logger.debug("CREATED SINGLETON ENCRYPTION MANAGER")

        return _manager

x__get_manager__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_manager__mutmut_1': x__get_manager__mutmut_1, 
    'x__get_manager__mutmut_2': x__get_manager__mutmut_2, 
    'x__get_manager__mutmut_3': x__get_manager__mutmut_3, 
    'x__get_manager__mutmut_4': x__get_manager__mutmut_4, 
    'x__get_manager__mutmut_5': x__get_manager__mutmut_5, 
    'x__get_manager__mutmut_6': x__get_manager__mutmut_6, 
    'x__get_manager__mutmut_7': x__get_manager__mutmut_7
}

def _get_manager(*args, **kwargs):
    result = _mutmut_trampoline(x__get_manager__mutmut_orig, x__get_manager__mutmut_mutants, args, kwargs)
    return result 

_get_manager.__signature__ = _mutmut_signature(x__get_manager__mutmut_orig)
x__get_manager__mutmut_orig.__name__ = 'x__get_manager'


# Public API - convenience functions that delegate to the singleton manager


def x_encrypt__mutmut_orig(plaintext: bytes) -> bytes:
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


# Public API - convenience functions that delegate to the singleton manager


def x_encrypt__mutmut_1(plaintext: bytes) -> bytes:
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
    return _get_manager().encrypt(None)

x_encrypt__mutmut_mutants : ClassVar[MutantDict] = {
'x_encrypt__mutmut_1': x_encrypt__mutmut_1
}

def encrypt(*args, **kwargs):
    result = _mutmut_trampoline(x_encrypt__mutmut_orig, x_encrypt__mutmut_mutants, args, kwargs)
    return result 

encrypt.__signature__ = _mutmut_signature(x_encrypt__mutmut_orig)
x_encrypt__mutmut_orig.__name__ = 'x_encrypt'


def x_decrypt__mutmut_orig(ciphertext: bytes) -> bytes:
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


def x_decrypt__mutmut_1(ciphertext: bytes) -> bytes:
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
    return _get_manager().decrypt(None)

x_decrypt__mutmut_mutants : ClassVar[MutantDict] = {
'x_decrypt__mutmut_1': x_decrypt__mutmut_1
}

def decrypt(*args, **kwargs):
    result = _mutmut_trampoline(x_decrypt__mutmut_orig, x_decrypt__mutmut_mutants, args, kwargs)
    return result 

decrypt.__signature__ = _mutmut_signature(x_decrypt__mutmut_orig)
x_decrypt__mutmut_orig.__name__ = 'x_decrypt'


def clear_encryption_cache() -> None:
    """Clear the encryption key cache (useful for testing or key rotation)."""
    _get_manager().clear_cache()


def x_reset_encryption_manager__mutmut_orig() -> None:
    """Reset the singleton manager (for testing only)."""
    global _manager
    with _manager_lock:
        _manager = None
        logger.debug("Reset encryption manager singleton")


def x_reset_encryption_manager__mutmut_1() -> None:
    """Reset the singleton manager (for testing only)."""
    global _manager
    with _manager_lock:
        _manager = ""
        logger.debug("Reset encryption manager singleton")


def x_reset_encryption_manager__mutmut_2() -> None:
    """Reset the singleton manager (for testing only)."""
    global _manager
    with _manager_lock:
        _manager = None
        logger.debug(None)


def x_reset_encryption_manager__mutmut_3() -> None:
    """Reset the singleton manager (for testing only)."""
    global _manager
    with _manager_lock:
        _manager = None
        logger.debug("XXReset encryption manager singletonXX")


def x_reset_encryption_manager__mutmut_4() -> None:
    """Reset the singleton manager (for testing only)."""
    global _manager
    with _manager_lock:
        _manager = None
        logger.debug("reset encryption manager singleton")


def x_reset_encryption_manager__mutmut_5() -> None:
    """Reset the singleton manager (for testing only)."""
    global _manager
    with _manager_lock:
        _manager = None
        logger.debug("RESET ENCRYPTION MANAGER SINGLETON")

x_reset_encryption_manager__mutmut_mutants : ClassVar[MutantDict] = {
'x_reset_encryption_manager__mutmut_1': x_reset_encryption_manager__mutmut_1, 
    'x_reset_encryption_manager__mutmut_2': x_reset_encryption_manager__mutmut_2, 
    'x_reset_encryption_manager__mutmut_3': x_reset_encryption_manager__mutmut_3, 
    'x_reset_encryption_manager__mutmut_4': x_reset_encryption_manager__mutmut_4, 
    'x_reset_encryption_manager__mutmut_5': x_reset_encryption_manager__mutmut_5
}

def reset_encryption_manager(*args, **kwargs):
    result = _mutmut_trampoline(x_reset_encryption_manager__mutmut_orig, x_reset_encryption_manager__mutmut_mutants, args, kwargs)
    return result 

reset_encryption_manager.__signature__ = _mutmut_signature(x_reset_encryption_manager__mutmut_orig)
x_reset_encryption_manager__mutmut_orig.__name__ = 'x_reset_encryption_manager'


# Legacy compatibility (for CONFIG_KEY_NAME used in tests)
CONFIG_KEY_NAME = "private_state_shared_secret"
