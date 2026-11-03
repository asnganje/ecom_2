from sqlalchemy.orm import Session

from app.modules.order.repository import OrderRepository
from app.modules.order.schema import OrderStatus, PaymentStatus
from app.modules.payment.model import Payment
from app.modules.payment.repository import PaymentRepository
from app.modules.payment.schema import CreatePaymentLinkRequest, PaymentLinkResponse
from app.modules.users.model import User
from fastapi import HTTPException, status

from app.modules.users.schema import UserRole


class PaymentService:
    def __init__(self, db:Session):
        self.order_repository=OrderRepository(db)
        self.payment_repository = PaymentRepository(db)
    def get_own_order(self, order_id:int, current_user:User):
        order = self.order_repository.get_order_by_id(order_id)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        if order.user_id != current_user.id and current_user.role != UserRole.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access denied"
            )
        return order
    def create_payment(self, current_user:User, payload:CreatePaymentLinkRequest)->PaymentLinkResponse:
        order = self.get_own_order(payload.order_id, current_user)
        if order.status != OrderStatus.PENDING.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment link can only be created for pending orders"
            )
        if order.payment_status == PaymentStatus.PAID.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order is already paid"
            )
        existing_payment=self.payment_repository.getting_pending_by_order_and_provider(order.id, payload.provider.value)
        if existing_payment is not None:
            return PaymentLinkResponse(
                order_id=payload.order_id,
                provider=payload.provider,
                amount=existing_payment.amount,
                currency=existing_payment.currency,
                payment_link=existing_payment.payment_link_url,
                provider_payment_link_id=existing_payment.provider_payment_link_id
            )
        payment = Payment(
            order_id=payload.order_id,
            user_id=current_user.id,
            provider=payload.provider.value,
            amount=order.total_amount,
            currency="USER",
            status=PaymentStatus.PENDING.value,
            payment_link_url="dummy link",
            provider_payment_link_id="dummy link id"
        )

        db_payment = self.payment_repository.create_payment(payment)

        return PaymentLinkResponse(
            order_id=payload.order_id,
            provider=payload.provider,
            amount=db_payment.amount,
            currency=db_payment.currency,
            payment_link=db_payment.payment_link_url,
            provider_payment_link_id=db_payment.provider_payment_link_id
        )



