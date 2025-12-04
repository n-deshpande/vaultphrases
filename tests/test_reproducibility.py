"""Test reproducibility with known test vectors.

These tests ensure that the derivation scheme produces consistent outputs
across different runs and implementations. The test vectors use test mode
for faster execution but verify the same deterministic behavior.

CRITICAL: If any of these tests fail, the derivation scheme has changed
and backward compatibility is BROKEN. This would mean users cannot recover
their passphrases from their root phrase.
"""

import pytest
from vaultphrases.derive import derive_master_key, derive_child_key
from vaultphrases.constants import LABEL_HOT, LABEL_COLD
from vaultphrases.wordlist import bytes_to_phrase


# =============================================================================
# FROZEN TEST VECTORS - DO NOT MODIFY
# =============================================================================
# These vectors were generated with vaultphrases v0.1.0 and MUST remain stable.
# If these tests fail, backward compatibility is broken.
#
# Test mode vectors (fast Argon2 parameters for CI):
TEST_VECTOR_ROOT_PHRASE = "correct horse battery staple"
TEST_VECTOR_MASTER_KEY_HEX = "30d853c509f28efb0b67ad776ea50d94a0a106a6ba4886534ff9c73b02e0ecc4"
TEST_VECTOR_HOT_KEY_HEX = "c6e7a0f9777d86803eb558155cfc0e8cda18bd77f51b02a931cb25fede2e5c13"
TEST_VECTOR_COLD_KEY_HEX = "178162974c67758635c64ecf9cc0580d70efd821d3b6592c82df341eeff44707"

# Production mode vectors (full Argon2 parameters - for reference only):
# Master key: 993ad4e731965509ab73b4d4aaacf06e4aa723f7f40846d70e9bb82eb402538d
# HOT key:    8ffd3bebb10f122d9d390a064451474fed3798acfc0c200e59670a523a57497c
# COLD key:   cd0a663d6be86e0c839dab533f222179990c11b1f6ced81aaf40f484134ce7af
# =============================================================================


def test_master_key_reproducibility():
    """Test that master key derivation is reproducible."""
    # Derive multiple times
    keys = [derive_master_key(TEST_VECTOR_ROOT_PHRASE, test_mode=True) for _ in range(5)]
    
    # All should be identical
    assert all(k == keys[0] for k in keys), "Master key derivation is not deterministic"
    assert len(keys[0]) == 32, "Master key should be 32 bytes"


def test_child_key_reproducibility():
    """Test that child key derivation is reproducible."""
    master_key = derive_master_key(TEST_VECTOR_ROOT_PHRASE, test_mode=True)
    
    # Derive HOT key multiple times
    hot_keys = [derive_child_key(master_key, LABEL_HOT) for _ in range(5)]
    
    # All should be identical
    assert all(k == hot_keys[0] for k in hot_keys), "HOT key derivation is not deterministic"
    
    # Derive COLD key multiple times
    cold_keys = [derive_child_key(master_key, LABEL_COLD) for _ in range(5)]
    
    # All should be identical
    assert all(k == cold_keys[0] for k in cold_keys), "COLD key derivation is not deterministic"


def test_phrase_generation_reproducibility():
    """Test that phrase generation from bytes is reproducible."""
    # Simple wordlist for testing
    wordlist = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot"]
    
    # Fixed bytes
    test_bytes = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    
    # Generate multiple times
    phrases = [bytes_to_phrase(test_bytes, wordlist, 6, "-") for _ in range(5)]
    
    # All should be identical
    assert all(p == phrases[0] for p in phrases), "Phrase generation is not deterministic"


def test_end_to_end_reproducibility():
    """Test complete end-to-end reproducibility: root phrase → passphrases."""
    wordlist = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel"]
    
    # Derive HOT and COLD phrases multiple times
    results = []
    for _ in range(3):
        master_key = derive_master_key(TEST_VECTOR_ROOT_PHRASE, test_mode=True)
        hot_key = derive_child_key(master_key, LABEL_HOT)
        cold_key = derive_child_key(master_key, LABEL_COLD)
        
        hot_phrase = bytes_to_phrase(hot_key, wordlist, 6, "-")
        cold_phrase = bytes_to_phrase(cold_key, wordlist, 6, "-")
        
        results.append((hot_phrase, cold_phrase))
    
    # All results should be identical
    assert all(r == results[0] for r in results), "End-to-end derivation is not deterministic"
    
    # Verify structure
    hot_phrase, cold_phrase = results[0]
    assert len(hot_phrase.split("-")) == 6, "HOT phrase should have 6 words"
    assert len(cold_phrase.split("-")) == 6, "COLD phrase should have 6 words"
    assert hot_phrase != cold_phrase, "HOT and COLD phrases should be different"


