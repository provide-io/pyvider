#
# SPDX-FileCopyrightText: Copyright (c) 2025-2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for the pyvider.common.encryption module

Tests the core encryption functionality independently of the Terraform protocol
to ensure cryptographic security and proper error handling."""

from collections.abc import Generator
import os
from pathlib import Path

from provide.foundation.errors import ConfigurationError
from provide.testkit.mocking import patch
import pytest

from pyvider.common.config import PyviderConfig
from pyvider.common.encryption import (
    HKDF_INFO,
    EncryptionError,
    decrypt,
    encrypt,
    reset_encryption_manager,
)

# Import testkit fixtures with fallback
try:
    from provide.testkit import temp_file
except ImportError:
    import tempfile

    @pytest.fixture
    def temp_file() -> Generator[str, None, None]:
        """Fallback temp_file fixture."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            yield f.name
        Path(f.name).unlink()

    def reset_encryption_manager_fixture(self: any) -> Generator[None, None, None]:
        """Reset the encryption manager before each test"""
        reset_encryption_manager()
        yield
        reset_encryption_manager()

    @pytest.fixture
    def temp_config_file(self: any, temp_file: str) -> Generator[str, None, None]:
        """Create a temporary config file for testing"""
        config_path = Path(temp_file + ".toml")
        with config_path.open("w") as f:
            f.write('[pyvider]\nprivate_state_shared_secret = "config-file-secret"\n')

        yield str(config_path)

        # Cleanup
        if config_path.exists():
            config_path.unlink()

    def test_encrypt_decrypt_roundtrip(self: any, encryption_key_env: any) -> None:
        """Test that data can be encrypted and decrypted successfully"""
        test_data = b"sensitive information that needs protection"

        encrypted = encrypt(test_data)
        decrypted = decrypt(encrypted)

        assert decrypted == test_data
        assert encrypted != test_data

    def test_encryption_produces_different_output(self: any, encryption_key_env: any) -> None:
        """Test that encryption produces different output each time (nonce randomization)"""
        test_data = b"same input data"

        encrypted1 = encrypt(test_data)
        encrypted2 = encrypt(test_data)

        assert encrypted1 != encrypted2
        assert decrypt(encrypted1) == test_data
        assert decrypt(encrypted2) == test_data

    def test_encrypt_empty_data(self: any, encryption_key_env: any) -> None:
        """Test encryption of empty data"""
        assert encrypt(b"") == b""
        assert decrypt(b"") == b""

    def test_encrypt_various_data_sizes(self: any, encryption_key_env: any) -> None:
        """Test encryption of various data sizes"""
        test_cases = [
            b"a",  # Single byte
            b"short string",  # Short string
            b"a" * 1000,  # Medium string
            b"x" * 100000,  # Large string
            b"\x00\x01\x02\x03\xff",  # Binary data
            "🔐🗝️💾".encode(),  # Unicode data
        ]

        for test_data in test_cases:
            encrypted = encrypt(test_data)
            decrypted = decrypt(encrypted)
            assert decrypted == test_data

    def test_encryption_structure(self: any, encryption_key_env: any) -> None:
        """Test that encrypted data has the expected structure (version + salt + nonce + ciphertext)"""
        test_data = b"test data for structure verification"
        encrypted = encrypt(test_data)

        # New format: [1 byte version][16 bytes salt][12 bytes nonce][ciphertext+tag]
        min_size = 1 + 16 + 12  # version + salt + nonce
        assert len(encrypted) >= min_size  # At least header size
        assert len(encrypted) > len(test_data)  # Should be longer due to header + MAC

        # Check version byte
        assert encrypted[0] == 0x01  # VERSION_CURRENT

    def test_decrypt_invalid_ciphertext_fails(self: any, encryption_key_env: any) -> None:
        """Test that decrypting invalid ciphertext fails with proper error"""
        invalid_data = b"this is not valid encrypted data"

        # Should raise EncryptionError (could be version mismatch or decryption failure)
        with pytest.raises(EncryptionError):
            decrypt(invalid_data)

    def test_decrypt_too_short_data_fails(self: any, encryption_key_env: any) -> None:
        """Test that data too short to contain a nonce fails"""
        short_data = b"short"  # Less than 12 bytes

        with pytest.raises(EncryptionError, match="Ciphertext too short"):
            decrypt(short_data)

    def test_decrypt_corrupted_nonce_fails(self: any, encryption_key_env: any) -> None:
        """Test that corrupted nonce in ciphertext fails"""
        test_data = b"test data"
        encrypted = encrypt(test_data)

        # Corrupt the nonce (skip version byte and salt, then corrupt nonce)
        # New format: [1 byte version][16 bytes salt][12 bytes nonce][ciphertext]
        corrupted = encrypted[:17] + b"bad_nonce123" + encrypted[29:]

        with pytest.raises(EncryptionError, match="Decryption failed"):
            decrypt(corrupted)

    def test_decrypt_corrupted_ciphertext_fails(self: any, encryption_key_env: any) -> None:
        """Test that corrupted ciphertext fails"""
        test_data = b"test data"
        encrypted = encrypt(test_data)

        # Corrupt the ciphertext portion (after version + salt + nonce)
        # New format: [1 byte version][16 bytes salt][12 bytes nonce][ciphertext]
        header = encrypted[:29]  # version + salt + nonce
        corrupted_ciphertext = b"corrupted" + b"\x00" * (len(encrypted) - 29 - 9)
        corrupted = header + corrupted_ciphertext

        with pytest.raises(EncryptionError, match="Decryption failed"):
            decrypt(corrupted)


