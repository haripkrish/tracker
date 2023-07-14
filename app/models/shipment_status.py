from typing import List

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.base import Base
from app.models.shipment import Shipment


class ShipmentStatus(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)

    shipment: Mapped[List["Shipment"]] = relationship(back_populates="shipment_status")
