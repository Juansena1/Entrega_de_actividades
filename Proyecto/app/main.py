from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.api.health import router as health_router


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        debug=settings.DEBUG,
        description="API REST del sistema Harmony Spa.",
    )
    
    application.include_router(health_router)
    application.include_router(
        api_router,
        prefix=settings.API_V1_PREFIX,
    )
    
    return application


app = create_application()
