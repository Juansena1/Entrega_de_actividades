from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.exceptions import credentials_exception
from app.infrastructure.database.session import get_db
from app.models import User, UserSession
bearer = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)) -> User:
    if credentials is None: raise credentials_exception()
    try:
        payload = jwt.decode(credentials.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = int(payload.get("sub")); jti = payload.get("jti")
        if not jti: raise credentials_exception()
    except (jwt.PyJWTError, TypeError, ValueError):
        raise credentials_exception()
    session = db.query(UserSession).filter(UserSession.jti == jti, UserSession.user_id == user_id, UserSession.is_active.is_(True), UserSession.revoked_at.is_(None)).first()
    user = db.get(User, user_id)
    now = datetime.utcnow()
    if not session or not user or not user.is_active or session.expires_at <= now or session.last_activity_at <= now - timedelta(minutes=settings.SESSION_INACTIVITY_MINUTES):
        if session:
            session.is_active = False; session.revoked_at = now; db.commit()
        raise credentials_exception()
    if now - session.last_activity_at >= timedelta(minutes=settings.SESSION_ACTIVITY_UPDATE_MINUTES):
        session.last_activity_at = now; db.commit()
    return user

def require_super_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role.value != "SUPER_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para realizar esta operación.")
    return current_user
