import re

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr


#TODO run this while creating tables
def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


class Base(DeclarativeBase):
    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
