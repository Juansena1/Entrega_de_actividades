from datetime import datetime
from sqlalchemy import Boolean, Computed, DateTime, Enum as SAEnum, Integer, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.base import Base
from app.domain.enums.user_role import UserRole

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
    Index("ix_users_role_active", "role", "is_active"),
    Index("ix_users_last_name", "last_name"),
)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole, name="user_role", values_callable=lambda x: [e.value for e in x]), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    # MySQL genera NULL para roles distintos de SUPER_ADMIN; UNIQUE permite un solo valor 1.
    super_admin_slot: Mapped[int | None] = mapped_column(Integer, Computed("CASE WHEN role = 'SUPER_ADMIN' THEN 1 ELSE NULL END", persisted=True), unique=True)
    sessions: Mapped[list["UserSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    client_profile: Mapped["ClientProfile | None"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    employee_profile: Mapped["EmployeeProfile | None"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
