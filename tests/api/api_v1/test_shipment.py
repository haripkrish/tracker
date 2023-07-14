import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.db.data_populator import DataPopulator

from app import crud, schemas


def test_shipment_with_valid_tracking_and_carrier_id(client: TestClient, override_get_db: Session):
    data_populator = DataPopulator(override_get_db)
    data_populator.populate_all_tables()
    shipment = crud.shipment.get(db=override_get_db, id=1)

    response = client.get(
        f"/api/v1/shipments/?tracking_id={shipment.tracking_id}&carrier_id={shipment.carrier_id}",
    )

    response_data = response.json()
    assert schemas.response.ShipmentWeatherListResponse.model_validate(response_data)
    assert len(response_data['shipments']) == 1
    assert response.status_code == 200



def test_shipment_with_invalid_tracking_id(client: TestClient, override_get_db: Session):

    response = client.get(
        f"/api/v1/shipments/?tracking_id=TN6727567811000",
    )

    response_data = response.json()
    assert 'detail' in response_data
    assert response.status_code == 404


def test_shipment_with_valid_tracking_id(client: TestClient, override_get_db: Session):
    data_populator = DataPopulator(override_get_db)
    data_populator.populate_all_tables()
    tracking_id = crud.shipment.get(db=override_get_db, id=11).tracking_id

    response = client.get(
        f"/api/v1/shipments/?tracking_id={tracking_id}",
    )

    response_data = response.json()
    assert schemas.response.ShipmentWeatherListResponse.model_validate(response_data)
    assert len(response_data['shipments']) == 1
    assert response.status_code == 200


def test_shipment_with_valid_carrier_id(client: TestClient, override_get_db: Session):
    data_populator = DataPopulator(override_get_db)
    data_populator.populate_all_tables()
    carrier_id = crud.shipment.get(db=override_get_db, id=22).carrier_id

    response = client.get(
        f"/api/v1/shipments/?carrier_id={carrier_id}",
    )

    response_data = response.json()
    assert schemas.response.ShipmentWeatherListResponse.model_validate(response_data)
    assert len(response_data['shipments']) == 1
    assert response.status_code == 200


def test_all_shipment(client: TestClient, override_get_db: Session):
    data_populator = DataPopulator(override_get_db)
    data_populator.populate_all_tables()

    response = client.get(
        f"/api/v1/shipments/",
    )

    response_data = response.json()
    assert schemas.response.ShipmentWeatherListResponse.model_validate(response_data)
    assert len(response_data['shipments']) > 1
    assert response.status_code == 200


def test_shipment_with_invalid_carrier_id(client: TestClient, override_get_db: Session):

    response = client.get(
        f"/api/v1/shipments/?carrier_id={str(uuid.uuid4())}",
    )

    response_data = response.json()
    assert 'detail' in response_data
    assert response.status_code == 404
