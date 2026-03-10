"""Logging configuration and helper functions for Market Movers CLI."""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure and return the application logger.

    Sets up dual-output logging:
    - File handler: DEBUG level to logs/market_movers.log (rotating, 5MB max)
    - Console handler: DEBUG if verbose, WARNING otherwise (writes to stderr)

    Args:
        verbose: If True, enable DEBUG-level console output.

    Returns:
        Configured logger instance for 'market_movers'.
    """
    logger = logging.getLogger("market_movers")
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s.%(funcName)s:%(lineno)d | %(message)s"
    )
    console_format = logging.Formatter("%(levelname)s: %(message)s")

    # File handler — always active, captures everything
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        file_handler = RotatingFileHandler(
            log_dir / "market_movers.log",
            maxBytes=5_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    except OSError as e:
        # Fall back to console-only if log directory can't be created
        print(f"Warning: Could not set up file logging: {e}", file=sys.stderr)

    # Console handler — stderr so it doesn't interfere with piped stdout
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.DEBUG if verbose else logging.WARNING)
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    return logger


def validate_tickers(raw_input: str) -> list[str]:
    """Parse and validate a comma-separated ticker string.

    Splits on commas, strips whitespace, and uppercases each symbol.
    Filters out empty strings.

    Args:
        raw_input: Comma-separated ticker symbols, e.g. "TCS.NS, WIPRO.NS".

    Returns:
        List of uppercased, stripped ticker symbols.

    Raises:
        ValueError: If no valid tickers remain after parsing.
    """
    tickers = [t.strip().upper() for t in raw_input.split(",") if t.strip()]
    if not tickers:
        raise ValueError("No valid ticker symbols provided.")
    return tickers
