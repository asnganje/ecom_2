from enum import Enum

from pydantic import ConfigDict, BaseModel


class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class UserBase(BaseModel):
    fullname:str
    email:str
class UserRead(UserBase):
    id:int
    is_active:bool
    role:str

    model_config = ConfigDict(
        from_attributes=True
    )