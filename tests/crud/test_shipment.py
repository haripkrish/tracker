from sqlalchemy.orm import Session

from app import crud
from app.schemas.shipment import ShipmentCreate
from tests.utils.address import get_random_address
from tests.utils.carrier import get_random_carrier
from tests.utils.common import get_random_string
from tests.utils.shipment_status import get_random_status


def test_create_shipment(override_get_db: Session) -> None:
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
    shipment = crud.shipment.create(db=override_get_db, obj_in=shipment_in)
    assert shipment_in.tracking_id == shipment.tracking_id
    assert shipment_in.carrier_id == shipment.carrier_id
    assert shipment_in.source_address_id == shipment.source_address_id
    assert shipment_in.destination_address_id == shipment.destination_address_id
    assert shipment_in.shipment_status_id == shipment.shipment_status_id

