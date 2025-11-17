"""Tests for wordlist functionality."""

import pytest
import tempfile
from pathlib import Path
from vaultphrases.wordlist import load_wordlist, WordlistError, get_default_wordlist_path


def test_load_wordlist_valid():
    """Test loading a valid wordlist."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("11111 apple\n")
        f.write("11112 banana\n")
        f.write("11113 cherry\n")
        temp_path = f.name
    
    try:
        words = load_wordlist(temp_path)
        assert words == ["apple", "banana", "cherry"]
    finally:
        Path(temp_path).unlink()


def test_load_wordlist_with_comments():
    """Test loading wordlist with comments and empty lines."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("# This is a comment\n")
        f.write("\n")
        f.write("11111 apple\n")
        f.write("# Another comment\n")
        f.write("11112 banana\n")
        f.write("\n")
        temp_path = f.name
    
    try:
        words = load_wordlist(temp_path)
        assert words == ["apple", "banana"]
    finally:
        Path(temp_path).unlink()


def test_load_wordlist_file_not_found():
    """Test error when wordlist file doesn't exist."""
    with pytest.raises(WordlistError, match="not found"):
        load_wordlist("/nonexistent/path/wordlist.txt")


def test_load_wordlist_invalid_format():
    """Test that wordlist accepts flexible formats (single word or numbered)."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("11111 apple\n")
        f.write("banana\n")  # Single word format (also valid)
        f.write("11113 cherry\n")
        temp_path = f.name
    
    try:
        words = load_wordlist(temp_path)
        # Should accept both formats
        assert words == ["apple", "banana", "cherry"]
    finally:
        Path(temp_path).unlink()


def test_load_wordlist_empty():
    """Test error when wordlist is empty."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("# Only comments\n")
        f.write("\n")
        temp_path = f.name
    
    try:
        with pytest.raises(WordlistError, match="empty"):
            load_wordlist(temp_path)
    finally:
        Path(temp_path).unlink()


def test_get_default_wordlist_path():
    """Test getting default wordlist path (should be None - user must provide)."""
    path = get_default_wordlist_path()
    assert path is None, "Default wordlist path should be None - users must provide their own wordlist"
