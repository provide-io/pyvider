import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from provide.foundation import logger
from provide.foundation.errors import with_error_handling

from pyvider.common.config import PyviderConfig
from pyvider.exceptions import FrameworkConfigurationError

# This salt is static and public.
HKDF_SALT = b"pyvider-private-state-encryption-salt"
HKDF_INFO = b"hkdf-info-for-aes-256-gcm-key"
CONFIG_KEY_NAME = "private_state_shared_secret"

_ENCRYPTION_KEY: bytes | None = None


@with_error_handling()
def _get_key() -> bytes:
    """
    Retrieves and derives a cryptographically strong encryption key.
    It now uses the unified configuration system and fails if no secret is found.
    """
    global _ENCRYPTION_KEY
    if _ENCRYPTION_KEY is not None:
        return _ENCRYPTION_KEY

    config = PyviderConfig()
    try:
        config.validate_required_fields()
        shared_secret = config.private_state_shared_secret
    except Exception as e:
        raise FrameworkConfigurationError(
            "🔐 Private state shared secret not found. Please set the "
            "PYVIDER_PRIVATE_STATE_SHARED_SECRET environment variable, or define "
            "'private_state_shared_secret' in a 'pyvider.toml' file."
        ) from e

    logger.debug("🔒 Using shared secret for private state encryption.")
    key_material = str(shared_secret).encode("utf-8")

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256 key
        salt=HKDF_SALT,
        info=HKDF_INFO,
    )
    _ENCRYPTION_KEY = hkdf.derive(key_material)
    return _ENCRYPTION_KEY


@with_error_handling()
def encrypt(plaintext: bytes) -> bytes:
    """Encrypts plaintext using AES-256-GCM with the derived key."""
    if not plaintext:
        return b""
    key = _get_key()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ciphertext


@with_error_handling()
def decrypt(ciphertext: bytes) -> bytes:
    """Decrypts ciphertext using AES-256-GCM with the derived key."""
    if not ciphertext:
        return b""
    if len(ciphertext) < 12:
        raise ValueError("Invalid ciphertext: too short to contain a nonce.")
    key = _get_key()
    nonce = ciphertext[:12]
    actual_ciphertext = ciphertext[12:]
    aesgcm = AESGCM(key)
    try:
        return aesgcm.decrypt(nonce, actual_ciphertext, None)
    except Exception as e:
        logger.error("🔒 Failed to decrypt private state.", exc_info=True)
        raise ValueError(
            "🔐 Private state decryption failed. This can happen if the shared secret has changed."
        ) from e
