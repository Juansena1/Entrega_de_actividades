from datetime import date
from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.base import Base
class EmployeeProfile(Base):
    __tablename__ = "employee_profiles"
    __table_args__ = (Index("ix_employee_profiles_available", "is_available"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    job_title: Mapped[str] = mapped_column(String(100), nullable=False)
    specialty: Mapped[str | None] = mapped_column(String(150), nullable=True)
    hire_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    user: Mapped["User"] = relationship(back_populates="employee_profile")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="esthetician", passive_deletes=True)
