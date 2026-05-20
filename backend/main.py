from backend.logging_config import get_logger
from backend.app import app
import os

logger = get_logger(__name__)

if __name__ == "__main__":
  import uvicorn

  host = os.getenv("HOST", "0.0.0.0")
  port = int(os.getenv("PORT", "8888"))
  debug = os.getenv("DEBUG", "false").lower() == "true"

  uvicorn.run(
    "backend.app:app",
    host=host,
    port=port,
    reload=debug,
    log_level="info"
  )
