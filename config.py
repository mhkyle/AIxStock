import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / 'config.env'
load_dotenv(env_path)

PROJECT_ROOT = os.getenv('PROJECT_ROOT', str(Path(__file__).parent))

class Config:   

    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
