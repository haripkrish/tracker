from app.schemas.article import ArticleCreate, ArticleUpdate
from tests.utils.common import get_random_int, get_random_string


def get_random_article() -> ArticleCreate:
    return ArticleCreate(name=get_random_string(5))


def get_random_update_article() -> ArticleUpdate:
    return ArticleUpdate(id=get_random_int(), name=get_random_string(5))
