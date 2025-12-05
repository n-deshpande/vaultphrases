# vaultphrases

Deterministic passphrase derivation tool for secure vault management.

## Overview

`vaultphrases` generates deterministic, human-friendly passphrases from a single root phrase using Argon2id and HMAC-SHA256. Perfect for managing a HOT (daily) and COLD (offline) password vaults.

## Requirements

- Python 3.7 or higher
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- A root phrase generated independently (12+ Diceware words recommended)

## Installation

Install from source using [uv](https://docs.astral.sh/uv/):

```bash
# Clone the repository
git clone https://github.com/n-deshpande/vaultphrases.git
cd vaultphrases

# Install with uv (recommended)
uv pip install .

# Or install in editable mode for development
uv pip install -e .
```

If you don't have uv installed, see the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

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
- File SHA256: `8f5ca830b8bffb6fe39c9736c024a00a6a6411adb3f83a9be8bfeeb6e067ae69`
- vaultphrases fingerprint: `8f5ca8...067ae69`

**EFF Large Wordlist (eff_large_wordlist.txt)**
- Words: 7,776
- File SHA256: `addd35536511597a02fa0a9ff1e5284677b8883b83e986e43f15a3db996b903e`
- vaultphrases fingerprint: `addd35...6b903e`

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
git clone https://github.com/n-deshpande/vaultphrases.git
cd vaultphrases
uv pip install .

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
