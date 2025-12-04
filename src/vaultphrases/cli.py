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
from .wordlist import load_wordlist, bytes_to_phrase, fingerprint_wordlist


# ANSI codes for minimal styling
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
RED = "\033[31m"


def print_header(title: str):
    """Print a minimal header."""
    print(f"\n{BOLD}{title}{RESET}")
    print(f"{DIM}{'─' * 40}{RESET}")


def print_status(message: str, status: str = "ok"):
    """Print a status line."""
    symbol = {"ok": f"{GREEN}✓{RESET}", "warn": f"{YELLOW}!{RESET}", "err": f"{RED}✗{RESET}"}.get(status, " ")
    print(f"  {symbol} {message}")


def get_root_phrase() -> str:
    """Securely prompt for the root phrase."""
    print(f"\n{DIM}Enter your root phrase (input hidden):{RESET}")
    root_phrase = getpass.getpass(prompt="  → ")
    
    if not root_phrase or not root_phrase.strip():
        print(f"\n{RED}✗ Error: Root phrase cannot be empty{RESET}")
        sys.exit(1)
    
    # Validate root phrase strength
    stripped = root_phrase.strip()
    char_count = len(stripped)
    word_counts = [
        len(stripped.split()),
        len(stripped.split('-')),
        len(stripped.split('_')),
        len(stripped.split(',')),
    ]
    word_count = max(word_counts)
    
    if word_count < 6 or char_count < 40:
        print(f"\n{YELLOW}⚠ Weak root phrase detected{RESET}")
        if word_count < 6:
            print(f"  {DIM}→ {word_count} words (recommend 12+){RESET}")
        if char_count < 40:
            print(f"  {DIM}→ {char_count} chars (recommend 60+){RESET}")
    
    return root_phrase


def clear_screen():
    """Clear the terminal screen and scrollback buffer."""
    if os.name == "nt":
        os.system("cls")
    else:
        sys.stdout.write("\033[2J\033[3J\033[H")
        sys.stdout.flush()
        os.system("clear")


