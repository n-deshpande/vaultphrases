# Security Policy

## Overview

`vaultphrases` is a security-critical tool for deriving deterministic passphrases. This document outlines the security model, threat assumptions, and responsible disclosure policy.

## Security Model

### What We Protect Against

- **Weak password derivation**: Argon2id provides memory-hard KDF protection
- **Domain separation failures**: HMAC-SHA256 ensures HOT/COLD/custom keys are independent
- **Deterministic reproducibility**: Same root phrase always produces same outputs
- **Offline operation**: No network access, no telemetry, no cloud dependencies
- **Memory exposure (best effort)**: Attempts to clear sensitive data from memory

### What We DON'T Protect Against

The following threats are **explicitly out of scope**:

1. **Physical compromise**: If an attacker has physical access to your machine during or after derivation
2. **Malware/spyware**: Keyloggers, memory scrapers, or other malicious software on your system
3. **Weak root phrases**: If your root phrase is "password123", no amount of Argon2id will save you
4. **Social engineering**: Tricking you into revealing your root phrase
5. **Supply chain attacks**: Malicious modifications to dependencies or the tool itself (audit the code!)
6. **Side-channel attacks**: Timing attacks, power analysis, electromagnetic emissions
7. **Terminal history/scrollback**: Passphrases may persist in terminal buffers despite clearing attempts
8. **Swap files/hibernation**: Sensitive data may be written to disk by the OS
9. **Core dumps**: Crash dumps may contain sensitive data
10. **Python memory management**: Python's garbage collector may leave copies of sensitive data in memory

## Threat Model

### Trust Assumptions

You must trust:
- Your operating system
- Your Python interpreter
- The `argon2-cffi` library
- This tool's source code (please audit it!)
- Your physical security
- Your root phrase generation method

### Single Point of Failure

**Your root phrase is the single secret that anchors everything.** If it's compromised, all derived passphrases are compromised. Protect it accordingly:

- Generate it using a proper wordlist (e.g., EFF Diceware)
- Use at least 12 words (preferably more)
- Store it physically (paper, metal, etc.)
- Never type it on a compromised machine
- Never store it digitally unencrypted

## Known Limitations

### Memory Clearing

Python's memory management makes it impossible to guarantee that sensitive data is cleared from memory. The `secure_clear_bytes()` and `secure_clear_string()` functions are **best-effort only** and may:

- Not work on all Python implementations
- Leave copies in memory due to string interning
- Be defeated by the garbage collector
- Fail silently without indication

**Recommendation**: Run this tool on a trusted, air-gapped machine, and reboot after use if handling extremely sensitive secrets.

### Terminal Security

The `clear_screen()` function attempts to clear the terminal and scrollback buffer, but:

- Effectiveness varies by terminal emulator
- Some terminals don't support scrollback clearing
- Shell history may still contain commands
- Terminal multiplexers (tmux, screen) may retain buffers

**Recommendation**: Close the terminal window after viewing secrets, or use a dedicated terminal session.

### Test Mode

The `--test` flag uses **dramatically weakened** Argon2 parameters (8 MiB memory, 1 iteration) for fast testing. **NEVER use test mode for real secrets.** It provides minimal protection against brute-force attacks.

## Best Practices

### For Users

1. **Generate a strong root phrase**: Use 12+ words from EFF Diceware or similar
2. **Verify wordlist integrity**: Check the fingerprint when loading wordlists
3. **Use production mode**: Never use `--test` for real secrets
4. **Close terminals**: Close the terminal window after viewing passphrases
5. **Physical security**: Store root phrase on paper/metal, not digitally
6. **Audit the code**: This tool is small and auditable - please review it
7. **Air-gap for maximum security**: Run on an offline machine for critical secrets
8. **Reboot after use**: For maximum paranoia, reboot after deriving secrets

### For Developers

1. **Never log sensitive data**: No root phrases, master keys, or derived passphrases in logs
2. **Minimize sensitive data lifetime**: Clear and delete as soon as possible
3. **Avoid string operations on secrets**: Use bytes where possible
4. **No network operations**: This tool must remain 100% offline
5. **Constant-time operations**: Use `hmac.compare_digest()` for comparisons
6. **Validate inputs**: Check for empty/weak root phrases
7. **Clear error messages**: Don't leak sensitive data in exceptions

## Cryptographic Specification

### Derivation Scheme V1

```
Root Phrase (user input)
    ↓ normalize (trim, lowercase, collapse whitespace)
    ↓ Argon2id(secret=phrase, salt="family-password-root-v1", 
    ↓          memory=256MiB, time=3, parallelism=1, len=32)
Master Key (32 bytes)
    ↓ HMAC-SHA256(master_key, "HOT_PHRASE_V1")[:32]
HOT Key (32 bytes)
    ↓ bytes_to_phrase(hot_key, wordlist, word_count, delimiter)
HOT Passphrase (human-friendly)
```

### Parameters

- **Argon2id**: Type.ID (hybrid mode)
- **Memory cost**: 256 MiB (262,144 KiB)
- **Time cost**: 3 iterations
- **Parallelism**: 1 thread
- **Salt**: `b"family-password-root-v1"` (fixed, public)
- **Output length**: 32 bytes

### Domain Separation

Child keys use HMAC-SHA256 with labels:
- `HOT_PHRASE_V1` - Daily vault passphrase
- `COLD_PHRASE_V1` - Offline vault passphrase
- Custom labels for user-defined secrets

## Responsible Disclosure

If you discover a security vulnerability in `vaultphrases`, please:

1. **Do NOT** open a public GitHub issue
2. **Do NOT** discuss it publicly before it's fixed
3. **DO** email the maintainers privately (see README for contact)
4. **DO** provide detailed reproduction steps
5. **DO** allow reasonable time for a fix (90 days suggested)

We will:
- Acknowledge your report within 48 hours
- Provide a fix timeline within 7 days
- Credit you in the security advisory (unless you prefer anonymity)
- Coordinate public disclosure after a fix is available

## Security Checklist for Auditors

When auditing this tool, check:

- [ ] No network operations anywhere in the code
- [ ] No logging of sensitive data (root phrases, keys, passphrases)
- [ ] No writing sensitive data to disk (except intentional user actions)
- [ ] Argon2id parameters match specification
- [ ] HMAC-SHA256 used correctly for child key derivation
- [ ] Input validation on root phrases
- [ ] Memory clearing attempts (even if not guaranteed)
- [ ] Error messages don't leak sensitive data
- [ ] Test mode clearly warned and never used by default
- [ ] Dependencies are minimal and well-known
- [ ] No shell injection vulnerabilities
- [ ] No timing attack vulnerabilities in critical paths

## Version History

- **V1** (2024): Initial derivation scheme with Argon2id + HMAC-SHA256

## License

This security policy is part of the vaultphrases project and is licensed under the same terms (MIT).
