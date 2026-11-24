
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base


class ClientProfile(Base):
    __tablename__ = "client_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    birth_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    emergency_contact_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    emergency_contact_phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    user: Mapped["User"] = relationship(
        back_populates="client_profile"
    )

    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="client",
        passive_deletes=True
    )
