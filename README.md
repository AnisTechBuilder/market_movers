# Market Movers CLI

A command-line utility that fetches near real-time stock market data, calculates percentage changes from the previous close, and displays a color-coded table in the terminal.

## Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run with default Indian market tickers
python main.py

# Run with custom tickers
python main.py -t "TCS.NS, WIPRO.NS, AAPL"

# Enable verbose debug logging
python main.py -t "TCS.NS" --verbose

# Show help
python main.py --help

# Show version
python main.py --version
```

## CLI Options

| Flag | Short | Description |
|------|-------|-------------|
| `--tickers` | `-t` | Comma-separated ticker symbols (default: RELIANCE.NS, TATAMOTORS.NS, INFY.NS, TCS.NS, HDFCBANK.NS) |
| `--verbose` | `-v` | Enable debug-level logging to console |
| `--version` | | Show version and exit |

## Project Structure

```
market_movers/
├── main.py                 # Entry point
├── market_movers/          # Main package
│   ├── __init__.py         # Package init + version
│   ├── cli.py              # CLI parsing + Rich output
│   ├── fetcher.py          # yfinance data retrieval
│   └── utils.py            # Logging config + helpers
├── logs/                   # Log files (gitignored)
├── requirements.txt        # Dependencies
└── README.md
```

## Logging

All operations are logged to `logs/market_movers.log`. Use `--verbose` to also see debug output in the terminal.

## License

MIT
