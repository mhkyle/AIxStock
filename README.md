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
│   └── services/
│       └── datas/          # Data ingestion and processing
├── pyproject.toml          # Project dependencies (managed by uv)
├── main.py                 # Entry point
└── README.md
```

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

### Run

```bash
uv run main.py
```

## License

See [LICENSE](LICENSE) for details.
