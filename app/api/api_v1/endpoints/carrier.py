from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Carrier])
def read_carriers(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve carrier details
    """
    carriers = crud.carrier.get_multi(
        db,
        skip=skip,
        limit=limit
    )
    return carriers


@router.get("/{id}", response_model=schemas.Carrier)
def read_carrier(
        *,
        db: Session = Depends(deps.get_db),
        id: UUID4
) -> Any:
    """
    Retrieve carrier details
    """
    carrier = crud.carrier.get(
        db,
        id=id
    )
    return carrier


@router.post("/", response_model=schemas.Carrier, status_code=201)
def create_item(
        *,
        db: Session = Depends(deps.get_db),
        carrier_in: schemas.CarrierRequest,
) -> Any:
    """
    Create new carrier.
    """
    item = crud.carrier.create(db=db, obj_in=carrier_in)
    return item


@router.put("/{id}", response_model=schemas.Carrier)
def update_carrier(
        *,
        db: Session = Depends(deps.get_db),
        id: UUID4,
        carrier_in: schemas.CarrierRequest,
) -> Any:
    """
    Update an carrier.
    """
    carrier = crud.carrier.get(db=db, id=id)
    if not carrier:
        raise HTTPException(status_code=404, detail="carrier not found")
    carrier = crud.carrier.update(db=db, db_obj=carrier, obj_in=carrier_in)
    return carrier
