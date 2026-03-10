"""CLI argument parsing, orchestration, and Rich terminal output."""

import argparse
import logging
from datetime import datetime, timezone

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from market_movers import __version__
from market_movers.fetcher import TickerResult, fetch_market_data
from market_movers.utils import setup_logging, validate_tickers

logger = logging.getLogger("market_movers")

DEFAULT_TICKERS = "RELIANCE.NS,SBIN.NS,INFY.NS,TCS.NS,HDFCBANK.NS,BHARTIARTL.NS,ITC.NS,ICICIBANK.NS"


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured ArgumentParser with --tickers, --verbose, and --version options.
    """
    parser = argparse.ArgumentParser(
        prog="market-movers",
        description="Fetch and display real-time stock market data with color-coded price changes.",
    )
    parser.add_argument(
        "--tickers",
        "-t",
        type=str,
        default=DEFAULT_TICKERS,
        help="Comma-separated list of ticker symbols (default: major Indian market tickers)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose debug logging to console",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def render_results(results: list[TickerResult], console: Console) -> None:
    """Render ticker results as a Rich table to the console.

    Displays a formatted table with color-coded percentage changes:
    green for positive, red for negative. Errored tickers show "--" values.

    Args:
        results: List of TickerResult objects to display.
        console: Rich Console instance for output.
    """
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    table = Table(
        title=f"Market Movers  |  {timestamp}",
        title_style="bold cyan",
        border_style="bright_black",
        show_lines=True,
    )
    table.add_column("Symbol", style="bold", justify="left")
    table.add_column("Current Price", justify="right")
    table.add_column("Previous Close", justify="right")
    table.add_column("% Change", justify="right")

    errors: list[tuple[str, str]] = []

    for result in results:
        if result.error is not None:
            table.add_row(
                f"[yellow]{result.symbol}[/yellow]",
                "--",
                "--",
                "[yellow]N/A[/yellow]",
            )
            errors.append((result.symbol, result.error))
            continue

        price_str = f"{result.current_price:,.2f}"
        prev_str = f"{result.previous_close:,.2f}"

        if result.pct_change is not None and result.pct_change >= 0:
            change_str = f"[bold green]+{result.pct_change:.2f}% ▲[/bold green]"
        else:
            change_str = f"[bold red]{result.pct_change:.2f}% ▼[/bold red]"

        table.add_row(result.symbol, price_str, prev_str, change_str)

    console.print()
    console.print(table)

    if errors:
        error_lines = "\n".join(f"  • {sym}: {msg}" for sym, msg in errors)
        console.print()
        console.print(
            Panel(
                f"[yellow]{error_lines}[/yellow]",
                title="[bold yellow]Skipped Tickers[/bold yellow]",
                border_style="yellow",
            )
        )


def run(args: argparse.Namespace | None = None) -> int:
    """Main CLI execution flow.

    Orchestrates: parse args → setup logging → validate tickers → fetch → render.

    Args:
        args: Parsed arguments. If None, parses from sys.argv.

    Returns:
        Exit code: 0 for success, 1 for partial failure, 2 for total failure.
    """
    parser = create_parser()
    parsed = parser.parse_args() if args is None else args

    setup_logging(verbose=parsed.verbose)
    console = Console()

    # Validate ticker input
    try:
        tickers = validate_tickers(parsed.tickers)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        logger.error("Invalid ticker input: %s", e)
        return 2

    logger.info("Tickers to fetch: %s", tickers)

    # Fetch market data with spinner
    with console.status("[bold cyan]Fetching market data...[/bold cyan]"):
        results = fetch_market_data(tickers)

    # Check for total failure
    successful = [r for r in results if r.error is None]
    failed = [r for r in results if r.error is not None]

    if not successful:
        # Check if all failures are network-related
        network_errors = any(
            "connect" in (r.error or "").lower() or "network" in (r.error or "").lower()
            for r in failed
        )
        if network_errors:
            console.print(
                "[bold red]Unable to fetch market data. "
                "Please check your internet connection.[/bold red]"
            )
        else:
            console.print(
                "[bold red]Failed to fetch data for all tickers. "
                "Check the log file for details.[/bold red]"
            )
        return 2

    # Render results
    render_results(results, console)

    if failed:
        return 1
    return 0
