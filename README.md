# Top US Stock Tickers

Automatically updated lists of US stock tickers sorted by market capitalization.

## 📁 Folder Structure

```
├── tickers/           # General ticker lists
│   ├── all.csv        # All US stocks (~5,300+)
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

## 🔄 Update Schedule

Data is automatically updated **daily at 10:00 UTC** (before US market open) via GitHub Actions.

## 📋 Data Fields

| Column | Description |
|--------|-------------|
| `symbol` | Stock ticker symbol (e.g., AAPL) |
| `name` | Company name |
| `price` | Last market price |
| `marketCap` | Market capitalization (USD) |
| `volume` | Trading volume |
| `industry` | Sector/industry |

**All files are sorted by market cap (largest first).**

## 🛠️ Local Development

```bash
pip install -r requirements.txt
python update_tickers.py
```

## 📝 Notes

- **Data source**: NASDAQ Stock Screener API
- **Updates**: Daily at 10:00 UTC (exclude weekend)
