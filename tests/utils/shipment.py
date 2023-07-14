from tests.utils.carrier import get_random_carrier
from tests.utils.address import get_random_address
from tests.utils.shipment_status import get_random_status
from app.schemas.shipment import ShipmentCreate


def get_random_shipment():
    carrier = get_random_carrier()
    source_address = get_random_address()
    destination_address = get_random_address()
    shipment_status = get_random_status()
    tracking_id = 'b100'
    return ShipmentCreate(
        tracking_id=tracking_id,
        carrier=carrier,
        source_address=source_address,
        destination_address=destination_address,
        shipment_status=shipment_status
    )
