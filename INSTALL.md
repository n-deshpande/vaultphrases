# Installation Guide

## Prerequisites

- Python 3.7 or higher
- pip or pipx

## Installation Methods

### Method 1: pipx (Recommended)

pipx installs the tool in an isolated environment, keeping your system clean:

```bash
# Install pipx if you don't have it
pip install pipx
pipx ensurepath

# Clone and install vaultphrases
git clone https://github.com/n-deshpande/vaultphrases.git
cd vaultphrases
pipx install .
```

### Method 2: pip (System-wide or Virtual Environment)

```bash
# Clone the repository
git clone https://github.com/n-deshpande/vaultphrases.git
cd vaultphrases

# Install system-wide (may require sudo)
pip install .

# Or create a virtual environment first (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install .
```

### Method 3: Development Mode

For contributors or if you want to modify the code:

```bash
git clone https://github.com/n-deshpande/vaultphrases.git
cd vaultphrases
pip install -e .
```

## Wordlist Setup

vaultphrases requires a wordlist file. Download one before first use:

```bash
# Create config directory
mkdir -p ~/.config/vaultphrases

# Download EFF Short Wordlist (1,296 words - recommended)
curl -o ~/.config/vaultphrases/eff_short_wordlist_1.txt \
  https://www.eff.org/files/2016/09/08/eff_short_wordlist_1.txt

# Or download EFF Large Wordlist (7,776 words)
curl -o ~/.config/vaultphrases/eff_large_wordlist.txt \
  https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt
```

## Verify Installation

```bash
# Check version
vaultphrases --version

# View help
vaultphrases --help
```

## First Run

```bash
# Generate HOT and COLD passphrases
vaultphrases --reveal --wordlist ~/.config/vaultphrases/eff_short_wordlist_1.txt
```

You'll be prompted to enter your root phrase. The tool will then derive and display your HOT and COLD passphrases.

## Troubleshooting

### Command not found

If `vaultphrases` is not found after installation:

**With pipx:**
```bash
pipx ensurepath
# Then restart your terminal
```

**With pip:**
```bash
# Check if the script directory is in your PATH
python -m site --user-base
# Add the bin directory to your PATH if needed
```

### Import errors

Make sure argon2-cffi is installed:
```bash
pip install argon2-cffi
```

### Permission errors

If you get permission errors with pip:
```bash
# Use --user flag
pip install --user .

# Or use a virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install .
```

## Uninstallation

```bash
# With pipx
pipx uninstall vaultphrases

# With pip
pip uninstall vaultphrases
```

## Building from Source

To create distribution packages:

```bash
# Install build tools
pip install build

# Build wheel and source distribution
python -m build

# Install from the built wheel
pip install dist/vaultphrases-0.1.0-py3-none-any.whl
```
