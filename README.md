# vaultphrases

Deterministic passphrase derivation tool for secure vault management.

## Overview

`vaultphrases` generates deterministic, human-friendly passphrases from a single root phrase using Argon2id and HMAC-SHA256. Perfect for managing HOT (daily) and COLD (offline) password vaults.

## Installation

```bash
pipx install vaultphrases
```

## Setup

Before using vaultphrases, download a wordlist:

```bash
# Download EFF Short Wordlist (recommended)
curl -O https://www.eff.org/files/2016/09/08/eff_short_wordlist_1.txt

# Or EFF Large Wordlist
curl -O https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt
```

## Quick Start

```bash
# Derive HOT and COLD phrases
vaultphrases --reveal --wordlist eff_short_wordlist_1.txt

# Derive custom labeled secret
vaultphrases --label "ssh" --words 8 --wordlist eff_short_wordlist_1.txt

# Show version
vaultphrases --version
```

## Security

- Offline-only operation
- No telemetry or network access
- Argon2id key derivation
- Deterministic and reproducible
- Memory clearing best-effort

## License

MIT
