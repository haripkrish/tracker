from app.schemas.address import AddressCreate
from tests.utils.common import get_random_string, get_random_city, get_random_int


def get_random_address() -> AddressCreate:
    return AddressCreate(
        street_name=get_random_string(10),
        city=get_random_city(),
        country=get_random_string(10),
        pincode=get_random_int()
    )
