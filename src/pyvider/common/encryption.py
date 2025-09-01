import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from pyvider.common.config import PyviderConfig
from pyvider.exceptions import FrameworkConfigurationError
from provide.foundation import logger

# This salt is static and public.
HKDF_SALT = b"pyvider-private-state-encryption-salt"
HKDF_INFO = b"hkdf-info-for-aes-256-gcm-key"
CONFIG_KEY_NAME = "private_state_shared_secret"

_ENCRYPTION_KEY: bytes | None = None


def _get_key() -> bytes:
    """
    Retrieves and derives a cryptographically strong encryption key.
    It now uses the unified configuration system and fails if no secret is found.
    """
    global _ENCRYPTION_KEY
    if _ENCRYPTION_KEY is not None:
        return _ENCRYPTION_KEY

    config = PyviderConfig()
    shared_secret = config.get(CONFIG_KEY_NAME)

    if not shared_secret:
        raise FrameworkConfigurationError(
            f"🔐 Private state shared secret not found. Please set the "
            f"PYVIDER_{CONFIG_KEY_NAME.upper()} environment variable, or define "
            f"'{CONFIG_KEY_NAME}' in a 'pyvider.toml' file (which can be "
            f"specified with the PYVIDER_CONFIG_FILE environment variable)."
        )

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


def encrypt(plaintext: bytes) -> bytes:
    """Encrypts plaintext using AES-256-GCM with the derived key."""
    if not plaintext:
        return b""
    key = _get_key()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ciphertext


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
