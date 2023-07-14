from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core.weather_api import weather_api
from app.schemas.response import WeatherInfo, ShipmentWeatherListResponse, ShipmentWeatherResponse

router = APIRouter()


async def integrity_error_handler(request, exc):
    constraint_name = exc.orig.diag.constraint_name
    violated_field = exc.orig.diag.column_name
    error_message = f"Unique constraint violation: Field '{violated_field}' violates constraint '{constraint_name}'"
    error_details = {"detail": error_message}

    raise HTTPException(status_code=409, detail=error_details)


@router.get("/", response_model=schemas.response.ShipmentWeatherListResponse | None)
def read_shipments(
        db: Session = Depends(deps.get_db),
        tracking_id: Optional[str] = None,
        carrier_id: Optional[str] = None
) -> Any:
    """
    Retrieve shipment and destination weather details using tracking id and carrier_id
    """
    shipments = crud.shipment.get_by_tracking_and_carrier_id(
        db=db, params={'tracking_id': tracking_id, 'carrier_id': carrier_id}
    )
    result = []
    for each_shipment in shipments:
        if each_shipment.destination_address.city:
            weather_info = weather_api.get_weather(each_shipment.destination_address.city)
        else:
            weather_info = WeatherInfo()
        result.append(ShipmentWeatherResponse(
            **schemas.ShipmentResponse.model_validate(each_shipment).model_dump(),
            weather_info=weather_info
        ))
    if not result:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return ShipmentWeatherListResponse(shipments=result)


@router.post("/")
def create_shipments(request: schemas.ShipmentCreateRequest, db: Session = Depends(deps.get_db)):
    try:
        print(request.model_dump())
        # Get or create a carrier
        carrier_obj = crud.carrier.get_by_field(db=db, field_name='name', field_value=request.carrier.name)
        if not carrier_obj:
            carrier_obj = crud.carrier.create(db=db, obj_in=schemas.CarrierCreate(**request.carrier.model_dump()))

        # Get or create shipment status
        shipment_status_obj = crud.shipment_status.get_by_field(
            db=db, field_name='name', field_value=request.shipment_status.name)
        if not shipment_status_obj:
            print(carrier_obj)
            shipment_status_obj = crud.shipment_status.create(
                db=db, obj_in=schemas.ShipmentStatusCreate(**request.shipment_status.model_dump()))

        # create from and to address
        source_address = crud.address.create(db=db, obj_in=schemas.AddressCreate(**request.source_address.model_dump()))
        destination_address = crud.address.create(
            db=db, obj_in=schemas.AddressCreate(**request.destination_address.model_dump()))

        # create a shipment with the above objects
        shipment = crud.shipment.create(db=db, obj_in=schemas.ShipmentCreate(
            tracking_id=request.tracking_id,
            carrier_id=carrier_obj.id,
            source_address_id=source_address.id,
            destination_address_id=source_address.id,
            shipment_status_id=shipment_status_obj.id
        ))
        shipment_items = []
        # create shipment items
        for item in request.shipment_item:
            # get or create a new article
            article_obj = crud.article.get_by_field(db=db, field_name='name', field_value=item.article_sku.article.name)
            if not article_obj:
                article_obj = crud.article.create(db=db, obj_in=item.article_sku.article)
            article_sku_obj = crud.article_sku.create(
                db=db,
                obj_in=schemas.ArticleSkuCreate(**item.article_sku.model_dump(), article_id=article_obj.id)
            )
            shipment_item = crud.shipment_items.create(
                db=db,
                obj_in=schemas.ShipmentItemsCreate(
                    **item.model_dump(),
                    article_sku_id=article_sku_obj.id,
                    shipment_id=shipment.id
                )
            )
            shipment_items.append(shipment_item)
    except IntegrityError as exc:
        return HTTPException(status_code=400, detail=exc.args)

    return schemas.ShipmentResponse(
        **schemas.Shipment.model_validate(shipment).model_dump(),
        carrier=carrier_obj,
        source_address=source_address,
        destination_address=destination_address,
        shipment_status=shipment_status_obj,
        shipment_item=shipment_items
    )
