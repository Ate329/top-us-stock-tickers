"""
US Stock Ticker Fetcher
=======================
Fetches US stock tickers from NASDAQ's stock screener API (covers NYSE, NASDAQ, AMEX),
then saves to CSV files sorted by market capitalization.
"""

import os
import re
import random
import time
import requests
import pandas as pd

# Configuration
NASDAQ_URL = "https://api.nasdaq.com/api/screener/stocks"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}


def fetch_tickers():
    """
    Fetches all US stock tickers from NASDAQ's screener API.
    Includes NYSE, NASDAQ, and AMEX listed stocks.
    """
    print("Fetching tickers from NASDAQ...")
    
    # Random initial delay (0.5-1.5s) to avoid predictable patterns
    time.sleep(random.uniform(0.5, 1.5))
    
    try:
        params = {
            "tableonly": "true",
            "download": "true"
        }
        
        response = requests.get(NASDAQ_URL, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        rows = response.json().get('data', {}).get('rows', [])
        
        if not rows:
            print("  No data returned from API")
            return []
        
        print(f"  Fetched {len(rows)} tickers from API")
        
        # Parse tickers with deduplication
        tickers = []
        seen_symbols = set()
        non_us_count = 0
        duplicate_count = 0
        
        for row in rows:
            # Only include US stocks
            if row.get('country') != 'United States':
                non_us_count += 1
                continue
            
            symbol = row.get('symbol', '').strip()
            
            # Skip duplicates
            if not symbol or symbol in seen_symbols:
                duplicate_count += 1
                continue
            seen_symbols.add(symbol)
            
            tickers.append({
                'symbol': symbol,
                'name': row.get('name', ''),
                'price': parse_number(row.get('lastsale', '')),
                'marketCap': parse_market_cap(row.get('marketCap', '')),
                'volume': parse_int(row.get('volume', '')),
                'industry': row.get('sector', ''),
            })
        
        print(f"  Excluded: {non_us_count} non-US, {duplicate_count} duplicates")
        print(f"  Found {len(tickers)} unique US tickers")
        return tickers
        
    except Exception as e:
        print(f"  Error: {e}")
        return []


def parse_market_cap(s):
    """Parse market cap string like '$1.2T' or '$500M' to numeric."""
    if not s or s == 'N/A':
        return None
    try:
        s = s.replace('$', '').replace(',', '').strip()
        multipliers = {'T': 1e12, 'B': 1e9, 'M': 1e6, 'K': 1e3}
        for suffix, mult in multipliers.items():
            if s.endswith(suffix):
                return float(s[:-1]) * mult
        return float(s)
    except:
        return None


def parse_number(s):
    """Parse price/number string to float."""
    if not s or s == 'N/A':
        return None
    try:
        return float(s.replace('$', '').replace(',', '').strip())
    except:
        return None


def parse_int(s):
    """Parse volume string to integer."""
    if not s or s == 'N/A':
        return None
    try:
        return int(str(s).replace(',', '').strip())
    except:
        return None


def save_files(tickers):
    """Save tickers to organized folder structure."""
    if not tickers:
        print("No tickers to save!")
        return False
    
    # Sort by market cap (descending)
    df = pd.DataFrame(tickers)
    df = df.sort_values('marketCap', ascending=False).reset_index(drop=True)
    
    # Create output directories
    os.makedirs("tickers", exist_ok=True)
    os.makedirs("by_industry", exist_ok=True)
    
    # === GENERAL TICKER LISTS ===
    print("\n📁 Saving ticker lists...")
    
    df.to_csv("tickers/all.csv", index=False)
    print(f"  ✓ tickers/all.csv ({len(df)} rows)")
    
    for n in [50, 100, 200]:
        df.head(n).to_csv(f"tickers/top_{n}.csv", index=False)
        print(f"  ✓ tickers/top_{n}.csv")
    
    # === BY INDUSTRY ===
    print("\n📁 Saving by industry...")
    
    industries = df['industry'].dropna().unique()
    industries = [i for i in industries if i and i.strip()]
    
    for industry in sorted(industries):
        industry_df = df[df['industry'] == industry]
        if len(industry_df) == 0:
            continue
        
        # Safe filename
        safe_name = re.sub(r'[^\w\s-]', '', industry.lower())
        safe_name = re.sub(r'\s+', '_', safe_name.strip())
        
        industry_df.to_csv(f"by_industry/{safe_name}.csv", index=False)
        print(f"  ✓ by_industry/{safe_name}.csv ({len(industry_df)} tickers)")
    
    return True


if __name__ == "__main__":
    print("=" * 50)
    print("US Stock Ticker Update")
    print("=" * 50)
    
    tickers = fetch_tickers()
    
    if not tickers:
        print("\n❌ No data found!")
        exit(1)
    
    if save_files(tickers):
        print("\n" + "=" * 50)
        print("✓ Update completed!")
        print("=" * 50)
    else:
        print("\n❌ Failed to save!")
        exit(1)
