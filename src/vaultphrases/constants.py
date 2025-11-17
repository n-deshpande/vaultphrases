"""Constants for vaultphrases derivation scheme V1."""

# Derivation scheme version
SCHEME_VERSION = "V1"

# Argon2id parameters for production
ARGON2_MEMORY_COST = 256 * 1024  # 256 MiB in KiB
ARGON2_TIME_COST = 3
ARGON2_PARALLELISM = 1
ARGON2_HASH_LENGTH = 32

# Argon2id parameters for testing (fast)
ARGON2_TEST_MEMORY_COST = 8 * 1024  # 8 MiB
ARGON2_TEST_TIME_COST = 1
ARGON2_TEST_PARALLELISM = 1

# Root salt for master key derivation
ROOT_SALT_V1 = b"family-password-root-v1"

# Standard labels for child key derivation
LABEL_HOT = "HOT_PHRASE_V1"
LABEL_COLD = "COLD_PHRASE_V1"

# Default passphrase settings
DEFAULT_WORD_COUNT = 6
DEFAULT_DELIMITER = "-"

# Default wordlist path
import os
from pathlib import Path
_MODULE_DIR = Path(__file__).parent
DEFAULT_WORDLIST_PATH = str(_MODULE_DIR / "data" / "eff_short_wordlist_1.txt")
