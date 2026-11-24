from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.infrastructure.database.session import get_db
router = APIRouter(tags=["Health"])
@router.get("/health", summary="Verificar que la API está activa")
def health_check(): return {"status": "ok", "service": "harmony-spa-api"}
@router.get("/health/ready", summary="Verificar conexión con MySQL")
def readiness_check(db: Session = Depends(get_db)):
    try: db.execute(text("SELECT 1"))
    except Exception as exc: raise HTTPException(status_code=503, detail="Base de datos no disponible") from exc
    return {"status": "ready", "database": "connected"}
