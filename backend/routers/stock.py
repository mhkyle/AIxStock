from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Dict, Any

from backend.services.data_source.akshare_data_source import AKShareDataService

router = APIRouter(
  prefix="/stock",
  tags=["Stock Data"],
  responses={
    404: {"description": "Stock data not found"},
    502: {"description": "Upstream data source error"},
  },
)


@router.get(
  "/info",
  summary="Get Stock Metadata",
  description="""
Retrieve comprehensive stock information including company name, listing status,
industry sector, and other fundamental metadata.

**Data Sources (with automatic fallback):**
1. Primary — East Money (东方财富): `ak.stock_individual_info_em()`
2. Fallback — XueQiu (雪球): `ak.stock_individual_basic_info_xq()`

**Stock Code Format:**
- Shanghai: 6-digit numeric code starting with `6xx` (e.g. `601127`)
- Shenzhen: 6-digit numeric code starting with `0xx` or `3xx` (e.g. `000001`)

> **Note:** XueQiu fallback currently only supports Shanghai stocks (`SH` prefix).
  """,
  response_description="List of stock metadata key-value pairs returned by the data source",
  responses={
    200: {
      "description": "Stock metadata retrieved successfully",
      "content": {
        "application/json": {
          "example": [
            {"item": "股票代码", "value": "601127"},
            {"item": "股票简称", "value": "小康股份"},
            {"item": "上市日期", "value": "2007-07-19"},
            {"item": "总市值", "value": "123.45亿"},
            {"item": "流通市值", "value": "98.76亿"},
          ]
        }
      },
    },
    404: {
      "description": "No data found — both data sources failed or returned empty results",
      "content": {
        "application/json": {
          "example": {
            "detail": "No data found for stock_code=601127 on date=20260101. Both data sources failed."
          }
        }
      },
    },
  },
)
async def get_stock_info(
  stock_code: str = Query(
    ...,
    description="6-digit A-share stock code (e.g. `601127` for Shanghai, `000001` for Shenzhen)",
    pattern="^[0-9]{6}$",
    examples=["601127", "000001"],
  ),
  date: str = Query(
    ...,
    description=(
      "Reference date in `YYYYMMDD` format. "
      "Stock data is typically available after market close (15:00 CST). "
      "Weekends and public holidays have no trading data."
    ),
    pattern="^[0-9]{8}$",
    examples=["20260101", "20251231"],
  ),
  timeout: int = Query(
    default=5,
    ge=1,
    le=30,
    description="Per-source request timeout in seconds. Applied independently to each data source.",
    examples=[5],
  ),
):
  service = AKShareDataService(date=date, stock_code=stock_code, timeout_by_seconds=timeout)
  result = service.get_single_stock_info()

  if result is None:
    raise HTTPException(
      status_code=404,
      detail=f"No data found for stock_code={stock_code} on date={date}. Both data sources failed.",
    )

  return JSONResponse(content=result.to_dict(orient="records"))


@router.get(
  "/history",
  summary="Get Daily Trading History",
  description="""
Retrieve OHLCV (Open / High / Low / Close / Volume) trading data for a specific
A-share stock on a given trading day.

**Underlying API:** `ak.stock_zh_a_hist(period='daily')`

**Returned Fields** (column names are in Chinese, as returned by AKShare):

| Field | Description |
|-------|-------------|
| 日期 | Trading date |
| 开盘 | Open price |
| 收盘 | Close price |
| 最高 | High price |
| 最低 | Low price |
| 成交量 | Volume (shares) |
| 成交额 | Turnover (CNY) |
| 振幅 | Amplitude (%) |
| 涨跌幅 | Change (%) |
| 涨跌额 | Change amount (CNY) |
| 换手率 | Turnover rate (%) |

**Prices are unadjusted (前复权 = none).**
  """,
  response_description="List of daily OHLCV records for the requested date",
  responses={
    200: {
      "description": "Trading history retrieved successfully",
      "content": {
        "application/json": {
          "example": [
            {
              "日期": "2026-01-02",
              "开盘": 18.50,
              "收盘": 18.90,
              "最高": 19.10,
              "最低": 18.40,
              "成交量": 12345678,
              "成交额": 233456789.0,
              "振幅": 3.78,
              "涨跌幅": 2.16,
              "涨跌额": 0.40,
              "换手率": 1.23,
            }
          ]
        }
      },
    },
    404: {
      "description": "No trading data found — likely a non-trading day (weekend / holiday) or invalid stock code",
      "content": {
        "application/json": {
          "example": {
            "detail": "No history data found for stock_code=601127 on date=20260101."
          }
        }
      },
    },
    502: {
      "description": "Upstream AKShare API returned an error",
      "content": {
        "application/json": {
          "example": {"detail": "Failed to fetch stock history: <upstream error message>"}
        }
      },
    },
  },
)
async def get_stock_history(
  stock_code: str = Query(
    ...,
    description="6-digit A-share stock code (e.g. `601127` for Shanghai, `000001` for Shenzhen)",
    pattern="^[0-9]{6}$",
    examples=["601127", "000001"],
  ),
  date: str = Query(
    ...,
    description=(
      "Trading date in `YYYYMMDD` format. "
      "Must be a valid trading day — weekends and public holidays return no data. "
      "All timestamps are CST (UTC+8)."
    ),
    pattern="^[0-9]{8}$",
    examples=["20260102", "20251231"],
  ),
  timeout: int = Query(
    default=5,
    ge=1,
    le=30,
    description="Request timeout in seconds.",
    examples=[5],
  ),
):
  service = AKShareDataService(date=date, stock_code=stock_code, timeout_by_seconds=timeout)

  try:
    result = service.get_stock_history()
  except Exception as e:
    raise HTTPException(status_code=502, detail=f"Failed to fetch stock history: {e}")

  if result is None or result.empty:
    raise HTTPException(
      status_code=404,
      detail=f"No history data found for stock_code={stock_code} on date={date}.",
    )

  return JSONResponse(content=result.to_dict(orient="records"))
