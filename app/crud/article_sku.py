from app.crud.base import CRUDBase
from app.models.article_sku import ArticleSku
from app.schemas.article_sku import ArticleSkuCreate, ArticleSkuUpdate


class CRUDArticleSku(CRUDBase[ArticleSku, ArticleSkuCreate, ArticleSkuUpdate]):
    pass


article_sku = CRUDArticleSku(ArticleSku)
