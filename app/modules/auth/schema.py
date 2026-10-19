from pydantic import BaseModel, Field, EmailStr


class RegisterRequest(BaseModel):
    fullname:str=Field(min_length=1, max_length=100)
    email:EmailStr
    password:str=Field(min_length=8, max_length=255)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)

