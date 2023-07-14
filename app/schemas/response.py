from app import schemas
from typing import List, Optional
from pydantic import BaseModel


class ArticleSku(schemas.ArticleSku):
    article: schemas.Article


class ShipmentItemsResponse(schemas.ShipmentItems):
    article_sku: ArticleSku


class WeatherInfo(BaseModel):
    location: Optional[str] = ''
    temperature: Optional[float] = 0.0
    conditions: Optional[str] = ''
    last_updated_at: Optional[str | None] = None


class ShipmentResponse(schemas.Shipment):
    carrier: schemas.Carrier
    source_address: schemas.Address
    destination_address: schemas.Address
    shipment_status: schemas.ShipmentStatus
    shipment_item: List[ShipmentItemsResponse]


class ShipmentWeatherResponse(ShipmentResponse):
    weather_info: Optional[WeatherInfo]


class ShipmentWeatherListResponse(BaseModel):
    shipments: List[ShipmentWeatherResponse]
