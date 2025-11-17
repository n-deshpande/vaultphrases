"""Wordlist loading and management."""

import os
from pathlib import Path
from typing import List
import hashlib

class WordlistError(Exception):
    """Raised when wordlist operations fail."""
    pass


def get_default_wordlist_path() -> str:
    """
    Get the path to the default EFF wordlist.
    
    Returns:
        Absolute path to the default wordlist file
    """
    from .constants import DEFAULT_WORDLIST_PATH
    return DEFAULT_WORDLIST_PATH


def load_wordlist(wordlist_path: str) -> List[str]:
    """
    Load a wordlist from a file.
    
    Supports multiple formats:
    - Plain text (one word per line)
    - EFF format (dice_number word)
    - BIP39 format (numbered list)
    
    Args:
        wordlist_path: Path to the wordlist file
        
    Returns:
        List of words from the wordlist
        
    Raises:
        WordlistError: If file doesn't exist or is invalid
    """
    path = Path(wordlist_path).expanduser()
    
    if not path.exists():
        raise WordlistError(f"Wordlist file not found: {wordlist_path}")
    
    if not path.is_file():
        raise WordlistError(f"Wordlist path is not a file: {wordlist_path}")
    
    words = []
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Handle different formats flexibly
                parts = line.split()
                
                if len(parts) == 0:
                    continue
                elif len(parts) == 1:
                    # Plain format: just the word
                    words.append(parts[0])
                else:
                    # EFF/numbered format: take the last part (the word)
                    words.append(parts[-1])
    
    except UnicodeDecodeError as e:
        raise WordlistError(f"Failed to decode wordlist file: {e}")
    except IOError as e:
        raise WordlistError(f"Failed to read wordlist file: {e}")
    
    if not words:
        raise WordlistError("Wordlist is empty")
    
    return words


def words_to_phrase(words: List[str], indices: List[int], delimiter: str = "-") -> str:
    """
    Convert word indices to a passphrase.
    
    Args:
        words: Wordlist to select from
        indices: List of indices into the wordlist
        delimiter: String to join words with
        
    Returns:
        Passphrase string
    """
    selected = [words[i % len(words)] for i in indices]
    return delimiter.join(selected)


def fingerprint_wordlist(words: List[str]) -> str:
    """
    Generate a SHA256 fingerprint of the wordlist.
    
    Args:
        words: List of words to fingerprint
        
    Returns:
        Hex digest of SHA256 hash (truncated to first 6 and last 6 chars)
    """
    
    # Join all words with newlines for consistent hashing
    content = '\n'.join(words).encode('utf-8')
    digest = hashlib.sha256(content).hexdigest()
    
    # Return truncated format: first6...last6
    return f"{digest[:6]}...{digest[-6:]}"


def print_wordlist_info(wordlist_path: str, words: List[str]) -> None:
    """
    Print wordlist information for verification.
    
    Args:
        wordlist_path: Path to the wordlist file
        words: Loaded words
    """
    filename = Path(wordlist_path).name
    fingerprint = fingerprint_wordlist(words)
    
    print(f"Using wordlist: {filename}")
    print(f"Words: {len(words)}")
    print(f"SHA256: {fingerprint}")


def bytes_to_phrase(raw: bytes, words: List[str], word_count: int, delimiter: str = "-") -> str:
    """
    Convert raw bytes to a human-friendly passphrase.
    
    Uses the bytes as a big integer and extracts word indices via modulo.
    
    Args:
        raw: Raw bytes to convert
        words: Wordlist to select from
        word_count: Number of words to generate
        delimiter: String to join words with (default: "-")
        
    Returns:
        Passphrase string
    """
    num = int.from_bytes(raw, "big")
    phrase_words = []
    base = len(words)
    
    for _ in range(word_count):
        idx = num % base
        phrase_words.append(words[idx])
        num //= base
    
    return delimiter.join(phrase_words)
