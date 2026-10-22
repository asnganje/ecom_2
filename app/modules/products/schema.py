from pydantic import BaseModel, Field, ConfigDict


class SpecificationItem(BaseModel):
    name:str
    value:str

class Specification:
    section:str
    features:list[SpecificationItem]

class ProductBase(BaseModel):
    name:str
    brand_name:str
    model_number:str
    description:str
    warranty: str
    discount_percent: float = Field(ge=0, le=100)
    stock_quantity: int = Field(ge=0)
    is_active: bool = Field(default=True)
    highlights: list[str]
    specifications: list[Specification]
    additional_images: list[str]
    price: float = Field(gt=0)
    image_url: str
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    brand_name: str| None = None
    model_number: str| None = None
    description: str| None = None
    warranty: str| None = None
    discount_percent: float| None = Field(default=None, ge=0, le=100)
    stock_quantity: int | None = Field(default=None, ge=0)
    is_active: bool | None = Field(default=None)
    highlights: list[str] | None = None
    specifications: list[Specification]| None = None
    additional_images: list[str]| None = None
    price: float |None = Field(default=None, gt=0)
    image_url: str| None = None
    category_id: int| None = None

class ProductRead(ProductBase):
    id:int
    selling_price:float|None

    model_config = ConfigDict(from_attributes=True)
