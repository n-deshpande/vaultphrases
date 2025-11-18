# Changelog

All notable changes to vaultphrases will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Wordlist fingerprint display for verification
- Enhanced root phrase strength validation (character count + word count)
- Test mode confirmation prompt to prevent accidental insecure usage
- Comprehensive reproducibility test suite (8 new tests)
- CHANGELOG.md for tracking changes
- PRE_V1_AUDIT.md with detailed code review

### Changed
- Improved root phrase validation with multiple criteria
- Enhanced CLI output with wordlist information

### Fixed
- Removed dead code from utils.py (unused functions with missing imports)
- Removed unused import from security.py
- Cleaned up code for better auditability

## [0.1.0] - 2025-11-18

### Added
- Initial release
- Deterministic passphrase derivation using Argon2id + HMAC-SHA256
- HOT and COLD phrase generation for vault architecture
- Custom labeled secret derivation
- Test mode for faster testing (insecure)
- Comprehensive documentation (README, SECURITY, INSTALL, BUILD_VALIDATION)
- CLI with beautiful output formatting
- Memory clearing best-effort security
- Screen clearing after displaying secrets
- Wordlist loading with flexible format support
- 12 unit tests covering core functionality

### Security
- Argon2id with 256 MiB memory, 3 iterations, parallelism 1
- HMAC-SHA256 for child key derivation
- Offline-only operation (no network access)
- No logging of sensitive data
- Input validation and normalization
- Clear threat model documentation

[Unreleased]: https://github.com/yourusername/vaultphrases/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/vaultphrases/releases/tag/v0.1.0
