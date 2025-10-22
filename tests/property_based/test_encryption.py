"""Property-based tests for encryption using Hypothesis."""

import pytest
from hypothesis import given, strategies as st, assume

from pyvider.common.encryption import encrypt_data, decrypt_data


@given(
    plaintext=st.binary(min_size=0, max_size=10000),
    secret=st.text(min_size=8, max_size=100),
)
def test_encryption_roundtrip_property(plaintext: bytes, secret: str):
    """
    Property: For any plaintext and secret, encrypting and then decrypting
    should return the original plaintext.
    """
    encrypted = encrypt_data(plaintext, secret)
    decrypted = decrypt_data(encrypted, secret)
    assert decrypted == plaintext


@given(
    plaintext=st.binary(min_size=1, max_size=1000),
    secret1=st.text(min_size=8, max_size=100),
    secret2=st.text(min_size=8, max_size=100),
)
def test_different_secrets_produce_different_results(
    plaintext: bytes, secret1: str, secret2: str
):
    """
    Property: Encrypting the same plaintext with different secrets
    should produce different ciphertexts.
    """
    assume(secret1 != secret2)  # Only test when secrets are different

    encrypted1 = encrypt_data(plaintext, secret1)
    encrypted2 = encrypt_data(plaintext, secret2)

    # The encrypted values should be different
    assert encrypted1 != encrypted2


@given(
    plaintext=st.binary(min_size=1, max_size=1000),
    secret=st.text(min_size=8, max_size=100),
)
def test_encryption_produces_different_output_each_time(plaintext: bytes, secret: str):
    """
    Property: Encrypting the same plaintext multiple times should produce
    different ciphertexts (due to random nonce/salt).
    """
    encrypted1 = encrypt_data(plaintext, secret)
    encrypted2 = encrypt_data(plaintext, secret)

    # Should be different due to random nonce
    assert encrypted1 != encrypted2

    # But both should decrypt to the same plaintext
    assert decrypt_data(encrypted1, secret) == plaintext
    assert decrypt_data(encrypted2, secret) == plaintext


@given(
    plaintext=st.binary(min_size=0, max_size=1000),
    secret=st.text(min_size=8, max_size=100),
)
def test_encrypted_size_is_larger_than_plaintext(plaintext: bytes, secret: str):
    """
    Property: Encrypted data should always be larger than plaintext
    (due to nonce, tag, and salt overhead).
    """
    encrypted = encrypt_data(plaintext, secret)
    # Encrypted data includes: salt (16) + nonce (12) + tag (16) + ciphertext
    # So it should be at least 44 bytes larger
    assert len(encrypted) >= len(plaintext) + 44


@given(
    plaintext=st.binary(min_size=1, max_size=1000),
    secret=st.text(min_size=8, max_size=100),
)
def test_ciphertext_does_not_contain_plaintext(plaintext: bytes, secret: str):
    """
    Property: The ciphertext should not contain the plaintext as a substring.
    """
    assume(len(plaintext) > 4)  # Only test for non-trivial plaintexts
    encrypted = encrypt_data(plaintext, secret)
    assert plaintext not in encrypted


@given(
    data=st.binary(min_size=1, max_size=1000),
    secret=st.text(min_size=8, max_size=100),
)
def test_decrypt_random_data_fails_gracefully(data: bytes, secret: str):
    """
    Property: Decrypting random data (not actually encrypted) should fail
    with an appropriate exception.
    """
    # Skip if data happens to have the right structure
    assume(len(data) < 44)  # Too short to be valid encrypted data

    with pytest.raises(Exception):
        decrypt_data(data, secret)
