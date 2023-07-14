# Import all the models, so that Base has them before being
# imported by Alembic
# noqa
from app.db.base_class import Base
from app.models.carrier import Carrier
from app.models.article import Article
from app.models.article_sku import ArticleSku
from app.models.address import Address
from app.models.shipment import Shipment
from app.models.shipment_item import ShipmentItem
from app.models.shipment_status import ShipmentStatus