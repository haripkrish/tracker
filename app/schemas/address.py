from pydantic import BaseModel, ConfigDict


class AddressBase(BaseModel):
    street_name: str
    city: str
    country: str
    pincode: int


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class AddressRequest(BaseModel):
    pass


class AddressInDBBase(AddressBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Address(AddressInDBBase):
    pass


class AddressInDB(AddressInDBBase):
    pass
