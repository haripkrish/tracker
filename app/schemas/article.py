from pydantic import BaseModel, ConfigDict


class ArticleBase(BaseModel):
    name: str | None


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    pass


class ArticleInDBBase(ArticleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Article(ArticleInDBBase):
    pass


class ArticleInDB(ArticleInDBBase):
    pass
