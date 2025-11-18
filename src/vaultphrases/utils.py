"""General utilities for vaultphrases."""


def normalise_phrase(phrase: str) -> str:
    """
    Normalise phrase: trim, lowercase, compress whitespace.
    
    This ensures consistent derivation regardless of input formatting.
    
    Args:
        phrase: Input phrase to normalise
        
    Returns:
        Normalised phrase with single spaces, lowercase, trimmed
        
    Examples:
        >>> normalise_phrase("  Hello   World  ")
        'hello world'
        >>> normalise_phrase("CORRECT HORSE BATTERY STAPLE")
        'correct horse battery staple'
    """
    return " ".join(phrase.strip().lower().split())


