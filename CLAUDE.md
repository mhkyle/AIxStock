# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AIxStock is an LLM-powered stock market evaluation and prediction system. It ingests multiple signal sources (historical data, human strategies, hard-coded rules) and feeds them to an LLM to produce market predictions. Data is sourced from [AKShare](https://akshare.akfamily.xyz/introduction.html).

## Package Management

This project uses **uv** exclusively. Never use `pip` directly.

```bash
uv add <package>               # add runtime dependency
uv add --dev <package>         # add dev dependency
uv sync                        # install all dependencies from uv.lock
uv run <command>               # run a command inside the venv
```

## Running Tests

```bash
uv run pytest                                          # all tests
uv run pytest backend/services/datas/tests/ -v        # specific directory
uv run pytest -k "test_falls_back"                    # single test by name
```

Tests live under `backend/services/datas/tests/`. `testpaths = ["backend"]` is set in `pyproject.toml`.

## Security Audit

```bash
uv run pip-audit                # check all dependencies for known CVEs
```

## Architecture

```
AIxStock/
├── backend/                   # Data fetching and business logic (Python)
│   └── services/
│       └── datas/
│           ├── akshare_input.py   # AKShareDataService — upstream API wrapper
│           └── tests/             # pytest tests for all service methods
├── local_storage/             # Append-only local cache for historical data
│   └── (Parquet files + metadata.json, see local_storage/README.md)
├── frontend/                  # UI layer (not yet implemented)
├── main.py                    # Entry point
└── pyproject.toml
```

### Data Flow

1. **Backend (`AKShareDataService`)** fetches stock data from AKShare with a primary source (东方财富) and XQ fallback. Returns `None` when both sources fail — callers must handle this.
2. **`local_storage`** acts as a cache: reads from disk first, fetches from upstream only for missing date ranges, then appends and updates `metadata.json`. Parquet files are append-only; rows are never mutated.
3. **Frontend** (planned) will consume backend services and display predictions.
4. **LLM engine** (planned) will synthesize all inputs into a prediction.

### Key Conventions

- `AKShareDataService` is instantiated with `date` (format `"YYYYMMDD"`) and `stock_code` (numeric string, e.g. `"601127"`).
- The XQ (雪球) fallback prefixes stock codes with `"SH"` — this is currently hard-coded for Shanghai stocks only. Shenzhen stocks (`SZ` prefix) are not yet handled.
- All A-share timestamps use **CST (UTC+8)**.
- `date` strings for `akshare` use `"YYYYMMDD"` format; date range slicing uses `"YYYY-MM-DD"`.

### Naming Conventions

Per project standards (see `~/.claude/CLAUDE.md`):
- Variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Indentation: 2 spaces