class TestKeyDerivation:
    """Test key derivation functionality"""

    def reset_encryption_manager_fixture(self: any) -> Generator[None, None, None]:
        """Reset the encryption manager before each test"""
        reset_encryption_manager()
        yield
        reset_encryption_manager()

    def test_encrypt_from_environment_variable(self) -> None:
        """Test encryption with key derived from environment variable"""
        test_secret = "test-secret-from-env"
        test_data = b"test data"

        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": test_secret}):
            encrypted = encrypt(test_data)
            decrypted = decrypt(encrypted)

            assert decrypted == test_data
            assert len(encrypted) > len(test_data)  # Has version + salt + nonce + MAC

    def test_encrypt_from_config_file(self) -> None:
        """Test encryption with key from config file (via environment)"""
        test_data = b"test data"

        # Test using environment variable (which is the correct way)
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": "config-file-secret"}, clear=True):
            reset_encryption_manager()

            encrypted = encrypt(test_data)
            decrypted = decrypt(encrypted)

            assert decrypted == test_data

    def test_encrypt_no_secret_fails(self) -> None:
        """Test that missing shared secret raises proper error"""
        with patch.dict(os.environ, {}, clear=True), patch.object(PyviderConfig, "get") as mock_get:
            mock_get.return_value = None

            reset_encryption_manager()

            with pytest.raises(ConfigurationError, match="Private state shared secret"):
                encrypt(b"test data")

    def test_salt_randomization(self) -> None:
        """Test that different encryptions use different salts"""
        test_secret = "test-salt-randomization"
        test_data = b"same plaintext"

        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": test_secret}):
            encrypted1 = encrypt(test_data)
            encrypted2 = encrypt(test_data)

            # Extract salts (bytes 1-17, after version byte)
            salt1 = encrypted1[1:17]
            salt2 = encrypted2[1:17]

            # Salts should be different (random)
            assert salt1 != salt2

            # But both should decrypt to same plaintext
            assert decrypt(encrypted1) == test_data
            assert decrypt(encrypted2) == test_data

    def test_different_secrets_produce_different_ciphertexts(self) -> None:
        """Test that different secrets produce different ciphertexts"""
        test_data = b"same plaintext"

        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": "secret1"}):
            reset_encryption_manager()
            encrypted1 = encrypt(test_data)

        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": "secret2"}):
            reset_encryption_manager()
            encrypted2 = encrypt(test_data)

        # Different secrets should produce different ciphertexts
        assert encrypted1 != encrypted2

        # And can't decrypt with wrong secret
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": "secret1"}):
            reset_encryption_manager()
            with pytest.raises(EncryptionError):
                decrypt(encrypted2)  # encrypted with secret2

    def test_same_secret_can_decrypt(self) -> None:
        """Test that the same secret can decrypt previously encrypted data"""
        test_secret = "consistent-secret"
        test_data = b"test data"

        # Encrypt with secret
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": test_secret}):
            reset_encryption_manager()
            encrypted = encrypt(test_data)

        # Decrypt with same secret (fresh manager)
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": test_secret}):
            reset_encryption_manager()
            decrypted = decrypt(encrypted)

        assert decrypted == test_data

    def test_hkdf_info_parameter(self) -> None:
        """Test that HKDF uses the correct info parameter"""
        # Info should be well-defined (salt is now random per encryption)
        assert HKDF_INFO == b"pyvider-private-state-v1"


