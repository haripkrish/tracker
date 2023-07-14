from pydantic import BaseModel, ConfigDict
from pydantic import UUID4


class ShipmentBase(BaseModel):
    tracking_id: str
    carrier_id: UUID4
    source_address_id: int
    destination_address_id: int
    shipment_status_id: int


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(ShipmentBase):
    pass


class ShipmentRequest(BaseModel):
    pass


class ShipmentRequestFilter(BaseModel):
    tracking_id: str
    carrier_id: UUID4


class ShipmentInDBBase(ShipmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Shipment(ShipmentInDBBase):
    pass


class ShipmentInDB(ShipmentInDBBase):
    pass


