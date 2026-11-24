from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.domain.enums.user_role import UserRole
class UserRepository:
    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.scalar(select(User).where(User.id == user_id))
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.scalar(select(User).where(User.email == email))
    @staticmethod
    def list_users(db: Session, role: UserRole | None = None, is_active: bool | None = None, skip: int = 0, limit: int = 50):
        query = select(User)
        if role is not None: query = query.where(User.role == role)
        if is_active is not None: query = query.where(User.is_active == is_active)
        return list(db.scalars(query.order_by(User.id.desc()).offset(skip).limit(limit)).all())
