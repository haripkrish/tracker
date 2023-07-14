from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app import crud
from tests.utils.address import get_random_address


def test_create_address(override_get_db: Session) -> None:
    address_in = get_random_address()
    address = crud.address.create(db=override_get_db, obj_in=address_in)
    assert address_in.street_name == address.street_name
    assert address_in.city == address.city
    assert address_in.country == address.country
    assert address_in.pincode == address.pincode
