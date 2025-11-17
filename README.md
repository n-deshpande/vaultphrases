# vaultphrases

Deterministic passphrase derivation tool for secure vault management.

## Overview

`vaultphrases` generates deterministic, human-friendly passphrases from a single root phrase using Argon2id and HMAC-SHA256. Perfect for managing HOT (daily) and COLD (offline) password vaults.

## Installation

```bash
pipx install vaultphrases
```

## Quick Start

```bash
# Derive HOT and COLD phrases
vaultphrases derive --reveal

# Derive custom labeled secret
vaultphrases derive --label "ssh" --words 8

# Show version
vaultphrases version
```

## Security

- Offline-only operation
- No telemetry or network access
- Argon2id key derivation
- Deterministic and reproducible
- Memory clearing best-effort

## License

MIT
