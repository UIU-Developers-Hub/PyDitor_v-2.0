# run.py
import uvicorn
import logging
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Run the FastAPI server"""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()