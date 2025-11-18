# Contributing to vaultphrases

Thank you for considering contributing to vaultphrases! This is a security-critical tool, so we have specific guidelines to maintain code quality and auditability.

## Code of Conduct

- Be respectful and constructive
- Focus on security and correctness
- Keep the codebase minimal and auditable
- Document all changes thoroughly

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/vaultphrases.git
cd vaultphrases

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e .
pip install pytest

# Run tests
pytest tests/ -v
```

## Coding Standards

### Security First

1. **Never log sensitive data** - No root phrases, keys, or passphrases in logs
2. **No network operations** - This tool must remain 100% offline
3. **Minimal dependencies** - Only add dependencies if absolutely necessary
4. **Audit-friendly code** - Keep code simple, clear, and well-documented
5. **Memory clearing** - Clear sensitive data from memory when done
6. **Input validation** - Validate all user inputs

### Code Style

1. **Follow PEP 8** - Use standard Python style
2. **Type hints** - Add type hints to all function signatures
3. **Docstrings** - Document all functions with clear docstrings
4. **Comments** - Explain complex logic, especially cryptographic operations
5. **Keep it simple** - Prefer clarity over cleverness

### Testing

1. **Write tests** - All new features must have tests
2. **Test determinism** - Verify reproducibility
3. **Test edge cases** - Empty inputs, invalid data, etc.
4. **Test security** - Verify domain separation, key independence
5. **Run all tests** - `pytest tests/ -v` must pass

## Pull Request Process

1. **Fork the repository** and create a feature branch
2. **Write clear commit messages** - Explain what and why
3. **Add tests** for new functionality
4. **Update documentation** - README, SECURITY.md, etc.
5. **Run tests** - Ensure all tests pass
6. **Check diagnostics** - No linting errors
7. **Keep PRs focused** - One feature/fix per PR
8. **Update CHANGELOG.md** - Add entry under [Unreleased]

## What to Contribute

### Welcome Contributions

- Bug fixes
- Documentation improvements
- Test coverage improvements
- Security enhancements
- Performance improvements (without compromising security)
- Usability improvements

### Requires Discussion First

- New features (open an issue first)
- Cryptographic changes (requires security review)
- Breaking changes (must be justified)
- New dependencies (must be essential)

### Not Accepted

- Features that compromise security
- Network operations
- Telemetry or analytics
- Unnecessary complexity
- Bloat or feature creep

## Security Considerations

### Cryptographic Changes

Any changes to cryptographic operations require:

1. **Security justification** - Why is this change needed?
2. **Backward compatibility** - Will old passphrases still work?
3. **Test vectors** - Provide known input/output pairs
4. **Documentation** - Update SECURITY.md with changes
5. **Version bump** - Increment scheme version if needed

### Memory Safety

When handling sensitive data:

1. Use `secure_clear_bytes()` and `secure_clear_string()`
2. Minimize lifetime of sensitive variables
3. Use `bytes` instead of `str` where possible
4. Avoid string operations on secrets
5. Test that memory clearing works

### Input Validation

All user inputs must be validated:

1. Check for empty/null values
2. Validate file paths exist
3. Check wordlist format
4. Warn about weak root phrases
5. Sanitize error messages (don't leak secrets)

## Testing Guidelines

### Test Structure

```python
def test_feature_name():
    """Test that feature does X correctly."""
    # Arrange
    input_data = "test input"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

### Test Categories

1. **Unit tests** - Test individual functions
2. **Integration tests** - Test complete workflows
3. **Reproducibility tests** - Verify determinism
4. **Security tests** - Verify domain separation, independence
5. **Edge case tests** - Empty inputs, invalid data

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_derive.py -v

# Run specific test
pytest tests/test_derive.py::test_derive_master_key_deterministic -v

# Run with coverage
pytest tests/ --cov=vaultphrases --cov-report=html
```

## Documentation Guidelines

### Code Documentation

1. **Docstrings** - All functions must have docstrings
2. **Type hints** - All parameters and returns must be typed
3. **Examples** - Include usage examples where helpful
4. **Security notes** - Document security considerations

### User Documentation

1. **README.md** - Keep examples up to date
2. **SECURITY.md** - Document threat model and limitations
3. **INSTALL.md** - Keep installation instructions current
4. **CHANGELOG.md** - Document all changes

## Release Process

1. Update version in `pyproject.toml` and `__init__.py`
2. Update CHANGELOG.md (move [Unreleased] to [X.Y.Z])
3. Run full test suite
4. Build package: `python -m build`
5. Test installation: `pip install dist/vaultphrases-X.Y.Z-py3-none-any.whl`
6. Create git tag: `git tag -a vX.Y.Z -m "Release X.Y.Z"`
7. Push tag: `git push origin vX.Y.Z`
8. (Optional) Publish to PyPI: `python -m twine upload dist/*`

## Questions?

- Open an issue for questions
- Tag issues with appropriate labels
- Be patient - this is a volunteer project

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
