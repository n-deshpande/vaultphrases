# vaultphrases Demo

This guide walks through common usage scenarios for vaultphrases.

## Prerequisites

1. Install vaultphrases (see [INSTALL.md](INSTALL.md))
2. Download a wordlist:

```bash
mkdir -p ~/.config/vaultphrases
curl -o ~/.config/vaultphrases/eff_short_wordlist_1.txt \
  https://www.eff.org/files/2016/09/08/eff_short_wordlist_1.txt
```

## Basic Usage

### Generate HOT and COLD Passphrases

```bash
vaultphrases --reveal --wordlist ~/.config/vaultphrases/eff_short_wordlist_1.txt
```

You'll be prompted to enter your root phrase. The tool will derive and display:
- **HOT phrase**: For your daily password manager (We like ProtonPass)
- **COLD phrase**: For your offline vault (e.g. KeePassXC)

### Generate Custom Labeled Passphrase

```bash
vaultphrases --label "ssh" --wordlist ~/.config/vaultphrases/eff_short_wordlist_1.txt
```

This derives a passphrase specifically for SSH keys, using domain separation.

### Adjust Word Count

```bash
# Use 8 words instead of the default 6
vaultphrases --reveal --words 8 --wordlist ~/.config/vaultphrases/eff_short_wordlist_1.txt
```

## Verification Workflow

**Always verify your passphrases before using them!**

1. Run the derivation command 2-3 times
2. Verify you get the exact same output each time
3. If outputs differ, you may have typos in your root phrase

```bash
# Run multiple times to verify
vaultphrases --reveal --wordlist ~/.config/vaultphrases/eff_short_wordlist_1.txt
# (enter root phrase, note output)

vaultphrases --reveal --wordlist ~/.config/vaultphrases/eff_short_wordlist_1.txt
# (enter same root phrase, verify same output)
```

## Recovery Scenario

If you forget your HOT or COLD passphrase:

1. Retrieve your root phrase from physical storage
2. Run vaultphrases with the same wordlist
3. Your passphrases will be regenerated exactly

```bash
vaultphrases --reveal --wordlist ~/.config/vaultphrases/eff_short_wordlist_1.txt
```

## Version Information

```bash
vaultphrases --version
```

Shows:
- Tool version
- Derivation scheme version
- KDF parameters
- Default wordlist info

## Security Notes

- **Never use `--test` for real secrets** - it uses weak parameters
- **Close your terminal** after viewing passphrases
- **Verify wordlist fingerprint** - the tool displays SHA256 when loading
- **Store root phrase offline** - paper or metal backup recommended

## Example Session

```
$ vaultphrases --reveal --wordlist ~/.config/vaultphrases/eff_short_wordlist_1.txt

╔═══════════════════════════════════════════════════════════╗
║                      VAULTPHRASES                         ║
║          Deterministic Passphrase Derivation              ║
╚═══════════════════════════════════════════════════════════╝

┌─ Root Phrase Input
│
│  Your root phrase is the master secret that derives all passphrases.
│  Input is hidden for security.
│
│  Root phrase: ********
│
└─────────────────────────────────────────────────────────────

┌─ Key Derivation
│
│  Loading wordlist... ✓
│  Loaded wordlist: eff_short_wordlist_1.txt (1296 words)
│  SHA256: abc123...def456
│  Deriving master key with Argon2id (this may take a few seconds)... ✓
│  Deriving HOT passphrase... ✓
│  Deriving COLD passphrase... ✓
│
└─────────────────────────────────────────────────────────────

╔═══════════════════════════════════════════════════════════╗
║                   DERIVED PASSPHRASES                     ║
║                    (keep these secret)                    ║
╚═══════════════════════════════════════════════════════════╝

HOT (daily vault):

word1-word2-word3-word4-word5-word6

───────────────────────────────────────────────────────────────

COLD (offline vault):

word7-word8-word9-word10-word11-word12

═══════════════════════════════════════════════════════════════

Press ENTER to clear the screen and exit...
```
