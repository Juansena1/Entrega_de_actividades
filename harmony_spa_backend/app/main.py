from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, version="1.0.0", debug=settings.DEBUG,
              description="API REST del sistema Harmony Spa")
app.include_router(health_router)
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
