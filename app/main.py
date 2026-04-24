from fastapi import FastAPI

from app.api.routes import health, notes
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.include_router(health.router)
app.include_router(notes.router)
