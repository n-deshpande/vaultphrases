#!/usr/bin/env python3
"""Demo script showing master key derivation.

⚠️  WARNING: This is a DEMO ONLY!
⚠️  NEVER use this example root phrase for real secrets!
⚠️  NEVER use the displayed keys for actual vault passwords!
⚠️  This script is for educational and testing purposes only.
"""

from src.vaultphrases.derive import derive_master_key, derive_child_key
from src.vaultphrases.constants import LABEL_HOT, LABEL_COLD
from src.vaultphrases.security import secure_clear_bytes

# Example root phrase (in real use, this comes from getpass)
# ⚠️  THIS IS A WELL-KNOWN EXAMPLE - DO NOT USE FOR REAL SECRETS!
root_phrase = "correct horse battery staple"

print("=== VaultPhrases Master Key Derivation Demo ===")
print("⚠️  WARNING: DEMO ONLY - DO NOT USE THESE VALUES FOR REAL SECRETS!\n")
print(f"Root phrase: {root_phrase}")
print("(In production, this would be entered securely via getpass)")
print("(This is a well-known example phrase - never use it for real!)\n")

# Derive master key
print("Deriving master key with Argon2id (test mode)...")
master_key = derive_master_key(root_phrase, test_mode=True)
print(f"Master key (hex): {master_key.hex()}")
print(f"Master key length: {len(master_key)} bytes\n")

# Derive child keys
print("Deriving child keys with HMAC-SHA256...")
hot_key = derive_child_key(master_key, LABEL_HOT)
cold_key = derive_child_key(master_key, LABEL_COLD)

print(f"HOT key (hex):  {hot_key.hex()}")
print(f"COLD key (hex): {cold_key.hex()}\n")

# Verify determinism
print("Verifying determinism...")
master_key2 = derive_master_key(root_phrase, test_mode=True)
print(f"Same master key? {master_key == master_key2}")

hot_key2 = derive_child_key(master_key2, LABEL_HOT)
print(f"Same HOT key? {hot_key == hot_key2}\n")

# Clean up (best effort)
print("Clearing sensitive data from memory...")
secure_clear_bytes(master_key)
secure_clear_bytes(hot_key)
secure_clear_bytes(cold_key)
print("Done!")
