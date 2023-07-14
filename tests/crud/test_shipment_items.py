from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.article_sku import ArticleSkuCreate
from app.schemas.shipment import ShipmentCreate
from app.schemas.shipment_item import ShipmentItemsCreate, ShipmentItemsUpdate
from tests.crud.test_article_sku import create_random_article, get_random_article_sku
from tests.utils.address import get_random_address
from tests.utils.carrier import get_random_carrier
from tests.utils.common import get_random_string, get_random_int
from tests.utils.shipment_status import get_random_status


def create_random_shipment(override_get_db: Session) -> ShipmentCreate:
    carrier = crud.carrier.create(db=override_get_db, obj_in=get_random_carrier())
    source_address = crud.address.create(db=override_get_db, obj_in=get_random_address())
    destination_address = crud.address.create(db=override_get_db, obj_in=get_random_address())
    shipment_status = crud.shipment_status.create(db=override_get_db, obj_in=get_random_status())
    tracking_id = get_random_string(10)
    shipment_in = ShipmentCreate(
        tracking_id=tracking_id,
        carrier_id=carrier.id,
        source_address_id=source_address.id,
        destination_address_id=destination_address.id,
        shipment_status_id=shipment_status.id
    )
    return crud.shipment.create(db=override_get_db, obj_in=shipment_in)


def create_random_article_sku(override_get_db: Session) -> ArticleSkuCreate:
    article = create_random_article(override_get_db)
    article_sku_in = get_random_article_sku(article_id=article.id)
    return crud.article_sku.create(db=override_get_db, obj_in=article_sku_in)


def get_random_shipment_item(shipment_id: int, article_sku_id: int) -> ShipmentItemsCreate:
    return ShipmentItemsCreate(
        shipment_id=shipment_id,
        article_sku_id=article_sku_id,
        quantity=get_random_int()
    )


def get_random_update_shipment_item() -> ShipmentItemsUpdate:
    return ShipmentItemsUpdate(
        quantity=get_random_int()
    )


def test_get_shipment_item(override_get_db: Session) -> None:
    shipment = create_random_shipment(override_get_db)
    article_sku = create_random_article_sku(override_get_db)
    shipment_item_in = get_random_shipment_item(shipment_id=shipment.id, article_sku_id=article_sku.id)
    shipment_item = crud.shipment_items.create(db=override_get_db, obj_in=shipment_item_in)
    shipment_item_by_id = crud.shipment_items.get(db=override_get_db, id=shipment_item.id)
    assert shipment_item_by_id
    assert shipment_item.shipment_id == shipment_item_by_id.shipment_id
    assert shipment_item.article_sku_id == shipment_item_by_id.article_sku_id
    assert shipment_item.quantity == shipment_item_by_id.quantity
    assert jsonable_encoder(shipment_item) == jsonable_encoder(shipment_item_by_id)


def test_get_multi_shipment_item(override_get_db: Session) -> None:
    shipment = create_random_shipment(override_get_db)
    article_sku = create_random_article_sku(override_get_db)
    shipment_item_in = get_random_shipment_item(shipment_id=shipment.id, article_sku_id=article_sku.id)
    crud.shipment_items.create(db=override_get_db, obj_in=shipment_item_in)
    shipment_items = crud.shipment_items.get_multi(override_get_db)
    assert len(shipment_items) >= 1


def test_create_shipment_item(override_get_db: Session) -> None:
    shipment = create_random_shipment(override_get_db)
    article_sku = create_random_article_sku(override_get_db)
    shipment_item_in = get_random_shipment_item(shipment_id=shipment.id, article_sku_id=article_sku.id)
    shipment_item = crud.shipment_items.create(db=override_get_db, obj_in=shipment_item_in)
    assert shipment_item.shipment_id == shipment_item_in.shipment_id
    assert shipment_item.article_sku_id == shipment_item_in.article_sku_id
    assert shipment_item.quantity == shipment_item_in.quantity
    assert shipment_item.id is not None


def test_remove_shipment_item(override_get_db: Session) -> None:
    shipment = create_random_shipment(override_get_db)
    article_sku = create_random_article_sku(override_get_db)
    shipment_item_in = get_random_shipment_item(shipment_id=shipment.id, article_sku_id=article_sku.id)
    shipment_item = crud.shipment_items.create(db=override_get_db, obj_in=shipment_item_in)
    crud.shipment_items.remove(db=override_get_db, id=shipment_item.id)
    shipment_item_removed = crud.shipment_items.get(db=override_get_db, id=shipment_item.id)
    assert shipment_item_removed is None
