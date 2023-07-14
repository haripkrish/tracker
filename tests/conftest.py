import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy_utils import database_exists, create_database, drop_database
from starlette.testclient import TestClient

from app.api.deps import get_db
from app.db import Base
from app.main import app


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1234@127.0.0.1:5432/tracker_test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_test_db():
    SessionLocal = sessionmaker(bind=engine)
    test_db = SessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    if database_exists(SQLALCHEMY_DATABASE_URL):
        drop_database(SQLALCHEMY_DATABASE_URL)
    create_database(SQLALCHEMY_DATABASE_URL)
    with engine.connect() as con:
        con.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
        con.commit()

    print("The uuid-ossp extension has been installed.")
    Base.metadata.create_all(engine, checkfirst=False)
    with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            if table.name != 'carrier':
                sequence_name = f"{table.name}_id_seq"
                connection.execute(text(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1"))
    app.dependency_overrides[get_db] = get_test_db
    yield
    drop_database(SQLALCHEMY_DATABASE_URL)


@pytest.fixture
def override_get_db():

    SessionLocal = sessionmaker(bind=engine)

    session: Session = SessionLocal()
    yield session
    for tbl in reversed(Base.metadata.sorted_tables):
        with engine.connect() as con:
            con.execute(tbl.delete())
            con.commit()
            con.close()
    session.close()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c