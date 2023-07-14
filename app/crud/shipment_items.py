from app.crud.base import CRUDBase
from app.models.shipment_item import ShipmentItem
from app.schemas.shipment_item import ShipmentItemsCreate, ShipmentItemsUpdate


class CRUDShipmentItems(CRUDBase[ShipmentItem, ShipmentItemsCreate, ShipmentItemsUpdate]):
    pass


shipment_items = CRUDShipmentItems(ShipmentItem)
