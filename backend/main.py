from backend.logging_config import get_logger
import app

logger = get_logger(__name__)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True,log_level="info")