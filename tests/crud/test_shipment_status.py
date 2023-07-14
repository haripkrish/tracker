from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app import crud
from tests.utils.shipment_status import get_random_status, get_random_update_status


def decorator_status_create(func):
    def inner(override_get_db, **kwargs):
        status_in = get_random_status()
        kwargs['status'] = crud.shipment_status.create(override_get_db, obj_in=status_in)
        func(override_get_db, **kwargs)
    return inner


@decorator_status_create
def test_get_status(override_get_db: Session, **kwargs) -> None:
    status = kwargs['status']
    status_by_id = crud.shipment_status.get(db=override_get_db, id=status.id)
    assert status_by_id
    assert status.name == status_by_id.name
    assert jsonable_encoder(status) == jsonable_encoder(status_by_id)


def test_get_multi_status(override_get_db: Session) -> None:
    status_in = get_random_status()
    crud.shipment_status.create(db=override_get_db, obj_in=status_in)
    status = crud.shipment_status.get_multi(override_get_db)
    assert len(status) >= 1


def test_create_status(override_get_db: Session) -> None:
    status_in = get_random_status()
    status = crud.shipment_status.create(db=override_get_db, obj_in=status_in)
    assert status.name == status_in.name


def test_update_status(override_get_db: Session) -> None:
    status_in = get_random_status()
    status = crud.shipment_status.create(db=override_get_db, obj_in=status_in)
    status_update = get_random_update_status()
    status_updated = crud.shipment_status.update(db=override_get_db, db_obj=status, obj_in=status_update)
    assert status.id == status_updated.id
    assert status.name == status_updated.name


def test_remove_status(override_get_db: Session) -> None:
    status_in = get_random_status()
    status = crud.shipment_status.create(db=override_get_db, obj_in=status_in)
    crud.shipment_status.remove(db=override_get_db, id=status.id)
    status_removed = crud.shipment_status.get(db=override_get_db, id=status.id)
    assert status_removed is None
