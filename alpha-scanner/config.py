"""
Alpha Scanner — Local Configuration Overrides
Edit this file to customize the scanner without touching alpha_scanner.py
"""

# ── Universe ──────────────────────────────────────────────────
# Options: 'SP500' | 'NASDAQ100' | ['AAPL','MSFT','NVDA', ...]
UNIVERSE = 'SP500'

# ── Top N candidates to highlight ────────────────────────────
TOP_N = 10

# ── Signal weights (must sum to 1.0) ─────────────────────────
WEIGHTS = {
    'technical':     0.35,
    'earnings':      0.30,
    'institutional': 0.20,
    'sentiment':     0.15,
}

# ── Alpaca Markets API (optional — improves news data) ───────
# Get a free key at: https://alpaca.markets
# Paper-trading keys work fine for market data
ALPACA_API_KEY    = ''
ALPACA_SECRET_KEY = ''

# ── Output paths ─────────────────────────────────────────────
OUTPUT_EXCEL = 'alpha_scan_results.xlsx'
OUTPUT_CSV   = 'alpha_scan_results.csv'
