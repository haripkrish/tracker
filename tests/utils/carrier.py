from app.schemas.carrier import CarrierCreate, CarrierUpdate
from tests.utils.common import get_random_uuid, get_random_string


def get_random_carrier() -> CarrierCreate:
    return CarrierCreate(id=get_random_uuid(), name=get_random_string(5))


def get_random_update_carrier() -> CarrierUpdate:
    return CarrierUpdate(id=get_random_uuid(), name=get_random_string(5))
