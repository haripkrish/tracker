from app.schemas.shipment_status import ShipmentStatusCreate, ShipmentStatusUpdate
from tests.utils.common import get_random_int, get_random_string


def get_random_status() -> ShipmentStatusCreate:
    return ShipmentStatusCreate(id=get_random_int(), name=get_random_string(5), description=get_random_string(10))


def get_random_update_status() -> ShipmentStatusUpdate:
    return ShipmentStatusUpdate(id=get_random_int(), name=get_random_string(5), description=get_random_string(10))
