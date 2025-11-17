"""General utilities for vaultphrases."""

def normalise_phrase(phrase: str) -> str:
    """Normalise phrase: trim, lowercase, compress whitespace."""
    return " ".join(phrase.strip().lower().split())


def derive_child(master_key: bytes, label: bytes, out_len: int) -> bytes:
    """Derive a child key using HMAC-SHA256(master_key, label)."""
    return hmac.new(master_key, label, hashlib.sha256).digest()[:out_len]


def format_base32_password(raw: bytes, length: int) -> str:
    """
    Convert raw bytes to a Base32 password.

    Base32 uses A–Z and 2–7; padding '=' removed.
    We trim to the desired length.
    """
    s = base64.b32encode(raw).decode("ascii").strip("=")
    return s[:length]


