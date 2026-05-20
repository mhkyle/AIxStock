from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from backend.services.data_source.akshare_data_source import AKShareDataService

router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/info")
async def get_stock_info(
  stock_code: str = Query(..., description="Stock code, e.g. '601127'"),
  date: str = Query(..., description="Date in YYYYMMDD format, e.g. '20260101'"),
  timeout: int = Query(default=5, ge=1, le=30, description="Request timeout in seconds"),
):
  """
  Get single stock info by stock_code and date.

  Returns stock metadata from East Money (东方财富) with XueQiu (雪球) as fallback.
  Returns None when both sources fail.
  """
  service = AKShareDataService(date=date, stock_code=stock_code, timeout_by_seconds=timeout)

  result = service.get_single_stock_info()

  if result is None:
    raise HTTPException(
      status_code=404,
      detail=f"No data found for stock_code={stock_code} on date={date}. Both data sources failed.",
    )

  return JSONResponse(content=result.to_dict(orient="records"))


@router.get("/history")
async def get_stock_history(
  stock_code: str = Query(..., description="Stock code, e.g. '601127'"),
  date: str = Query(..., description="Date in YYYYMMDD format, e.g. '20260101'"),
  timeout: int = Query(default=5, ge=1, le=30, description="Request timeout in seconds"),
):
  """
  Get single-day historical trading data for a stock.

  Uses ak.stock_zh_a_hist with period='daily' for the given date.
  """
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
