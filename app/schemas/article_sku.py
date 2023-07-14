from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ArticleSkuBase(BaseModel):
    sku: str
    article_id: int
    price: Optional[Decimal | None]


class ArticleSkuCreate(ArticleSkuBase):
    pass


class ArticleSkuUpdate(ArticleSkuBase):
    pass



class ArticleSkuInDBBase(ArticleSkuBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ArticleSku(ArticleSkuInDBBase):
    pass


class ArticleSkuInDB(ArticleSkuInDBBase):
    pass
