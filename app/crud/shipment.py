from sqlalchemy.orm import Session, selectinload
from sqlalchemy.sql.expression import select

from app.crud.base import CRUDBase
from app.models import Shipment, ShipmentItem, ArticleSku, Carrier
from app.models.address import source_address_alias, destination_address_alias
from app.schemas import ShipmentResponse
from app.schemas.shipment import ShipmentCreate, ShipmentUpdate, ShipmentRequestFilter


class CRUDShipment(CRUDBase[Shipment, ShipmentCreate, ShipmentUpdate]):

    def get_by_tracking_and_carrier_id(
            self, db: Session, *, params: ShipmentRequestFilter
    ) -> ShipmentResponse | None:

        shipment_data = select(Shipment, Carrier, source_address_alias, source_address_alias, destination_address_alias) \
            .join(Carrier, Carrier.id == Shipment.carrier_id) \
            .join(source_address_alias, source_address_alias.id == Shipment.source_address_id) \
            .join(destination_address_alias, destination_address_alias.id == Shipment.destination_address_id) \
            .options(selectinload(Shipment.shipment_item).joinedload(ShipmentItem.article_sku, innerjoin=True)
                     .joinedload(ArticleSku.article, innerjoin=True))

        for match_field, match_value in params.items():
            if match_value:
                match match_field:
                    case "tracking_id":
                        shipment_data = shipment_data.where(
                            Shipment.tracking_id == match_value
                        )
                    case "carrier_id":
                        shipment_data = shipment_data.where(
                            Shipment.carrier_id == match_value
                        )
                    case _:
                        pass
        return db.scalars(shipment_data).all()


shipment = CRUDShipment(Shipment)
