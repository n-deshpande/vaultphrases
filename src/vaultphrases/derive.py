"""Core derivation logic for vaultphrases."""

import hmac
import hashlib
from typing import Optional
from argon2 import low_level

from .constants import (
    ARGON2_MEMORY_COST,
    ARGON2_TIME_COST,
    ARGON2_PARALLELISM,
    ARGON2_HASH_LENGTH,
    ARGON2_TEST_MEMORY_COST,
    ARGON2_TEST_TIME_COST,
    ARGON2_TEST_PARALLELISM,
    ROOT_SALT_V1,
)
from .security import secure_clear_bytes, secure_clear_string
from .utils import normalise_phrase

def derive_master_key(root_phrase: str, test_mode: bool = False) -> bytes:
    """
    Derive the master key from a root phrase using Argon2id.
    
    This is the first step in the deterministic derivation chain.
    The master key is used to derive all child keys via HMAC-SHA256.
    
    Args:
        root_phrase: The user's root phrase (will be normalised)
        test_mode: If True, use faster parameters for testing
        
    Returns:
        32-byte master key
        
    Security notes:
    - Root phrase is normalised (trimmed, lowercased, whitespace collapsed)
    - Argon2id provides memory-hard KDF protection
    - Best-effort memory clearing after derivation
    """
    # Normalise the root phrase
    normalised_phrase = normalise_phrase(root_phrase)
    
    # Convert to bytes for Argon2
    phrase_bytes = normalised_phrase.encode('utf-8')
    
    try:
        # Select parameters based on mode
        if test_mode:
            memory_cost = ARGON2_TEST_MEMORY_COST
            time_cost = ARGON2_TEST_TIME_COST
            parallelism = ARGON2_TEST_PARALLELISM
        else:
            memory_cost = ARGON2_MEMORY_COST
            time_cost = ARGON2_TIME_COST
            parallelism = ARGON2_PARALLELISM
        
        # Derive master key using Argon2id
        master_key = low_level.hash_secret_raw(
            secret=phrase_bytes,
            salt=ROOT_SALT_V1,
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
            hash_len=ARGON2_HASH_LENGTH,
            type=low_level.Type.ID,  # Argon2id
        )
        
        return master_key
        
    finally:
        # Best-effort memory clearing
        secure_clear_string(normalised_phrase)
        secure_clear_bytes(phrase_bytes)


def hkdf_child(master_key: bytes, label: str, out_len: int = 32) -> bytes:
    """
    Derive a child key from the master key using HMAC-SHA256.
    
    Simple HKDF-style derivation for domain separation.
    
    Args:
        master_key: Master key from derive_master_key()
        label: Domain label (e.g., "HOT_PHRASE_V1", "COLD_PHRASE_V1")
        out_len: Output length in bytes (default: 32)
        
    Returns:
        Child key of specified length
    """
    label_bytes = label.encode('utf-8')
    return hmac.new(master_key, label_bytes, hashlib.sha256).digest()[:out_len]


# Backwards compatibility alias
derive_child_key = hkdf_child
