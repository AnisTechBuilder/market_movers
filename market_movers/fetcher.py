"""Stock market data retrieval and calculations using yfinance."""

import logging
import math
from dataclasses import dataclass

import yfinance as yf

# Suppress yfinance's noisy stderr output for invalid tickers
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

logger = logging.getLogger("market_movers")


@dataclass(frozen=True, slots=True)
class TickerResult:
    """Result of fetching market data for a single ticker.

    Attributes:
        symbol: The ticker symbol (e.g. "TCS.NS").
        current_price: Current/last traded price, or None on error.
        previous_close: Previous closing price, or None on error.
        pct_change: Percentage change from previous close, or None on error.
        error: Error message if fetch failed, or None on success.
    """

    symbol: str
    current_price: float | None = None
    previous_close: float | None = None
    pct_change: float | None = None
    error: str | None = None


def fetch_single_ticker(symbol: str) -> TickerResult:
    """Fetch market data for a single ticker symbol.

    Uses yfinance's fast_info for speed (~200-500ms per ticker).
    Calculates percentage change: ((current - previous) / previous) * 100.

    Args:
        symbol: A yfinance-compatible ticker symbol (e.g. "TCS.NS").

    Returns:
        TickerResult with price data on success, or error message on failure.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.fast_info

        current_price = info.get("last_price") or info.get("lastPrice")
        previous_close = info.get("previous_close") or info.get("previousClose")

        if current_price is None or previous_close is None:
            logger.warning("No price data available for %s", symbol)
            return TickerResult(symbol=symbol, error="No price data available")

        if math.isnan(current_price) or math.isnan(previous_close):
            logger.warning("NaN price data for %s", symbol)
            return TickerResult(symbol=symbol, error="No price data available")

        if previous_close == 0:
            logger.warning("Previous close is zero for %s", symbol)
            return TickerResult(symbol=symbol, error="Previous close is zero")

        pct_change = ((current_price - previous_close) / previous_close) * 100

        logger.debug(
            "%s: current=%.2f, prev_close=%.2f, change=%.2f%%",
            symbol,
            current_price,
            previous_close,
            pct_change,
        )

        return TickerResult(
            symbol=symbol,
            current_price=round(current_price, 2),
            previous_close=round(previous_close, 2),
            pct_change=round(pct_change, 2),
        )

    except Exception as e:
        logger.error("Failed to fetch %s: %s", symbol, e)
        logger.debug("Traceback for %s", symbol, exc_info=True)
        return TickerResult(symbol=symbol, error=str(e))


def fetch_market_data(symbols: list[str]) -> list[TickerResult]:
    """Fetch market data for multiple ticker symbols.

    Iterates sequentially over symbols and fetches data for each.
    Failed tickers are included in results with error messages.

    Args:
        symbols: List of yfinance-compatible ticker symbols.

    Returns:
        List of TickerResult objects, one per input symbol.
        Order matches input order.
    """
    logger.info("Fetching data for %d ticker(s)...", len(symbols))
    results: list[TickerResult] = []

    for i, symbol in enumerate(symbols, start=1):
        logger.info("Fetching %s (%d/%d)...", symbol, i, len(symbols))
        result = fetch_single_ticker(symbol)
        results.append(result)

    successful = sum(1 for r in results if r.error is None)
    logger.info("Completed: %d/%d tickers fetched successfully.", successful, len(symbols))

    return results
