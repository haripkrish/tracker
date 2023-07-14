from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app import crud
from tests.utils.article import get_random_article, get_random_update_article


def test_get_article(override_get_db: Session) -> None:
    article_in = get_random_article()
    article = crud.article.create(db=override_get_db, obj_in=article_in)
    article_by_id = crud.article.get(db=override_get_db, id=article.id)
    assert article_by_id
    assert article.name == article_by_id.name
    assert jsonable_encoder(article) == jsonable_encoder(article_by_id)


def test_get_multi_article(override_get_db: Session) -> None:
    article_in_1 = get_random_article()
    article_in_2 = get_random_article()
    crud.article.create(db=override_get_db, obj_in=article_in_1)
    crud.article.create(db=override_get_db, obj_in=article_in_2)
    articles = crud.article.get_multi(override_get_db)
    assert len(articles) > 1


def test_create_article(override_get_db: Session) -> None:
    article_in = get_random_article()
    article = crud.article.create(db=override_get_db, obj_in=article_in)
    assert article.name == article_in.name


def test_update_article(override_get_db: Session) -> None:
    article_in = get_random_article()
    article = crud.article.create(db=override_get_db, obj_in=article_in)
    article_update = get_random_update_article()
    article_updated = crud.article.update(db=override_get_db, db_obj=article, obj_in=article_update)
    assert article.id == article_updated.id
    assert article.name == article_updated.name


def test_remove_article(override_get_db: Session) -> None:
    article_in = get_random_article()
    article = crud.article.create(db=override_get_db, obj_in=article_in)
    crud.article.remove(db=override_get_db, id=article.id)
    article_removed = crud.article.get(db=override_get_db, id=article.id)
    assert article_removed is None