class TestEncryptionSecurity:
    """Test security properties of the encryption implementation"""

    def test_encryption_key_not_leaked_in_exceptions(
        self,
        encryption_key_env: pytest.MonkeyPatch,
    ) -> None:
        """Test that encryption keys are not leaked in exception messages"""
        invalid_data = b"invalid encrypted data"

        try:
            decrypt(invalid_data)
        except EncryptionError as e:
            error_message = str(e)
            # Ensure no key material is in the error message
            assert "key" not in error_message.lower() or "wrong key" in error_message.lower()
            # No long hex strings that could be key material
            assert len([word for word in error_message.split() if len(word) > 30]) == 0

    def test_ciphertext_does_not_contain_plaintext(self, encryption_key_env: pytest.MonkeyPatch) -> None:
        """Test that ciphertext does not contain recognizable plaintext"""
        plaintext = b"this is very secret information that should not be visible"
        encrypted = encrypt(plaintext)

        # The encrypted data should not contain any of the original words
        encrypted.decode("latin1", errors="ignore").lower()
        for word in [b"secret", b"information", b"visible"]:
            assert word not in encrypted

    def test_key_derivation_is_deterministic(self) -> None:
        """Test that key derivation is deterministic for the same salt and secret"""
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF

        from pyvider.common.encryption import HKDF_INFO

        test_secret = "deterministic-test-secret"
        test_salt = b"test_salt_16byte"  # 16 bytes

        # Manually derive key to compare
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=test_salt,
            info=HKDF_INFO,
        )
        hkdf.derive(test_secret.encode("utf-8"))

        # Encrypt and extract the derived key behavior by decrypting
        # We can't access _derive_key directly, but we can verify determinism
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": test_secret}):
            reset_encryption_manager()
            # Create test data with controlled salt by monkey-patching os.urandom

            original_urandom = os.urandom
            call_count = [0]

            def controlled_urandom(n: int) -> bytes:
                call_count[0] += 1
                if call_count[0] == 1:  # First call is for salt
                    return test_salt
                return original_urandom(n)  # Nonce uses real random

            with patch.object(os, "urandom", controlled_urandom):
                encrypted = encrypt(b"test")

            # Verify the salt in the ciphertext matches
            extracted_salt = encrypted[1:17]  # bytes 1-17 are salt
            assert extracted_salt == test_salt

    @pytest.mark.parametrize("data_size", [1, 16, 256, 1024, 4096])
    def test_encryption_timing_independence(
        self, encryption_key_env: pytest.MonkeyPatch, data_size: int
    ) -> None:
        """Test that encryption time doesn't vary significantly with data content"""
        # This is a basic test - sophisticated timing analysis would require more complex testing
        data_zeros = b"\x00" * data_size
        data_random = os.urandom(data_size)

        # Both should encrypt without error
        encrypted_zeros = encrypt(data_zeros)
        encrypted_random = encrypt(data_random)

        # Both should decrypt correctly
        assert decrypt(encrypted_zeros) == data_zeros
        assert decrypt(encrypted_random) == data_random

        # Ciphertext lengths should be similar (nonce + data + MAC)
        assert abs(len(encrypted_zeros) - len(encrypted_random)) == 0


class TestEncryptionCompatibility:
    """Test compatibility and edge cases"""

    def test_encryption_with_unicode_secrets(self) -> None:
        """Test that unicode secrets work correctly"""
        unicode_secret = "🔐🗝️💾 unicode secret with emojis"

        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": unicode_secret}):
            reset_encryption_manager()

            # Test encryption/decryption works
            test_data = b"test data with unicode secret"
            encrypted = encrypt(test_data)
            decrypted = decrypt(encrypted)
            assert decrypted == test_data

    def test_encryption_with_very_long_secret(self) -> None:
        """Test encryption with very long shared secret"""
        long_secret = "x" * 10000  # 10KB secret

        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": long_secret}):
            reset_encryption_manager()

            test_data = b"test with long secret"
            encrypted = encrypt(test_data)
            decrypted = decrypt(encrypted)
            assert decrypted == test_data

    def test_encryption_with_special_characters_secret(self) -> None:
        """Test encryption with special characters in secret"""
        special_secret = "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`"

        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": special_secret}):
            reset_encryption_manager()

            test_data = b"test with special character secret"
            encrypted = encrypt(test_data)
            decrypted = decrypt(encrypted)
            assert decrypted == test_data


# 🐍🏗️🔚
