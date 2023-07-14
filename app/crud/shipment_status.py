from app.crud.base import CRUDBase
from app.models.shipment_status import ShipmentStatus
from app.schemas.shipment_status import ShipmentStatusCreate, ShipmentStatusUpdate


class CRUDStatus(CRUDBase[ShipmentStatus, ShipmentStatusCreate, ShipmentStatusUpdate]):
    pass


shipment_status = CRUDStatus(ShipmentStatus)
