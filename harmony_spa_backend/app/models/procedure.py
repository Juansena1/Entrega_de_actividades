from decimal import Decimal
from sqlalchemy import Boolean, CheckConstraint, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.base import Base
class Procedure(Base):
    __tablename__ = "procedures"
    __table_args__ = (CheckConstraint("price >= 0", name="ck_procedures_price_nonnegative"), CheckConstraint("duration_minutes > 0", name="ck_procedures_duration_positive"))
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sessions: Mapped[list["ProcedureSession"]] = relationship(back_populates="procedure", cascade="all, delete-orphan", order_by="ProcedureSession.session_number")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="procedure")
