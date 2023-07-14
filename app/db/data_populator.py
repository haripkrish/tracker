import logging
import random

from faker import Faker
from faker.providers import address

from app import crud
from app import schemas
from app.db.session import SessionLocal
from sqlalchemy.orm import Session


logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class DataPopulator:
    def __init__(self, db: Session):
        self.fake = Faker('de_DE')
        self.fake.add_provider(address)
        self.country = 'Germany'
        self.db = db

    def populate_address_data(self):
        for i in range(100):
            address = schemas.AddressCreate(
                street_name=self.fake.address().split('\n')[0],
                city=self.fake.city(),
                country=self.country,
                pincode=self.fake.postcode()
            )
            crud.address.create(db=self.db, obj_in=address)

    def populate_article_with_sku(self):
        article_names = [
            "Laptop",
            "Wireless Earbuds",
            "Mouse",
            "Drone",
            "Keyboard"
        ]
        for i in range(5):
            article = schemas.ArticleCreate(
                name=article_names[i]
            )
            print(i)
            art = crud.article.create(db=self.db, obj_in=article)
            for j in range(3):
                article_sku = schemas.ArticleSkuCreate(
                    sku=self.fake.uuid4(),
                    price=self.fake.random_int(min=10, max=100),
                    article_id=art.id
                )
                crud.article_sku.create(db=self.db, obj_in=article_sku)

    def populate_carrier_data(self):
        shipment_carriers = [
            "DHL",
            "Deutsche Post",
            "Hermes",
            "UPS",
            "FedEx",
            "GLS",
            "DPD",
            "TNT Express",
            "GO! Express & Logistics",
            "Trans-o-Flex"
        ]
        for carrier_name in range(10):
            carrier = schemas.CarrierCreate(
                name=shipment_carriers[carrier_name]
            )
            crud.carrier.create(db=self.db, obj_in=carrier)

    def populate_shipment_status_data(self):
        shipment_statuses = [
            'Pending',
            'In Transit',
            'Out for Delivery',
            'Delivered',
            'Failed Delivery',
            'Returned',
            'Cancelled',
            'Delayed',
            'On Hold',
            'Arrival Scan'
        ]
        for status in shipment_statuses:
            shipment_status = schemas.ShipmentStatusCreate(
                name=status,
                description=status
            )
            crud.shipment_status.create(db=self.db, obj_in=shipment_status)

    def populate_shipment_data(self):
        carrier = crud.carrier.get_multi(db=self.db)
        address = crud.address.get_multi(db=self.db)
        status = crud.shipment_status.get_multi(db=self.db)
        prefix = 'TN'

        for i in range(10):
            random_number = self.fake.random_int(min=10000000, max=99999999)
            shipment = schemas.ShipmentCreate(
                tracking_id=f'{prefix}{random_number}',
                carrier_id=carrier[i].id,
                source_address_id=address[i].id,
                destination_address_id=address[i + 1].id,
                shipment_status_id=status[i].id
            )
            crud.shipment.create(db=self.db, obj_in=shipment)

    def populate_shipment_item(self):
        shipment = crud.shipment.get_multi(db=self.db)
        article_sku = crud.article_sku.get_multi(db=self.db)
        for each_shipment in shipment:
            for _ in range(2):
                shipment_item = schemas.ShipmentItemsCreate(
                    article_sku_id=random.choice(article_sku).id,
                    shipment_id=each_shipment.id,
                    quantity=random.randint(1, 6)
                )
                crud.shipment_items.create(db=self.db, obj_in=shipment_item)

    def populate_all_tables(self) -> None:
        self.populate_address_data()
        self.populate_article_with_sku()
        self.populate_shipment_status_data()
        self.populate_carrier_data()
        self.populate_shipment_data()
        self.populate_shipment_item()
