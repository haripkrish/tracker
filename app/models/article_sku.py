from sqlalchemy import DECIMAL, ForeignKey
from decimal import Decimal
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.models.article import Article
from app.models.shipment_item import ShipmentItem
from app.db.base import Base
from typing import List


class ArticleSku(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL, nullable=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("article.id"), nullable=False)

    article: Mapped["Article"] = relationship(back_populates="article_sku")
    shipment_item: Mapped[List["ShipmentItem"]] = relationship(back_populates="article_sku")
