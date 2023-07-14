from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.ShipmentStatus])
def read_shipment_statuses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve shipment status details
    """
    shipment_status = crud.shipment_status.get_multi(
        db,
        skip=skip,
        limit=limit
    )
    return shipment_status


@router.get("/{id}", response_model=schemas.ShipmentStatus)
def read_shipment_status(
    *,
    db: Session = Depends(deps.get_db),
    id: int
) -> Any:
    """
    Retrieve shipment status detail
    """
    return crud.shipment_status.get(
        db,
        id=id
    )


@router.post("/", response_model=schemas.ShipmentStatus, status_code=201)
def create_shipment_statuses(
    *,
    db: Session = Depends(deps.get_db),
    shipment_status_in: schemas.ShipmentStatusRequest,
) -> Any:
    """
    Create new shipment status.
    """
    return crud.shipment_status.create(db=db, obj_in=shipment_status_in)


@router.put("/{id}", response_model=schemas.ShipmentStatus)
def update_shipment_statuses(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    shipment_status_in: schemas.ShipmentStatusRequest,
) -> Any:
    """
    Update a shipment status
    """
    shipment_status = crud.shipment_status.get(db=db, id=id)
    if not shipment_status:
        raise HTTPException(status_code=404, detail="Shipment status not found")
    shipment_status = crud.carrier.update(db=db, db_obj=shipment_status, obj_in=shipment_status_in)
    return shipment_status
