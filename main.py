#!/usr/bin/env python3
"""Market Movers CLI - Entry point.

Usage:
    python main.py
    python main.py -t "TCS.NS, WIPRO.NS"
    python main.py -t "TCS.NS, WIPRO.NS" --verbose
    python main.py --help
"""

import signal
import sys


def _handle_sigint(signum: int, frame: object) -> None:
    """Handle Ctrl+C gracefully with a clean exit."""
    print("\nOperation cancelled by user.")
    sys.exit(130)


def main() -> None:
    """Entry point for the Market Movers CLI."""
    signal.signal(signal.SIGINT, _handle_sigint)

    # Lazy import to keep --help and --version fast
    from market_movers.cli import run

    sys.exit(run())


if __name__ == "__main__":
    main()
