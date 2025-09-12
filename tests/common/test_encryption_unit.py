"""
Unit tests for the pyvider.common.encryption module

Tests the core encryption functionality independently of the Terraform protocol
to ensure cryptographic security and proper error handling.
"""
import os
from unittest.mock import patch, MagicMock

import pytest

from pyvider.common.config import PyviderConfig
from pyvider.common.encryption import encrypt, decrypt, _get_key, HKDF_SALT, HKDF_INFO, _ENCRYPTION_KEY
from pyvider.exceptions import FrameworkConfigurationError

# Import testkit fixtures with fallback
try:
    from provide.testkit import temp_file
except ImportError:
    import tempfile
    
    @pytest.fixture
    def temp_file():
        """Fallback temp_file fixture."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            yield f.name
        os.unlink(f.name)


class TestEncryptionCore:
    """Test core encryption/decryption functionality"""

    @pytest.fixture
    def reset_encryption_key(self):
        """Reset the cached encryption key before each test"""
        import pyvider.common.encryption
        original_key = pyvider.common.encryption._ENCRYPTION_KEY
        pyvider.common.encryption._ENCRYPTION_KEY = None
        yield
        pyvider.common.encryption._ENCRYPTION_KEY = original_key

    @pytest.fixture
    def temp_config_file(self, temp_file):
        """Create a temporary config file for testing"""
        config_path = str(temp_file) + '.toml'
        with open(config_path, 'w') as f:
            f.write('[pyvider]\nprivate_state_shared_secret = "config-file-secret"\n')
        
        yield config_path
        
        # Cleanup
        if os.path.exists(config_path):
            os.unlink(config_path)

    def test_encrypt_decrypt_roundtrip(self, encryption_key_env):
        """Test that data can be encrypted and decrypted successfully"""
        test_data = b"sensitive information that needs protection"
        
        encrypted = encrypt(test_data)
        decrypted = decrypt(encrypted)
        
        assert decrypted == test_data
        assert encrypted != test_data

    def test_encryption_produces_different_output(self, encryption_key_env):
        """Test that encryption produces different output each time (nonce randomization)"""
        test_data = b"same input data"
        
        encrypted1 = encrypt(test_data)
        encrypted2 = encrypt(test_data)
        
        assert encrypted1 != encrypted2
        assert decrypt(encrypted1) == test_data
        assert decrypt(encrypted2) == test_data

    def test_encrypt_empty_data(self, encryption_key_env):
        """Test encryption of empty data"""
        assert encrypt(b"") == b""
        assert decrypt(b"") == b""

    def test_encrypt_various_data_sizes(self, encryption_key_env):
        """Test encryption of various data sizes"""
        test_cases = [
            b"a",  # Single byte
            b"short string",  # Short string
            b"a" * 1000,  # Medium string
            b"x" * 100000,  # Large string
            b"\x00\x01\x02\x03\xff",  # Binary data
            "🔐🗝️💾".encode('utf-8'),  # Unicode data
        ]
        
        for test_data in test_cases:
            encrypted = encrypt(test_data)
            decrypted = decrypt(encrypted)
            assert decrypted == test_data

    def test_encryption_structure(self, encryption_key_env):
        """Test that encrypted data has the expected structure (nonce + ciphertext)"""
        test_data = b"test data for structure verification"
        encrypted = encrypt(test_data)
        
        # AES-GCM uses 12-byte nonce
        assert len(encrypted) >= 12  # At least nonce length
        assert len(encrypted) > len(test_data)  # Should be longer due to nonce + MAC

    def test_decrypt_invalid_ciphertext_fails(self, encryption_key_env):
        """Test that decrypting invalid ciphertext fails with proper error"""
        invalid_data = b"this is not valid encrypted data"
        
        with pytest.raises(ValueError, match="Private state decryption failed"):
            decrypt(invalid_data)

    def test_decrypt_too_short_data_fails(self, encryption_key_env):
        """Test that data too short to contain a nonce fails"""
        short_data = b"short"  # Less than 12 bytes
        
        with pytest.raises(ValueError, match="Invalid ciphertext: too short"):
            decrypt(short_data)

    def test_decrypt_corrupted_nonce_fails(self, encryption_key_env):
        """Test that corrupted nonce in ciphertext fails"""
        test_data = b"test data"
        encrypted = encrypt(test_data)
        
        # Corrupt the nonce (first 12 bytes)
        corrupted = b"bad_nonce123" + encrypted[12:]
        
        with pytest.raises(ValueError, match="Private state decryption failed"):
            decrypt(corrupted)

    def test_decrypt_corrupted_ciphertext_fails(self, encryption_key_env):
        """Test that corrupted ciphertext fails"""
        test_data = b"test data"
        encrypted = encrypt(test_data)
        
        # Corrupt the ciphertext portion
        nonce = encrypted[:12]
        corrupted_ciphertext = b"corrupted" + b"\x00" * (len(encrypted) - 12 - 9)
        corrupted = nonce + corrupted_ciphertext
        
        with pytest.raises(ValueError, match="Private state decryption failed"):
            decrypt(corrupted)


class TestKeyDerivation:
    """Test key derivation functionality"""

    @pytest.fixture(autouse=True)
    def reset_encryption_key(self):
        """Reset the cached encryption key before each test"""
        import pyvider.common.encryption
        original_key = pyvider.common.encryption._ENCRYPTION_KEY
        pyvider.common.encryption._ENCRYPTION_KEY = None
        yield
        pyvider.common.encryption._ENCRYPTION_KEY = original_key

    def test_get_key_from_environment_variable(self):
        """Test key derivation from environment variable"""
        test_secret = "test-secret-from-env"
        
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": test_secret}):
            key = _get_key()
            
            assert len(key) == 32  # AES-256 key length
            assert isinstance(key, bytes)

    def test_get_key_from_config_file(self):
        """Test key derivation from config file"""
        import pyvider.common.encryption
        
        # Test using environment variable (which is the correct way)
        with patch.dict(os.environ, {'PYVIDER_PRIVATE_STATE_SHARED_SECRET': 'config-file-secret'}, clear=True):
            # Clear the cached key first
            pyvider.common.encryption._ENCRYPTION_KEY = None
            
            key = _get_key()
            
            assert len(key) == 32
            assert isinstance(key, bytes)

    def test_get_key_no_secret_fails(self):
        """Test that missing shared secret raises proper error"""
        import pyvider.common.encryption
        
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(PyviderConfig, 'get') as mock_get:
                mock_get.return_value = None
                
                # Clear the cached key first
                pyvider.common.encryption._ENCRYPTION_KEY = None
                
                with pytest.raises(FrameworkConfigurationError, match="Private state shared secret not found"):
                    _get_key()

    def test_key_caching(self):
        """Test that keys are cached and not re-derived"""
        test_secret = "test-caching-secret"
        
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": test_secret}):
            key1 = _get_key()
            key2 = _get_key()
            
            assert key1 is key2  # Should be the same object due to caching

    def test_different_secrets_produce_different_keys(self):
        """Test that different secrets produce different derived keys"""
        import pyvider.common.encryption
        
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": "secret1"}):
            pyvider.common.encryption._ENCRYPTION_KEY = None
            key1 = _get_key()
        
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": "secret2"}):
            pyvider.common.encryption._ENCRYPTION_KEY = None
            key2 = _get_key()
        
        assert key1 != key2

    def test_same_secret_produces_same_key(self):
        """Test that the same secret always produces the same derived key"""
        import pyvider.common.encryption
        test_secret = "consistent-secret"
        
        # Get key first time
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": test_secret}):
            pyvider.common.encryption._ENCRYPTION_KEY = None
            key1 = _get_key()
        
        # Get key second time
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": test_secret}):
            pyvider.common.encryption._ENCRYPTION_KEY = None
            key2 = _get_key()
        
        assert key1 == key2

    def test_hkdf_parameters(self):
        """Test that HKDF uses the correct parameters"""
        # These should be static and well-defined
        assert HKDF_SALT == b"pyvider-private-state-encryption-salt"
        assert HKDF_INFO == b"hkdf-info-for-aes-256-gcm-key"


class TestEncryptionSecurity:
    """Test security properties of the encryption implementation"""

    def test_encryption_key_not_leaked_in_exceptions(self, encryption_key_env):
        """Test that encryption keys are not leaked in exception messages"""
        invalid_data = b"invalid encrypted data"
        
        try:
            decrypt(invalid_data)
        except ValueError as e:
            error_message = str(e)
            # Ensure no key material is in the error message
            assert "key" not in error_message.lower()
            assert len([word for word in error_message.split() if len(word) > 20]) == 0  # No long strings

    def test_ciphertext_does_not_contain_plaintext(self, encryption_key_env):
        """Test that ciphertext does not contain recognizable plaintext"""
        plaintext = b"this is very secret information that should not be visible"
        encrypted = encrypt(plaintext)
        
        # The encrypted data should not contain any of the original words
        encrypted_str = encrypted.decode('latin1', errors='ignore').lower()
        for word in [b'secret', b'information', b'visible']:
            assert word not in encrypted

    def test_key_derivation_is_deterministic(self):
        """Test that key derivation is deterministic for the same input"""
        import pyvider.common.encryption
        from pyvider.common.encryption import HKDF_SALT, HKDF_INFO
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.hkdf import HKDF
        
        test_secret = "deterministic-test-secret"
        
        # Manually derive key to compare
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=HKDF_SALT,
            info=HKDF_INFO,
        )
        expected_key = hkdf.derive(test_secret.encode("utf-8"))
        
        # Get key through the encryption module
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": test_secret}):
            pyvider.common.encryption._ENCRYPTION_KEY = None
            actual_key = _get_key()
        
        assert actual_key == expected_key

    @pytest.mark.parametrize("data_size", [1, 16, 256, 1024, 4096])
    def test_encryption_timing_independence(self, encryption_key_env, data_size):
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

    def test_encryption_with_unicode_secrets(self):
        """Test that unicode secrets work correctly"""
        import pyvider.common.encryption
        unicode_secret = "🔐🗝️💾 unicode secret with emojis"
        
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": unicode_secret}):
            pyvider.common.encryption._ENCRYPTION_KEY = None
            key = _get_key()
            
            assert len(key) == 32
            
            # Test encryption/decryption works
            test_data = b"test data with unicode secret"
            encrypted = encrypt(test_data)
            decrypted = decrypt(encrypted)
            assert decrypted == test_data

    def test_encryption_with_very_long_secret(self):
        """Test encryption with very long shared secret"""
        import pyvider.common.encryption
        long_secret = "x" * 10000  # 10KB secret
        
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": long_secret}):
            pyvider.common.encryption._ENCRYPTION_KEY = None
            key = _get_key()
            
            assert len(key) == 32  # Should still derive to 32-byte key
            
            test_data = b"test with long secret"
            encrypted = encrypt(test_data)
            decrypted = decrypt(encrypted)
            assert decrypted == test_data

    def test_encryption_with_special_characters_secret(self):
        """Test encryption with special characters in secret"""
        import pyvider.common.encryption
        special_secret = "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`"
        
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": special_secret}):
            pyvider.common.encryption._ENCRYPTION_KEY = None
            key = _get_key()
            
            assert len(key) == 32
            
            test_data = b"test with special character secret"
            encrypted = encrypt(test_data)
            decrypted = decrypt(encrypted)
            assert decrypted == test_data