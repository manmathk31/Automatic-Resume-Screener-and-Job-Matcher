import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger(__name__)

def mount_frontend(app: FastAPI) -> None:
    frontend_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "frontend")
    )

    if os.path.exists(frontend_path):
        app.mount(
            "/",
            StaticFiles(directory=frontend_path, html=True),
            name="frontend"
        )
        logger.info(f"Frontend mounted from: {frontend_path}")
    else:
        logger.warning(
            f"Frontend folder not found at: {frontend_path} — "
            f"serving API only"
        )
