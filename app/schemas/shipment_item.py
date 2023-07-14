from pydantic import BaseModel, ConfigDict


class ShipmentItemsBase(BaseModel):
    article_sku_id: int
    shipment_id: int
    quantity: int


class ShipmentItemsCreate(ShipmentItemsBase):
    pass


class ShipmentItemsUpdate(ShipmentItemsBase):
    pass


class ShipmentItemsRequest(BaseModel):
    pass


class ShipmentItemResponse(BaseModel):
    pass


class ShipmentItemsInDBBase(ShipmentItemsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ShipmentItems(ShipmentItemsInDBBase):
    pass


class ShipmentItemsInDB(ShipmentItemsInDBBase):
    pass
