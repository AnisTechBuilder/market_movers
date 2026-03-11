# Market Movers CLI

A command-line utility that fetches near real-time stock market data, calculates percentage changes from the previous close, and displays a color-coded table in the terminal.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Internet connection (for fetching live stock data)

## Setup

### macOS / Linux

```bash
# Clone the repository
git clone https://github.com/your-username/market_movers.git
cd market_movers

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Windows (Command Prompt)

```cmd
:: Clone the repository
git clone https://github.com/your-username/market_movers.git
cd market_movers

:: Create virtual environment
python -m venv .venv

:: Activate virtual environment
.venv\Scripts\activate.bat

:: Install dependencies
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
# Clone the repository
git clone https://github.com/your-username/market_movers.git
cd market_movers

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

> **Note (Windows PowerShell):** If you get an execution policy error, run the following first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

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

### Example Output

```
          Market Movers  |  2026-03-10 17:24:37 UTC
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Symbol        ┃ Current Price ┃ Previous Close ┃ % Change ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ RELIANCE.NS   │      1,408.80 │       1,418.60 │ -0.69% ▼ │
│ SBIN.NS       │      1,112.20 │       1,101.00 │ +1.02% ▲ │
│ INFY.NS       │      1,295.60 │       1,315.80 │ -1.54% ▼ │
│ TCS.NS        │      2,513.10 │       2,527.80 │ -0.58% ▼ │
│ HDFCBANK.NS   │        849.45 │         839.10 │ +1.23% ▲ │
└───────────────┴───────────────┴────────────────┴──────────┘
```

## CLI Options

| Flag | Short | Description |
|------|-------|-------------|
| `--tickers` | `-t` | Comma-separated ticker symbols (default: RELIANCE.NS, SBIN.NS, INFY.NS, TCS.NS, HDFCBANK.NS, BHARTIARTL.NS, ITC.NS, ICICIBANK.NS) |
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

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `python3` not found (Windows) | Use `python` instead of `python3`. Windows installs Python as `python`. |
| `source` not recognized (Windows) | Use `.venv\Scripts\activate.bat` (CMD) or `.venv\Scripts\Activate.ps1` (PowerShell) instead of `source`. |
| PowerShell execution policy error | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `pip` not found | Try `python -m pip install -r requirements.txt` |
| Ticker shows N/A | The symbol may be delisted or temporarily unavailable on Yahoo Finance. |
| No internet error | Ensure you have an active internet connection. The app requires network access to fetch live data. |

## Deactivating the Virtual Environment

```bash
# macOS / Linux
deactivate

# Windows (CMD / PowerShell)
deactivate
```

## License

MIT
