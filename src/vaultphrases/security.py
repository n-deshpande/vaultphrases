"""Security utilities for vaultphrases."""

import ctypes
import sys
from typing import Optional

def secure_clear_string(s: str) -> None:
    """
    Best-effort attempt to clear a string from memory.
    
    Note: Python strings are immutable, so this is not guaranteed to work
    in all cases. This is a defense-in-depth measure.
    """
    try:
        # Get the string's buffer address
        if sys.version_info >= (3, 0):
            # Python 3: strings are Unicode objects
            str_address = id(s)
            str_size = sys.getsizeof(s)
            # Overwrite memory with zeros
            ctypes.memset(str_address, 0, str_size)
    except Exception:
        # If clearing fails, we can't do much about it
        # Don't raise - this is best-effort only
        pass


def secure_clear_bytes(b: Optional[bytes]) -> None:
    """
    Best-effort attempt to clear bytes from memory.
    
    Note: This is not guaranteed to work in all cases due to Python's
    memory management, but it's a defense-in-depth measure.
    
    WARNING: This may cause issues in some Python implementations.
    Use with caution and only when absolutely necessary.
    """
    if b is None:
        return
    
    try:
        # Attempt to overwrite the bytes object's buffer
        # Note: This is implementation-dependent and may not work in all cases
        if isinstance(b, (bytes, bytearray)):
            # For bytearray, we can directly modify
            if isinstance(b, bytearray):
                for i in range(len(b)):
                    b[i] = 0
            else:
                # For bytes, try to access the underlying buffer
                # This is a best-effort approach
                buf_address = id(b) + sys.getsizeof(b) - len(b)
                ctypes.memset(buf_address, 0, len(b))
    except Exception:
        # If clearing fails, we can't do much about it
        # Don't raise - this is best-effort only
        pass

