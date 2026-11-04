from sqlalchemy.orm import Session

from app.modules.order.repository import OrderRepository
from app.modules.order.schema import OrderStatus, PaymentStatus
from app.modules.payment.model import Payment
from app.modules.payment.provider import StripeProvider
from app.modules.payment.repository import PaymentRepository
from app.modules.payment.schema import CreatePaymentLinkRequest, PaymentLinkResponse, VerifyPaymentRequest, \
    VerifyPaymentResponse, PaymentProvider
from app.modules.users.model import User
from fastapi import HTTPException, status

from app.modules.users.schema import UserRole


class PaymentService:
    def __init__(self, db:Session):
        self.order_repository=OrderRepository(db)
        self.payment_repository = PaymentRepository(db)
    def _get_provider(self, provider:PaymentProvider):
        if provider == provider.STRIPE:
            return StripeProvider()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported payment provider"
            )

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

        provider = self._get_provider(payload.provider)
        provider_response=provider.create_payment_link(
            order_id=order.id,
            amount=order.total_amount,
            user_email=current_user.email,
            user_name=current_user.fullname
        )

        payment = Payment(
            order_id=payload.order_id,
            user_id=current_user.id,
            provider=payload.provider.value,
            amount=order.total_amount,
            currency="USD",
            status=PaymentStatus.PENDING.value,
            payment_link_url=provider_response["payment_link"],
            provider_payment_link_id=provider_response["provider_payment_link_id"]
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

    def verify_payment(self, current_user:User, payload:VerifyPaymentRequest)->dict:
        order = self.get_own_order(payload.order_id, current_user)
        payment=self.payment_repository.get_payment_by_order_and_provider(order.id, payload.provider.value)

        if payment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )

        if payment.status == PaymentStatus.PAID.value:
            return VerifyPaymentResponse(
                order_id=order.id,
                payment_status=PaymentStatus.PAID,
                order_status=order.status,
                provider=payload.provider,
                payment_id=payment.provider_payment_id or payload.payment_id
            ).model_dump()

        provider_v = self._get_provider(payload.provider)
        provider_payment = provider_v.get_payment_details(payload.payment_id)
        expected_amount = int(round(order.total_amount * 100))

        if provider_payment["amount"] != expected_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment amount does not match order amount"
            )

        if not provider_payment["is_paid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="payment not completed",
            )
        payment.status = PaymentStatus.PAID.value
        payment.provider_payment_id = provider_payment["payment_id"]
        self.payment_repository.update_payment(payment)

        order.payment_status = PaymentStatus.PAID.value
        order.status = OrderStatus.CONFIRMED.value
        self.order_repository.update_order(order)

        return VerifyPaymentResponse(
            order_id=order.id,
            payment_status=PaymentStatus.PAID,
            order_status=order.status,
            provider=payload.provider,
            payment_id=payment.provider_payment_id
        ).model_dump()





