from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.domain.enums.user_role import UserRole
from app.models import User, ClientProfile, EmployeeProfile, UserSession
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
class UserService:
    @staticmethod
    def create_user(db: Session, data: UserCreate) -> User:
        if UserRepository.get_by_email(db, data.email):
            raise HTTPException(status_code=409, detail="El correo electrónico ya está registrado.")
        user = User(first_name=data.first_name, last_name=data.last_name, email=data.email.lower(), phone=data.phone, password_hash=hash_password(data.password), role=data.role)
        if data.role == UserRole.CLIENTE:
            user.client_profile = ClientProfile(**data.client_profile.model_dump())
        else:
            user.employee_profile = EmployeeProfile(**data.employee_profile.model_dump())
        db.add(user)
        db.commit(); db.refresh(user)
        return user
    @staticmethod
    def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
        user = UserRepository.get_by_id(db, user_id)
        if not user: raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        values = data.model_dump(exclude_unset=True)
        if "email" in values and values["email"]:
            other = UserRepository.get_by_email(db, values["email"].lower())
            if other and other.id != user_id: raise HTTPException(status_code=409, detail="El correo electrónico ya está registrado.")
            values["email"] = values["email"].lower()
        for key, value in values.items(): setattr(user, key, value)
        user.updated_at = datetime.utcnow()
        db.commit(); db.refresh(user)
        return user
    @staticmethod
    def change_status(db: Session, user_id: int, is_active: bool) -> User:
        user = UserRepository.get_by_id(db, user_id)
        if not user: raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        user.is_active = is_active
        user.updated_at = datetime.utcnow()
        if not is_active:
            now = datetime.utcnow()
            for session in db.query(UserSession).filter(UserSession.user_id == user_id, UserSession.is_active.is_(True)).all():
                session.is_active = False; session.revoked_at = now
        db.commit(); db.refresh(user)
        return user
