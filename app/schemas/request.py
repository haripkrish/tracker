from _decimal import Decimal

from app import schemas
from typing import List, Optional
from pydantic import BaseModel


class ArticleCreateRequest(BaseModel):
    name: str


class ArticleSkuCreateRequest(BaseModel):
    sku: str
    price: Decimal
    article: ArticleCreateRequest


class ShipmentItemCreateRequest(BaseModel):
    quantity: int
    article_sku: ArticleSkuCreateRequest


class CarrierCreateRequest(BaseModel):
    name: str


class ShipmentStatusCreateRequest(BaseModel):
    name: str
    description: Optional[str]


class AddressCreateRequest(BaseModel):
    street_name: str
    city: str
    country: str
    pincode: int


class ShipmentCreateRequest(BaseModel):
    tracking_id: str
    carrier: CarrierCreateRequest
    shipment_status: ShipmentStatusCreateRequest
    source_address: AddressCreateRequest
    destination_address: AddressCreateRequest
    shipment_item: List[ShipmentItemCreateRequest]