def test_normalization_reproducibility():
    """Test that phrase normalization produces consistent results."""
    # Different formatting, same content
    phrases = [
        "correct horse battery staple",
        "  correct horse battery staple  ",
        "CORRECT HORSE BATTERY STAPLE",
        "Correct   Horse    Battery     Staple",
        "\tcorrect\thorse\tbattery\tstaple\t",
    ]
    
    # All should produce the same master key
    keys = [derive_master_key(p, test_mode=True) for p in phrases]
    
    assert all(k == keys[0] for k in keys), "Normalization is not consistent"


def test_cross_run_stability():
    """
    Test that outputs remain stable across runs.
    
    CRITICAL: This is a regression test. If this fails, the derivation scheme
    has changed and backward compatibility is BROKEN. Users will not be able
    to recover their passphrases.
    """
    # Derive keys
    master_key = derive_master_key(TEST_VECTOR_ROOT_PHRASE, test_mode=True)
    hot_key = derive_child_key(master_key, LABEL_HOT)
    cold_key = derive_child_key(master_key, LABEL_COLD)
    
    # Verify against frozen test vectors
    assert master_key.hex() == TEST_VECTOR_MASTER_KEY_HEX, \
        f"Master key mismatch! Expected {TEST_VECTOR_MASTER_KEY_HEX}, got {master_key.hex()}"
    assert hot_key.hex() == TEST_VECTOR_HOT_KEY_HEX, \
        f"HOT key mismatch! Expected {TEST_VECTOR_HOT_KEY_HEX}, got {hot_key.hex()}"
    assert cold_key.hex() == TEST_VECTOR_COLD_KEY_HEX, \
        f"COLD key mismatch! Expected {TEST_VECTOR_COLD_KEY_HEX}, got {cold_key.hex()}"


def test_different_phrases_produce_different_keys():
    """Test that different root phrases produce different outputs."""
    phrases = [
        "correct horse battery staple",
        "incorrect horse battery staple",
        "correct horse battery stapler",
        "correct horse battery",
    ]
    
    keys = [derive_master_key(p, test_mode=True) for p in phrases]
    
    # All keys should be unique
    assert len(set(k.hex() for k in keys)) == len(keys), "Different phrases should produce different keys"


def test_label_independence():
    """Test that different labels produce independent keys."""
    master_key = derive_master_key(TEST_VECTOR_ROOT_PHRASE, test_mode=True)
    
    labels = ["HOT_PHRASE_V1", "COLD_PHRASE_V1", "SSH_PHRASE_V1", "GPG_PHRASE_V1"]
    child_keys = [derive_child_key(master_key, label) for label in labels]
    
    # All child keys should be unique
    assert len(set(k.hex() for k in child_keys)) == len(child_keys), "Different labels should produce different keys"


def test_production_mode_stability():
    """
    Test production mode stability with frozen vectors.
    
    NOTE: This test is slow (~3-5 seconds) due to full Argon2 parameters.
    It verifies that production derivation remains stable.
    """
    # Production mode frozen vectors
    PROD_MASTER_KEY_HEX = "993ad4e731965509ab73b4d4aaacf06e4aa723f7f40846d70e9bb82eb402538d"
    PROD_HOT_KEY_HEX = "8ffd3bebb10f122d9d390a064451474fed3798acfc0c200e59670a523a57497c"
    PROD_COLD_KEY_HEX = "cd0a663d6be86e0c839dab533f222179990c11b1f6ced81aaf40f484134ce7af"
    
    # Derive with production parameters
    master_key = derive_master_key(TEST_VECTOR_ROOT_PHRASE, test_mode=False)
    hot_key = derive_child_key(master_key, LABEL_HOT)
    cold_key = derive_child_key(master_key, LABEL_COLD)
    
    # Verify against frozen production vectors
    assert master_key.hex() == PROD_MASTER_KEY_HEX, \
        f"Production master key mismatch! Expected {PROD_MASTER_KEY_HEX}, got {master_key.hex()}"
    assert hot_key.hex() == PROD_HOT_KEY_HEX, \
        f"Production HOT key mismatch! Expected {PROD_HOT_KEY_HEX}, got {hot_key.hex()}"
    assert cold_key.hex() == PROD_COLD_KEY_HEX, \
        f"Production COLD key mismatch! Expected {PROD_COLD_KEY_HEX}, got {cold_key.hex()}"


def test_bytes_to_phrase_stability():
    """Test that bytes_to_phrase produces stable output."""
    # Fixed wordlist and bytes for reproducibility
    wordlist = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel"]
    test_bytes = bytes.fromhex(TEST_VECTOR_HOT_KEY_HEX)
    
    # Generate phrase
    phrase = bytes_to_phrase(test_bytes, wordlist, 6, "-")
    
    # Should always produce the same phrase (frozen from v0.1.0)
    expected = "delta-charlie-alpha-golf-foxtrot-echo"
    assert phrase == expected, f"Phrase mismatch! Expected {expected}, got {phrase}"
