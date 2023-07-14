import logging

from app.db.session import SessionLocal
from app.db.data_populator import DataPopulator
from app.core.config import settings
from sqlalchemy.sql import text

logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    #db.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
    if settings.POPULATE_DATABASE:
        data_populator = DataPopulator(db)
        data_populator.populate_all_tables()
    #db.commit()
    db.close()


def main() -> None:
    logger.info("Setting up database dependencies")
    init()
    logger.info("Database dependencies created")


if __name__ == "__main__":
    main()
