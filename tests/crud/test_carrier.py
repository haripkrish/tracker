from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app import crud
from tests.utils.carrier import get_random_carrier, get_random_update_carrier


def test_get_carrier(override_get_db: Session) -> None:
    carrier_in = get_random_carrier()
    carrier = crud.carrier.create(db=override_get_db, obj_in=carrier_in)
    carrier_by_id = crud.carrier.get(db=override_get_db, id=carrier.id)
    assert carrier_by_id
    assert carrier.name == carrier_by_id.name
    assert jsonable_encoder(carrier) == jsonable_encoder(carrier_by_id)


def test_get_multi_carrier(override_get_db: Session) -> None:
    carrier_in_1 = get_random_carrier()
    carrier_in_2 = get_random_carrier()
    crud.carrier.create(db=override_get_db, obj_in=carrier_in_1)
    crud.carrier.create(db=override_get_db, obj_in=carrier_in_2)
    carrier = crud.carrier.get_multi(override_get_db)
    assert len(carrier) > 1


def test_create_carrier(override_get_db: Session) -> None:
    carrier_in = get_random_carrier()
    carrier = crud.carrier.create(db=override_get_db, obj_in=carrier_in)
    assert carrier.name == carrier_in.name


def test_update_carrier(override_get_db: Session) -> None:
    carrier_in = get_random_carrier()
    carrier = crud.carrier.create(db=override_get_db, obj_in=carrier_in)
    carrier_update = get_random_update_carrier()
    carrier_updated = crud.carrier.update(db=override_get_db, db_obj=carrier, obj_in=carrier_update)
    assert carrier.id == carrier_updated.id
    assert carrier.name == carrier_updated.name


def test_remove_carrier(override_get_db: Session) -> None:
    carrier_in = get_random_carrier()
    carrier = crud.carrier.create(db=override_get_db, obj_in=carrier_in)
    crud.carrier.remove(db=override_get_db, id=carrier.id)
    carrier_removed = crud.carrier.get(db=override_get_db, id=carrier.id)
    assert carrier_removed is None
