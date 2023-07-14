from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func

from app.db.base_class import Base
from sqlalchemy.orm import relationship
from typing import List
import uuid


class Carrier(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4(), index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    shipment: Mapped[List["Shipment"]] = relationship(back_populates="carrier")
