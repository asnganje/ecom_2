from enum import Enum

from pydantic import BaseModel

class PaymentProvider(str, Enum):
    STRIPE = "STRIPE"

class CreatePaymentLinkRequest(BaseModel):
    order_id:int
    provider:PaymentProvider

class PaymentLinkResponse(BaseModel):
    order_id:int
    provider:PaymentProvider
    amount:float
    currency:str
    payment_link:str
    provider_payment_link_id:str