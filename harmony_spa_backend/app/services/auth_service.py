from datetime import datetime, timedelta
from uuid import uuid4
import jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import verify_password
from app.models import User, UserSession
from app.repositories.user_repository import UserRepository

def authenticate_user(db: Session, email: str, password: str, ip_address: str | None = None, user_agent: str | None = None):
    user = UserRepository.get_by_email(db, email.lower())
    if not user or not user.is_active or not verify_password(password, user.password_hash): return None
    now = datetime.utcnow(); expires = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES); jti = str(uuid4())
    session = UserSession(user_id=user.id, jti=jti, created_at=now, last_activity_at=now, expires_at=expires, is_active=True, ip_address=ip_address, user_agent=user_agent)
    db.add(session); db.commit()
    payload = {"sub": str(user.id), "jti": jti, "iat": now, "exp": expires}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

def revoke_session(db: Session, jti: str):
    session = db.query(UserSession).filter(UserSession.jti == jti, UserSession.is_active.is_(True)).first()
    if session:
        session.is_active = False; session.revoked_at = datetime.utcnow(); db.commit()
