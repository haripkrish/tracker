from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.article import ArticleCreate
from app.schemas.article_sku import ArticleSkuCreate, ArticleSkuUpdate
from tests.utils.common import get_random_string, get_random_price


def create_random_article(override_get_db: Session) -> ArticleCreate:
    article_in = ArticleCreate(
        name=get_random_string(10),
        description=get_random_string(50)
    )
    return crud.article.create(db=override_get_db, obj_in=article_in)


def get_random_article_sku(article_id: str) -> ArticleSkuCreate:
    return ArticleSkuCreate(
        sku=get_random_string(10),
        price=get_random_price(),
        article_id=article_id
    )


def get_random_update_article_sku(article_id: str) -> ArticleSkuUpdate:
    return ArticleSkuUpdate(
        sku=get_random_string(10),
        price=get_random_price(),
        article_id=article_id
    )


def test_get_article_sku(override_get_db: Session) -> None:
    article = create_random_article(override_get_db)
    article_sku_in = get_random_article_sku(article_id=article.id)
    article_sku = crud.article_sku.create(db=override_get_db, obj_in=article_sku_in)
    article_sku_by_id = crud.article_sku.get(db=override_get_db, id=article_sku.id)
    assert article_sku_by_id
    assert article_sku.sku == article_sku_by_id.sku
    assert article_sku.price == article_sku_by_id.price
    assert article_sku.article_id == article_sku_by_id.article_id
    assert jsonable_encoder(article_sku) == jsonable_encoder(article_sku_by_id)


def test_get_multi_article_sku(override_get_db: Session) -> None:
    article = create_random_article(override_get_db)
    article_sku_in = get_random_article_sku(article_id=article.id)
    crud.article_sku.create(db=override_get_db, obj_in=article_sku_in)
    article_skus = crud.article_sku.get_multi(override_get_db)
    assert len(article_skus) >= 1


def test_create_article_sku(override_get_db: Session) -> None:
    article = create_random_article(override_get_db)
    article_sku_in = get_random_article_sku(article_id=article.id)
    article_sku = crud.article_sku.create(db=override_get_db, obj_in=article_sku_in)
    assert article_sku.sku == article_sku_in.sku
    assert article_sku.price == article_sku_in.price
    assert article_sku.article_id == article_sku_in.article_id
    assert article_sku.id is not None


def test_update_article_sku(override_get_db: Session) -> None:
    article = create_random_article(override_get_db)
    article_sku_in = get_random_article_sku(article_id=article.id)
    article_sku = crud.article_sku.create(db=override_get_db, obj_in=article_sku_in)
    article_update = create_random_article(override_get_db)
    article_sku_update = get_random_update_article_sku(article_id=article_update.id)
    article_sku_updated = crud.article_sku.update(db=override_get_db, db_obj=article_sku, obj_in=article_sku_update)
    assert article_sku.id == article_sku_updated.id


def test_remove_article_sku(override_get_db: Session) -> None:
    article = create_random_article(override_get_db)
    article_sku_in = get_random_article_sku(article_id=article.id)
    article_sku = crud.article_sku.create(db=override_get_db, obj_in=article_sku_in)
    crud.article_sku.remove(db=override_get_db, id=article_sku.id)
    article_sku_removed = crud.article_sku.get(db=override_get_db, id=article_sku.id)
    assert article_sku_removed is None
