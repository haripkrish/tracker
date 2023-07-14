from app.crud.base import CRUDBase
from app.models.carrier import Carrier
from app.schemas.carrier import CarrierCreate, CarrierUpdate


class CRUDCarrier(CRUDBase[Carrier, CarrierCreate, CarrierUpdate]):
    pass


carrier = CRUDCarrier(Carrier)
