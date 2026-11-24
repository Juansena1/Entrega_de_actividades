from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.core.exceptions import credentials_exception
from app.infrastructure.database.session import get_db
from app.models import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import authenticate_user, revoke_session
import jwt
from app.core.config import settings
router = APIRouter()
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    token = authenticate_user(db, data.email, data.password, request.client.host if request.client else None, request.headers.get("user-agent"))
    if not token: raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos.", headers={"WWW-Authenticate": "Bearer"})
    return TokenResponse(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)): return current_user
@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from fastapi.security import HTTPAuthorizationCredentials
    auth = request.headers.get("authorization", "")
    token = auth.split(" ", 1)[1] if " " in auth else ""
    try: jti = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]).get("jti")
    except jwt.PyJWTError: raise credentials_exception()
    revoke_session(db, jti)
    return Response(status_code=204)
