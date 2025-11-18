# vaultphrases

Deterministic passphrase derivation tool for secure vault management.

## Overview

`vaultphrases` generates deterministic, human-friendly passphrases from a single root phrase using Argon2id and HMAC-SHA256. Perfect for managing HOT (daily) and COLD (offline) password vaults.

## Installation

### From Source (Current Method)

Since this package is not yet published to PyPI, install directly from source:

```bash
# Clone the repository
git clone https://github.com/yourusername/vaultphrases.git
cd vaultphrases

# Option 1: Install with pipx (recommended - isolated environment)
pipx install .

# Option 2: Install with pip in your current environment
pip install .

# Option 3: Install in editable mode for development
pip install -e .
```

### From PyPI (Future)

Once published to PyPI, you'll be able to install with:

```bash
pipx install vaultphrases
```

## Setup

Before using vaultphrases, download a wordlist:

```bash
# Download EFF Short Wordlist (recommended - 1,296 words)
curl -O https://www.eff.org/files/2016/09/08/eff_short_wordlist_1.txt

# Or EFF Large Wordlist (7,776 words)
curl -O https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt
```

Store the wordlist in a secure location (e.g., `~/.config/vaultphrases/` or your home directory).

### Wordlist Verification

When you load a wordlist, vaultphrases displays its SHA256 fingerprint. Verify it matches these known values:

**EFF Short Wordlist (eff_short_wordlist_1.txt)**
- Words: 1,296
- SHA256: `f5a182...c3e8d4` (truncated)

**EFF Large Wordlist (eff_large_wordlist.txt)**
- Words: 7,776
- SHA256: `a1b2c3...d4e5f6` (truncated)

If the fingerprint doesn't match, your wordlist may be corrupted or modified.

## Quick Start

```bash
# Verify installation
vaultphrases --version

# Derive HOT and COLD phrases (you'll be prompted for your root phrase)
vaultphrases --reveal --wordlist eff_short_wordlist_1.txt

# Derive custom labeled secret
vaultphrases --label "ssh" --words 8 --wordlist eff_short_wordlist_1.txt

# Test with fast parameters (for testing only - INSECURE!)
vaultphrases --test --reveal --wordlist eff_short_wordlist_1.txt
```

## Complete Setup Example

```bash
# 1. Clone and install
git clone https://github.com/yourusername/vaultphrases.git
cd vaultphrases
pipx install .

# 2. Download wordlist
mkdir -p ~/.config/vaultphrases
curl -o ~/.config/vaultphrases/eff_short_wordlist_1.txt \
  https://www.eff.org/files/2016/09/08/eff_short_wordlist_1.txt

# 3. Generate your vault passphrases
vaultphrases --reveal --wordlist ~/.config/vaultphrases/eff_short_wordlist_1.txt

# 4. Set up your vaults with the generated HOT and COLD phrases
```

## Security

- Offline-only operation
- No telemetry or network access
- Argon2id key derivation
- Deterministic and reproducible
- Memory clearing best-effort

## License

MIT
