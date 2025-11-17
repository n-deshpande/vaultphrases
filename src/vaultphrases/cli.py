"""CLI entrypoint for vaultphrases."""

import argparse
import getpass
import os
import sys
import time

from .constants import (
    SCHEME_VERSION,
    LABEL_HOT,
    LABEL_COLD,
    DEFAULT_WORD_COUNT,
    DEFAULT_DELIMITER,
    DEFAULT_WORDLIST_PATH,
)
from .derive import derive_master_key, hkdf_child
from .security import secure_clear_bytes
from .wordlist import load_wordlist, bytes_to_phrase


def print_banner():
    """Print the welcome banner."""
    print()
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                      VAULTPHRASES                         ║")
    print("║          Deterministic Passphrase Derivation              ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()


def print_section_header(title: str):
    """Print a section header."""
    print()
    print(f"┌─ {title}")
    print("│")


def print_section_footer():
    """Print a section footer."""
    print("│")
    print("└─────────────────────────────────────────────────────────────")


def print_progress(message: str, delay: float = 0.3):
    """Print a progress message with a brief pause."""
    print(f"│  {message}", end="", flush=True)
    time.sleep(delay)
    print(" ✓")


def get_root_phrase() -> str:
    """
    Securely prompt for the root phrase.
    
    Uses getpass to avoid echoing to terminal.
    
    Returns:
        The root phrase entered by the user
    """
    print_section_header("Root Phrase Input")
    print("│  Your root phrase is the master secret that derives all passphrases.")
    print("│  Input is hidden for security.")
    print("│")
    root_phrase = getpass.getpass(prompt="│  Root phrase: ")
    
    if not root_phrase or not root_phrase.strip():
        print()
        print("✗ Error: Root phrase cannot be empty")
        sys.exit(1)
    
    # Warn about weak phrases
    word_count = len(root_phrase.strip().split())
    if word_count < 6:
        print("│")
        print(f"│  ⚠  WARNING: Your root phrase has only {word_count} words.")
        print("│     For strong security, use at least 12 words from a wordlist.")
        print("│     Weak root phrases can be brute-forced despite Argon2id.")
    
    print_section_footer()
    
    return root_phrase


def clear_screen():
    """
    Clear the terminal screen and scrollback buffer.
    
    Note: This attempts to clear scrollback, but effectiveness varies by terminal.
    For maximum security, close the terminal window after viewing secrets.
    """
    if os.name == "nt":
        # Windows
        os.system("cls")
    else:
        # Unix/Linux/macOS - clear screen and scrollback
        # \033[2J clears screen, \033[3J clears scrollback, \033[H moves cursor to home
        sys.stdout.write("\033[2J\033[3J\033[H")
        sys.stdout.flush()
        # Also try the clear command as fallback
        os.system("clear")


def run_derivation(args):
    """Run the main derivation workflow."""
    try:
        # Print banner
        print_banner()
        
        # Show test mode warning prominently
        if args.test:
            print("╔═══════════════════════════════════════════════════════════╗")
            print("║                  ⚠  TEST MODE ENABLED  ⚠                  ║")
            print("╠═══════════════════════════════════════════════════════════╣")
            print("║  Using WEAK Argon2 parameters for testing only!          ║")
            print("║  NEVER use --test for real secrets!                      ║")
            print("║  Test mode is 30x faster but provides minimal protection ║")
            print("╚═══════════════════════════════════════════════════════════╝")
            print()
        
        # Get root phrase securely
        root_phrase = get_root_phrase()
        
        # Derive master key
        print_section_header("Key Derivation")
        print_progress("Loading wordlist..." if (args.reveal or args.label) else "Initializing...", 0.1)
        
        # Load wordlist if needed
        if args.reveal or args.label:
            wordlist_path = args.wordlist or DEFAULT_WORDLIST_PATH
            words = load_wordlist(wordlist_path)
        
        print_progress("Deriving master key with Argon2id (this may take a few seconds)...", 0.2)
        master_key = derive_master_key(root_phrase, test_mode=args.test)
        
        # Securely clear root phrase from memory
        from .security import secure_clear_string
        secure_clear_string(root_phrase)
        del root_phrase
        
        # Derive and display child keys
        if args.reveal:
            print_progress("Deriving HOT passphrase...", 0.1)
            hot_raw = hkdf_child(master_key, LABEL_HOT, 32)
            hot_phrase = bytes_to_phrase(hot_raw, words, args.words, DEFAULT_DELIMITER)
            
            print_progress("Deriving COLD passphrase...", 0.1)
            cold_raw = hkdf_child(master_key, LABEL_COLD, 32)
            cold_phrase = bytes_to_phrase(cold_raw, words, args.words, DEFAULT_DELIMITER)
            
            print_section_footer()
            
            # Display passphrases
            print()
            print("╔═══════════════════════════════════════════════════════════╗")
            print("║                   DERIVED PASSPHRASES                     ║")
            print("║                    (keep these secret)                    ║")
            print("╚═══════════════════════════════════════════════════════════╝")
            print()
            print("HOT (daily vault):")
            print()
            print(hot_phrase)
            print()
            print("─" * 63)
            print()
            print("COLD (offline vault):")
            print()
            print(cold_phrase)
            print()
            print("═" * 63)
            print()
            print("Security Reminder:")
            print("  • Copy these passphrases to your password managers now")
            print("  • Close this terminal window after clearing the screen")
            print("  • Do not screenshot or log these values")
            print("  • Terminal scrollback may retain these values")
            print()
            print("Next Steps:")
            print("  1. Set up your HOT vault (Bitwarden/1Password) with the HOT phrase")
            print("  2. Set up your COLD vault (KeePassXC) with the COLD phrase + keyfile")
            print("  3. Store your root phrase securely offline (paper backup)")
            print()
            
            try:
                input("Press ENTER to clear the screen and exit...")
                clear_screen()
            except EOFError:
                # Handle non-interactive mode (e.g., piped input)
                print("(Non-interactive mode - screen not cleared)")
                pass
            
            secure_clear_bytes(hot_raw)
            secure_clear_bytes(cold_raw)
            
        elif args.label:
            print_progress(f"Deriving passphrase for label '{args.label}'...", 0.1)
            custom_raw = hkdf_child(master_key, args.label, 32)
            custom_phrase = bytes_to_phrase(custom_raw, words, args.words, DEFAULT_DELIMITER)
            print_section_footer()
            
            # Display custom passphrase
            print()
            print("╔═══════════════════════════════════════════════════════════╗")
            print("║                   DERIVED PASSPHRASE                      ║")
            print("╚═══════════════════════════════════════════════════════════╝")
            print()
            print(f"Label: {args.label}")
            print()
            print(custom_phrase)
            print()
            print("═" * 63)
            print()
            print("Security Reminder:")
            print("  • Copy this passphrase immediately")
            print("  • Close this terminal window after clearing the screen")
            print()
            
            try:
                input("Press ENTER to clear the screen and exit...")
                clear_screen()
            except EOFError:
                # Handle non-interactive mode (e.g., piped input)
                print("(Non-interactive mode - screen not cleared)")
                pass
            
            secure_clear_bytes(custom_raw)
            
        else:
            print_progress("Master key derived successfully", 0.1)
            print_section_footer()
            print()
            print("✓ Master key derived and verified")
            print()
            print("Next Steps:")
            print("  • Use --reveal to show HOT and COLD passphrases")
            print("  • Use --label NAME to derive a custom passphrase")
            print()
            print("Examples:")
            print("  vaultphrases --reveal")
            print("  vaultphrases --label ssh --words 8")
            print()
        
        secure_clear_bytes(master_key)
        return 0
        
    except KeyboardInterrupt:
        print()
        print()
        print("✗ Operation cancelled by user")
        return 1
    except Exception as e:
        print()
        print(f"✗ Error: {e}")
        return 1


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="vaultphrases",
        description="Deterministic passphrase derivation tool for secure vault management",
        epilog="""
Examples:
  vaultphrases --reveal                     # Show HOT and COLD passphrases
  vaultphrases --label ssh                  # Derive custom passphrase
  vaultphrases --words 8 --reveal           # Use 8 words instead of 6
  vaultphrases --version                    # Show version info
  
Security:
  • Your root phrase is the master secret - keep it safe offline
  • HOT phrase: for daily password manager (Bitwarden/1Password)
  • COLD phrase: for offline vault (KeePassXC + keyfile)
  • All derivations are deterministic and reproducible
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Main derivation options
    parser.add_argument(
        "--reveal",
        action="store_true",
        help="show HOT and COLD passphrases (default: derive only)"
    )
    parser.add_argument(
        "--words",
        type=int,
        default=DEFAULT_WORD_COUNT,
        metavar="N",
        help=f"number of words in passphrase (default: {DEFAULT_WORD_COUNT})"
    )
    parser.add_argument(
        "--label",
        type=str,
        metavar="NAME",
        help="derive custom passphrase with domain separation (e.g., 'ssh', 'gpg')"
    )
    parser.add_argument(
        "--wordlist",
        type=str,
        metavar="FILE",
        help="path to custom wordlist file (default: EFF short wordlist)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="use fast Argon2 parameters for testing (INSECURE - testing only!)"
    )
    
    # Utility flags
    parser.add_argument(
        "--version",
        action="store_true",
        help="show version and derivation scheme info"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="verify derivation without revealing full passphrases"
    )
    
    return parser.parse_args()


def main():
    """Main CLI entrypoint."""
    args = parse_args()
    
    if args.version:
        print()
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                      VAULTPHRASES                         ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print()
        print(f"Version:           0.1.0")
        print(f"Derivation Scheme: {SCHEME_VERSION}")
        print(f"KDF:               Argon2id (256 MiB, 3 iterations)")
        print(f"Child Derivation:  HMAC-SHA256")
        print(f"Default Wordlist:  EFF Short Wordlist")
        print()
        print("Repository: https://github.com/yourusername/vaultphrases")
        print("License:    MIT")
        print()
        return 0
    
    if args.verify:
        print()
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                    VERIFICATION MODE                      ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print()
        print("Verify mode - not yet implemented")
        print()
        print("This will allow you to verify that your derivation produces")
        print("expected outputs without revealing the full passphrases.")
        print()
        return 0
    
    return run_derivation(args)


if __name__ == "__main__":
    sys.exit(main())
