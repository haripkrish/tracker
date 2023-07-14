from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base
from sqlalchemy.orm import relationship, aliased
from typing import List
from app.models.shipment import Shipment


class Address(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    street_name: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    pincode: Mapped[int] = mapped_column(Integer, nullable=False)

    shipments_as_source: Mapped[List["Shipment"]] = relationship(
        foreign_keys=[Shipment.source_address_id],
        overlaps="source_address"
    )
    destination_as_source: Mapped[List["Shipment"]] = relationship(
        foreign_keys=[Shipment.destination_address_id],
        overlaps="destination_address"
    )


source_address_alias = aliased(Address, name="source_address_alias")
destination_address_alias = aliased(Address, name="destination_address_alias")
