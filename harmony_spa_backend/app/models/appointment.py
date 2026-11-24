from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.base import Base
from app.domain.enums.appointment_status import AppointmentStatus
class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = (Index("ix_appointments_start_status", "starts_at", "status"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client_profiles.id", ondelete="RESTRICT"), nullable=False)
    procedure_id: Mapped[int] = mapped_column(ForeignKey("procedures.id", ondelete="RESTRICT"), nullable=False)
    esthetician_id: Mapped[int | None] = mapped_column(ForeignKey("employee_profiles.id", ondelete="SET NULL"), nullable=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[AppointmentStatus] = mapped_column(SAEnum(AppointmentStatus, name="appointment_status", values_callable=lambda x: [e.value for e in x]), default=AppointmentStatus.PENDIENTE, nullable=False)
    cancellation_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cancellation_penalty: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    client: Mapped["ClientProfile"] = relationship(back_populates="appointments")
    procedure: Mapped["Procedure"] = relationship(back_populates="appointments")
    esthetician: Mapped["EmployeeProfile | None"] = relationship(back_populates="appointments")