def run_derivation(args):
    """Run the main derivation workflow."""
    try:
        print(f"\n{BOLD}vaultphrases{RESET} {DIM}v0.1.0{RESET}")
        
        # Test mode warning
        if args.test:
            print(f"\n{YELLOW}{BOLD}⚠ TEST MODE{RESET} {DIM}— weak Argon2 params, not for real secrets{RESET}")
            if args.reveal or args.label:
                try:
                    confirmation = input(f"  Type 'test' to confirm: ")
                    if confirmation.lower() != "test":
                        print(f"\n{RED}✗ Not confirmed. Remove --test for secure derivation.{RESET}")
                        return 1
                except (EOFError, KeyboardInterrupt):
                    print(f"\n{RED}✗ Cancelled.{RESET}")
                    return 1
        
        # Get root phrase
        root_phrase = get_root_phrase()
        
        # Load wordlist if needed
        words = None
        if args.reveal or args.label:
            wordlist_path = args.wordlist or DEFAULT_WORDLIST_PATH
            if not wordlist_path:
                print(f"\n{RED}✗ No wordlist specified{RESET}")
                print(f"  {DIM}Use --wordlist PATH or download EFF wordlist:{RESET}")
                print(f"  {DIM}https://www.eff.org/files/2016/09/08/eff_short_wordlist_1.txt{RESET}")
                sys.exit(1)
            words = load_wordlist(wordlist_path)
            wordlist_name = os.path.basename(wordlist_path)
            wordlist_fp = fingerprint_wordlist(words)[:16]
            print(f"\n{DIM}Wordlist: {wordlist_name} ({len(words)} words) [{wordlist_fp}…]{RESET}")
        
        # Derive master key
        print(f"\n{DIM}Deriving master key...{RESET}", end="", flush=True)
        master_key = derive_master_key(root_phrase, test_mode=args.test)
        print(f" {GREEN}✓{RESET}")
        
        # Clear root phrase
        from .security import secure_clear_string
        secure_clear_string(root_phrase)
        del root_phrase
        
        if args.reveal:
            # Derive HOT and COLD
            hot_raw = hkdf_child(master_key, LABEL_HOT, 32)
            hot_phrase = bytes_to_phrase(hot_raw, words, args.words, DEFAULT_DELIMITER)
            cold_raw = hkdf_child(master_key, LABEL_COLD, 32)
            cold_phrase = bytes_to_phrase(cold_raw, words, args.words, DEFAULT_DELIMITER)
            
            print_header("Derived Passphrases")
            print(f"\n  {BOLD}HOT{RESET} {DIM}(daily vault){RESET}")
            print(f"  {hot_phrase}")
            print(f"\n  {BOLD}COLD{RESET} {DIM}(offline vault){RESET}")
            print(f"  {cold_phrase}")
            
            print(f"\n{DIM}{'─' * 40}{RESET}")
            print(f"{DIM}• Verify by running again with same root phrase{RESET}")
            print(f"{DIM}• Close terminal after copying{RESET}")
            
            try:
                input(f"\n{DIM}Press ENTER to clear screen...{RESET}")
                clear_screen()
            except EOFError:
                pass
            
            secure_clear_bytes(hot_raw)
            secure_clear_bytes(cold_raw)
            
        elif args.label:
            # Derive custom label
            custom_raw = hkdf_child(master_key, args.label, 32)
            custom_phrase = bytes_to_phrase(custom_raw, words, args.words, DEFAULT_DELIMITER)
            
            print_header(f"Derived: {args.label}")
            print(f"\n  {custom_phrase}")
            
            print(f"\n{DIM}• Verify by running again with same root phrase{RESET}")
            
            try:
                input(f"\n{DIM}Press ENTER to clear screen...{RESET}")
                clear_screen()
            except EOFError:
                pass
            
            secure_clear_bytes(custom_raw)
            
        else:
            print(f"\n{GREEN}✓ Master key derived{RESET}")
            print(f"\n{DIM}Use --reveal for HOT/COLD phrases, or --label NAME for custom{RESET}")
        
        secure_clear_bytes(master_key)
        return 0
        
    except KeyboardInterrupt:
        print(f"\n\n{RED}✗ Cancelled{RESET}")
        return 1
    except Exception as e:
        print(f"\n{RED}✗ Error: {e}{RESET}")
        return 1


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="vaultphrases",
        description="Deterministic passphrase derivation for secure vault management",
        epilog="""
examples:
  vaultphrases --reveal              Show HOT and COLD passphrases
  vaultphrases --label ssh           Derive custom passphrase
  vaultphrases --words 8 --reveal    Use 8 words instead of 6
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--reveal", action="store_true", help="show HOT and COLD passphrases")
    parser.add_argument("--words", type=int, default=DEFAULT_WORD_COUNT, metavar="N", help=f"words in passphrase (default: {DEFAULT_WORD_COUNT})")
    parser.add_argument("--label", type=str, metavar="NAME", help="derive custom passphrase (e.g., 'ssh', 'gpg')")
    parser.add_argument("--wordlist", type=str, metavar="FILE", help="path to wordlist file")
    parser.add_argument("--test", action="store_true", help="fast Argon2 params (INSECURE, testing only)")
    parser.add_argument("--version", action="store_true", help="show version info")
    parser.add_argument("--verify", action="store_true", help="verify derivation (not yet implemented)")
    
    return parser.parse_args()


def main():
    """Main CLI entrypoint."""
    args = parse_args()
    
    if args.version:
        print(f"\n{BOLD}vaultphrases{RESET} v0.1.0")
        print(f"{DIM}Scheme: {SCHEME_VERSION} | KDF: Argon2id (256 MiB, 3 iter) | HMAC-SHA256{RESET}")
        print(f"{DIM}https://github.com/n-deshpande/vaultphrases | MIT{RESET}\n")
        return 0
    
    if args.verify:
        print(f"\n{BOLD}vaultphrases{RESET} {DIM}verify{RESET}")
        print(f"{DIM}Not yet implemented — will verify derivation without full reveal{RESET}\n")
        return 0
    
    return run_derivation(args)


if __name__ == "__main__":
    sys.exit(main())
