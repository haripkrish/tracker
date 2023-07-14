from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.base import Base


class ShipmentItem(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    shipment_id: Mapped[int] = mapped_column(ForeignKey("shipment.id"), nullable=False, index=True)
    article_sku_id: Mapped[int] = mapped_column(ForeignKey("articlesku.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)

    # relationship
    shipment: Mapped["Shipment"] = relationship(back_populates="shipment_item")
    article_sku: Mapped["ArticleSku"] = relationship(back_populates="shipment_item")
