from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependency import get_current_user, get_db
from app.modules.payment.schema import CreatePaymentLinkRequest, PaymentLinkResponse
from app.modules.payment.service import PaymentService
from app.modules.users.model import User

router = APIRouter(prefix="/payment")

@router.post("/create-link", status_code=status.HTTP_201_CREATED, response_model=PaymentLinkResponse)
def create_payment(payload:CreatePaymentLinkRequest,
                   current_user:User=Depends(get_current_user),
                   db:Session=Depends(get_db)
                   ):
    payment_service = PaymentService(db)
    return payment_service.create_payment(current_user, payload)



