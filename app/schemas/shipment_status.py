from pydantic import BaseModel, ConfigDict
from typing import Optional, Union


class ShipmentStatusBase(BaseModel):
    name: str
    description: Optional[str]


class ShipmentStatusCreate(ShipmentStatusBase):
    pass


class ShipmentStatusUpdate(ShipmentStatusBase):
    name: str


class ShipmentStatusRequest(BaseModel):
    name: str
    description: str


class ShipmentStatusInDBBase(ShipmentStatusBase):
    id: int
    name: str
    description: Union[str | None]
    model_config = ConfigDict(from_attributes=True)


class ShipmentStatus(ShipmentStatusInDBBase):
    pass


class ShipmentStatusInDB(ShipmentStatusInDBBase):
    pass
