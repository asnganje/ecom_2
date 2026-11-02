from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependency import get_current_user, get_db
from app.modules.order.schema import PlaceOrderRequest, OrderRead, OrderStatusUpdate
from app.modules.order.service import OrderService
from app.modules.users.model import User

router = APIRouter(prefix="/orders")
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderRead)
def place_order(payload:PlaceOrderRequest,
                current_user:User=Depends(get_current_user),
                db:Session=Depends(get_db)
                ):
    order_service = OrderService(db)
    order = order_service.place_order(current_user, payload)
    return order

@router.get("/me", status_code=status.HTTP_200_OK, response_model=list[OrderRead])
def list_my_orders(current_user:User=Depends(get_current_user),
                db:Session=Depends(get_db)):
    order_service = OrderService(db)
    orders = order_service.list_my_orders(current_user)
    return orders

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrderRead])
def list_all_orders(current_user:User=Depends(get_current_user),
                db:Session=Depends(get_db)):
    order_service = OrderService(db)
    orders = order_service.list_all_orders(current_user)
    return orders

@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderRead)
def get_order_by_id(order_id:int, current_user:User=Depends(get_current_user),
                db:Session=Depends(get_db)):
    order_service = OrderService(db)
    order = order_service.get_order(order_id, current_user)
    return order

@router.patch("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderRead)
def update_order_status(order_id:int, payload:OrderStatusUpdate, db:Session=Depends(get_db), current_user:User=Depends(get_current_user)):
    order_service = OrderService(db)
    order = order_service.update_order_status(order_id, current_user, payload)
    return order

