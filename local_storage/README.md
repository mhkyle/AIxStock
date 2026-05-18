# local_storage

Local persistence layer for AIxStock. Stores historical stock market data on disk and incrementally appends new records as time progresses, avoiding redundant API calls to upstream data sources.

## Purpose

Upstream data sources (e.g. AKShare) have rate limits, latency, and availability constraints. `local_storage` acts as a local cache and time-series accumulator:

- **First run**: fetches full historical range from the upstream source and persists it locally.
- **Subsequent runs**: fetches only the missing tail (dates after the last stored record) and appends it to the existing dataset.
- **Reads**: the backend always reads from local storage first, falling back to the upstream source only when data is absent.

```
┌──────────────┐     miss / new dates      ┌─────────────────┐
│   Backend    │ ─────────────────────────► │  Upstream APIs  │
│   Services   │                            │  (AKShare, ...) │
└──────┬───────┘                            └────────┬────────┘
       │  hit                                        │ fetch
       │                                             ▼
       │                                    ┌─────────────────┐
       └───────────────────────────────────►│  local_storage  │
                                            │  (append-only)  │
                                            └─────────────────┘
```

## Storage Layout

```
local_storage/
├── stocks/
│   ├── <stock_code>/
│   │   └── daily.parquet       # Daily OHLCV history, append-only
│   └── ...
├── indices/
│   └── shanghai_summary.parquet
└── metadata.json               # Tracks last-updated timestamp per stock
```

Each stock gets its own subdirectory keyed by stock code (e.g. `601127/`). Data is stored in [Parquet](https://parquet.apache.org/) format for efficient columnar reads and compact disk usage.

## Append Strategy

1. Read `metadata.json` to get `last_updated` date for the requested stock code.
2. If no record exists, fetch the full history from the upstream source.
3. If a record exists, fetch only `[last_updated + 1 day, today]` from upstream.
4. Deduplicate on the date index to guard against overlapping fetches.
5. Append new rows to the existing Parquet file and update `metadata.json`.

## Data Schema

Each daily record contains:

| Column     | Type     | Description                        |
|------------|----------|------------------------------------|
| `date`     | `date`   | Trading date (index)               |
| `open`     | `float`  | Opening price                      |
| `high`     | `float`  | Intraday high                      |
| `low`      | `float`  | Intraday low                       |
| `close`    | `float`  | Closing price                      |
| `volume`   | `int`    | Trading volume (shares)            |
| `turnover` | `float`  | Turnover amount (CNY)              |

## Usage

```python
from local_storage import StockStorage

storage = StockStorage()

# Load (and auto-update) daily history for a stock
df = storage.get_daily("601127")

# Manually trigger an incremental update
storage.update("601127")

# Check last-updated date
storage.last_updated("601127")
```

## Notes

- All timestamps are stored in **CST (UTC+8)** to match A-share market conventions.
- Non-trading days (weekends, public holidays) are **not stored** — gaps in the date index are expected.
- Parquet files are **append-only**; historical rows are never modified.
- `metadata.json` is the source of truth for incremental update logic — do not edit it manually.
