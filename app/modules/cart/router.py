from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependency import get_current_user, get_db
from app.modules.cart.schema import CartRead, UpdateCartItemRequest
from app.modules.cart.service import CartService
from app.modules.users.model import User
from app.modules.cart.schema import AddItemRequest

router = APIRouter(prefix="/cart")

@router.get("/me", status_code=status.HTTP_200_OK, response_model=CartRead)
def get_my_cart(current_user:User = Depends(get_current_user), db: Session=Depends(get_db)):
    cart_service=CartService(db)
    return cart_service.get_my_cart(current_user)

@router.post("/items", status_code=status.HTTP_201_CREATED, response_model=CartRead)
def add_item_to_cart(payload:AddItemRequest, current_user:User = Depends(get_current_user), db: Session=Depends(get_db)):
    cart_service=CartService(db)
    return cart_service.add_item(current_user, payload)

@router.patch("/items/{item_id}", status_code=status.HTTP_200_OK, response_model=CartRead)
def update_cart_item(payload:UpdateCartItemRequest, item_id:int, current_user:User = Depends(get_current_user), db: Session=Depends(get_db)):
    cart_service=CartService(db)
    return cart_service.update_item(current_user, item_id, payload)


@router.delete("/items/{item_id}", status_code=status.HTTP_200_OK, response_model=CartRead)
def remove_cart_item(item_id:int, current_user:User = Depends(get_current_user), db: Session=Depends(get_db)):
    cart_service=CartService(db)
    return cart_service.remove_item(current_user, item_id)

@router.delete("/me", status_code=status.HTTP_200_OK, response_model=CartRead)
def clear_cart( current_user:User = Depends(get_current_user), db: Session=Depends(get_db)):
    cart_service=CartService(db)
    return cart_service.clear_cart(current_user)



