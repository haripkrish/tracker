from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.db.base import Base
from sqlalchemy.orm import relationship
from typing import List


class Article(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    article_sku: Mapped[List["ArticleSku"]] = relationship(back_populates="article")
