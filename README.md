# Top US Stock Tickers

Automatically updated CSV lists of US-listed stocks from NASDAQ (grouped by industry), plus a daily S&P 500 constituent list matched against the NASDAQ universe and sorted by market capitalization.

## Folder Structure

```
├── tickers/           # General ticker lists
│   ├── all.csv        # All US stocks (~5,300+)
│   ├── sp500.csv      # Current S&P 500 constituents
│   ├── top_50.csv     # Top 50 by market cap
│   ├── top_100.csv    # Top 100 by market cap
│   └── top_200.csv    # Top 200 by market cap
│
└── by_industry/       # Tickers grouped by industry
    ├── technology.csv
    ├── health_care.csv
    ├── finance.csv
    └── ...            # One file per industry
```

## Update Schedule

Data is automatically updated **daily at 10:00 UTC** (before US market open) via GitHub Actions.

## Data Fields

| Column | Description |
|--------|-------------|
| `symbol` | Stock ticker symbol (e.g., AAPL) |
| `name` | Company name |
| `price` | Last market price |
| `marketCap` | Market capitalization (USD) |
| `volume` | Trading volume |
| `industry` | Sector/industry |

**All files are sorted by market cap (largest first).**

## Data Sources

- `tickers/all.csv`, `tickers/top_50.csv`, `tickers/top_100.csv`, `tickers/top_200.csv`, and `by_industry/*.csv` are generated from the NASDAQ Stock Screener API.
- `tickers/sp500.csv` uses Wikipedia only for S&P 500 membership and then matches those symbols back to NASDAQ rows for the output fields.
- `tickers/sp500.csv` currently contains all matched constituent tickers, which can be more than 500 rows because the index can include multiple share classes.

## How to Use the Data

Other people can use this repo in a few simple ways:

1. Consume the CSVs directly from the raw GitHub URLs without cloning the repository.
2. Use the generated files as static datasets in scripts, notebooks, dashboards, or screeners.
3. Read only the specific file you need, such as the full list, the S&P 500 list, or an industry slice.

Common starting points:

- `tickers/all.csv`: all US tickers in this dataset
- `tickers/sp500.csv`: current S&P 500 constituent tickers
- `tickers/top_50.csv`, `tickers/top_100.csv`, `tickers/top_200.csv`: largest names by market cap
- `by_industry/*.csv`: sector-grouped subsets

Raw GitHub URL examples:

```text
https://raw.githubusercontent.com/Ate329/top-us-stock-tickers/main/tickers/all.csv
https://raw.githubusercontent.com/Ate329/top-us-stock-tickers/main/tickers/sp500.csv
https://raw.githubusercontent.com/Ate329/top-us-stock-tickers/main/tickers/top_50.csv
https://raw.githubusercontent.com/Ate329/top-us-stock-tickers/main/by_industry/technology.csv
```

Example with Python:

```python
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/Ate329/top-us-stock-tickers/main/tickers/sp500.csv"
)
print(df.head())
```

Example with the standard library:

```python
import csv
import urllib.request

url = "https://raw.githubusercontent.com/Ate329/top-us-stock-tickers/main/tickers/top_50.csv"
with urllib.request.urlopen(url) as response:
    rows = list(csv.DictReader(line.decode("utf-8") for line in response))

print(rows[0])
```

## Local Development

```bash
python -m pip install -r requirements.txt
python update_tickers.py
```

## Notes

- NASDAQ provides the output fields used in every generated CSV: `symbol`, `name`, `price`, `marketCap`, `volume`, `industry`.
- Wikipedia is used only to determine current S&P 500 membership.
- Symbol normalization is required for some share classes, such as `BRK.B` <-> `BRK/B` and `BF.B` <-> `BF/B`.
- The GitHub Actions workflow runs the update automatically on weekdays.
