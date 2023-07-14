from fastapi import APIRouter

from app.api.api_v1.endpoints import carrier, shipment_status, shipment

api_router = APIRouter()
api_router.include_router(carrier.router, prefix="/carriers", tags=['carriers'])
api_router.include_router(shipment_status.router, prefix="/shipment_statuses", tags=['shipment_statuses'])
api_router.include_router(shipment.router, prefix="/shipments", tags=['shipments'])
