from pydantic import BaseModel, Field, ConfigDict


class AddressBase(BaseModel):
    full_name:str
    phone_number:str
    address_line_1:str
    address_line_2: str|None = None
    city: str
    state: str
    postal_code: str
    country: str="Kenya"
    is_default:bool=False
class AddressCreate(AddressBase):
    pass
class AddressRead(AddressBase):
    id:int
    user_id:int

    model_config = ConfigDict(from_attributes=True)

class AddressUpdate(BaseModel):
    full_name: str| None = None
    phone_number: str| None = None
    address_line_1: str| None = None
    address_line_2: str | None = None
    city: str| None = None
    state: str| None = None
    postal_code: str| None = None
    country: str | None = None
    is_default: bool| None = None