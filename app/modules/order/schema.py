from enum import Enum

from pydantic import BaseModel, ConfigDict


class OrderItemRead(BaseModel):
    id:int
    product_id:int
    product_name:str
    product_img_url: str
    quantity: int
    unit_price: float
    unit_selling_price: float
    sub_total: float

    model_config = ConfigDict(from_attributes=True)

class OrderStatus(str, Enum):
    PENDING="PENDING"
    CONFIRMED="CONFIRMED"
    SHIPPED="SHIPPED"
    DELIVERED="DELIVERED"
    CANCELLED="CANCELLED"

class PaymentStatus(str, Enum):
    PENDING="PENDING"
    PAID="PAID"
    FAILED="FAILED"
    REFUNDED="REFUNDED"

class PlaceOrderRequest(BaseModel):
    shipping_address_id:int

class OrderRead(BaseModel):
    id:int
    user_id: int
    shipping_address_id:int
    total_items:int
    total_amount: float
    status: OrderStatus
    payment_status: PaymentStatus
    items:list[OrderItemRead]

    model_config = ConfigDict(from_attributes=True)

class OrderStatusUpdate(BaseModel):
    status:OrderStatus
