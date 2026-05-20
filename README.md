# AIxStock

AIxStock is a stock market evaluation and prediction system powered by Large Language Models (LLMs). It synthesizes multiple input sources — historical data, human-defined strategies, and hard-coded rules — to generate actionable market insights.

## Overview

Traditional stock analysis tools rely on fixed algorithms or manual interpretation. AIxStock takes a different approach: it feeds diverse signal sources into an LLM, which reasons across all inputs to produce a unified prediction or evaluation.

```
┌─────────────────────────────────────────┐
│              Input Sources              │
│                                         │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │  Historical │  │ Human Invention  │  │
│  │  Stock Data │  │   Strategies     │  │
│  └──────┬──────┘  └────────┬─────────┘  │
│         │                  │            │
│  ┌──────┴──────────────────┴─────────┐  │
│  │       Hard-coded Strategies       │  │
│  │       (+ more inputs ...)         │  │
│  └──────────────────┬────────────────┘  │
└─────────────────────│───────────────────┘
                      ▼
            ┌─────────────────┐
            │   LLM Engine    │
            └────────┬────────┘
                     ▼
            ┌─────────────────┐
            │  Prediction /   │
            │   Evaluation    │
            └─────────────────┘
```

## Input Parameters

### 1. Historical Stock Market Data
Raw time-series market data including OHLCV (Open, High, Low, Close, Volume), technical indicators, and historical trends. This forms the factual foundation for the LLM's analysis.

Data source from [AKShare](https://akshare.akfamily.xyz/introduction.html)

### 2. Human Invention Strategies
User-defined trading strategies and hypotheses expressed in natural language or structured format. These allow domain experts to encode their intuition and experience into the system.

### 3. Hard-coded Strategies
Pre-defined rule-based strategies (e.g., moving average crossovers, RSI thresholds, support/resistance levels) that serve as baseline signals alongside LLM reasoning.

### 4. Additional Inputs *(extensible)*
The system is designed to accommodate further signal types, such as:
- News sentiment and macroeconomic indicators
- Earnings reports and financial statements
- Social media and market sentiment signals

## Output

The LLM synthesizes all provided inputs and returns:
- A market **evaluation** of current conditions
- A **prediction** with directional bias (bullish / bearish / neutral)
- Supporting **reasoning** explaining the conclusion

## Project Structure

```
AIxStock/
├── backend/
│   ├── app.py                      # FastAPI app factory (create_app)
│   ├── main.py                     # Entry point — runs uvicorn via backend/app.py
│   ├── logging_config.py           # Logging setup
│   ├── routers/
│   │   ├── stock.py                # /stock/info and /stock/history endpoints
│   │   ├── agent.py                # /agent/* endpoints (optional, loaded if available)
│   │   └── performance.py          # /performance/* endpoints (optional)
│   └── services/
│       ├── data_source/
│       │   ├── akshare_data_source.py  # AKShareDataService — upstream API wrapper
│       │   └── tests/
│       └── store/
│           └── tests/
├── local_storage/                  # Append-only local cache (Parquet + metadata.json)
├── frontend/                       # UI layer (not yet implemented)
├── pyproject.toml                  # Project dependencies (managed by uv)
└── README.md
```

## API Endpoints

The backend exposes a FastAPI server with interactive docs at `http://localhost:8888/docs`.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info and enabled features |
| GET | `/health` | Health check |
| GET | `/system/info` | Architecture and module status |
| GET | `/stock/info` | Stock metadata (name, sector, listing info) |
| GET | `/stock/history` | Daily OHLCV trading history |
| POST | `/agent/chat` | Agent chat (if agent module available) |
| GET | `/agent/status` | Agent module status |
| GET | `/agent/history/{user_id}` | User interaction history |
| GET | `/agent/memory/{user_id}` | User memory summary |
| GET | `/agent/tools` | Available agent tools |

### Stock endpoint parameters

Both `/stock/info` and `/stock/history` accept:
- `stock_code` — 6-digit A-share code (e.g. `601127` for Shanghai, `000001` for Shenzhen)
- `date` — trading date in `YYYYMMDD` format
- `timeout` — per-source timeout in seconds (default: 5, range: 1–30)

## Getting Started

### Prerequisites
- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd AIxStock

# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate
```

### Run backend server

```bash
# Development (with auto-reload via DEBUG env var)
DEBUG=true uv run python -m backend.main

# Production
uv run python -m backend.main
```

## Local Debugging

### 1. Start in debug mode

```bash
DEBUG=true uv run python -m backend.main
```

`DEBUG=true` sets uvicorn's `reload=True`, so the server automatically restarts on any source file change — no manual restarts needed.

### 2. Explore the API interactively

Once the server is running, open the auto-generated docs in your browser:

- **Swagger UI** — `http://localhost:8888/docs` (try requests directly from the browser)
- **ReDoc** — `http://localhost:8888/redoc` (clean reference view)

Example request to test the stock info endpoint:

```
GET http://localhost:8888/stock/info?stock_code=601127&date=20260512
```

### 3. Monitor logs

Logs are written to two rotating files under `log/`:

```bash
# Stream all application logs
tail -f log/application.log

# Stream errors only
tail -f log/error.log
```

Log format: `YYYY-MM-DD HH:MM:SS - <module> - <LEVEL> - <message>`

### 4. Run tests

```bash
# Run all tests
uv run pytest

# Run a specific test directory with verbose output
uv run pytest backend/services/data_source/tests/ -v

# Run a single test by name
uv run pytest -k "test_name"
```

### 5. Check module availability

The agent and performance modules load conditionally at startup. Check the server logs or call `/system/info` to see which modules are active:

```bash
curl http://localhost:8888/system/info | python3 -m json.tool
```

### 6. Dependency audit

```bash
uv run pip-audit
```

## License

See [LICENSE](LICENSE) for details.
