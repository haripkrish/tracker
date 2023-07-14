from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base
from sqlalchemy.orm import relationship
from typing import List
import uuid


class Shipment(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tracking_id: Mapped[str] = mapped_column(nullable=False, index=True, unique=True)
    carrier_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("carrier.id"), nullable=False, index=True)
    source_address_id: Mapped[int] = mapped_column(ForeignKey("address.id"), nullable=False)
    destination_address_id: Mapped[int] = mapped_column(ForeignKey("address.id"), nullable=False)
    shipment_status_id: Mapped[int] = mapped_column(ForeignKey("shipmentstatus.id"), nullable=False)

    shipment_status: Mapped["ShipmentStatus"] = relationship(back_populates="shipment")

    carrier: Mapped["Carrier"] = relationship(back_populates="shipment")
    source_address: Mapped["Address"] = relationship(foreign_keys=[source_address_id])
    destination_address: Mapped["Address"] = relationship(foreign_keys=[destination_address_id])

    shipment_item: Mapped[List["ShipmentItem"]] = relationship(back_populates="shipment")

