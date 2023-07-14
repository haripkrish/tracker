from typing import Optional
from pydantic import BaseModel, UUID4, ConfigDict


class CarrierBase(BaseModel):
    name: str | None


class CarrierCreate(CarrierBase):
    name: str


class CarrierUpdate(CarrierBase):
    name: str


class CarrierRequest(BaseModel):
    name: str


class CarrierInDBBase(CarrierBase):
    id: UUID4
    name: str
    model_config = ConfigDict(from_attributes=True)


class Carrier(CarrierInDBBase):
    pass


class CarrierInDB(CarrierInDBBase):
    pass


class CarrierResponse(BaseModel):
    id: UUID4
    name: str
