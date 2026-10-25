from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.modules.cart.model import Cart, CartItem


class CartRepository:
    def __init__(self, db:Session):
        self.db =db
    def get_active_cart_by_user_id(self, user_id:int)->Cart|None:
        statement=select(Cart).where(Cart.user_id == user_id, Cart.is_active.is_(True))
        cart = self.db.scalars(statement).first()
        return cart
    def create_cart(self, cart:Cart)->Cart:
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart
    def get_items_by_cart_id(self, cart_id:int)->list[CartItem]:
        statement = select(CartItem).where(CartItem.cart_id == cart_id).order_by(CartItem.id.asc())
        cart_items = self.db.scalars(statement).all()
        return cart_items
    def get_item_by_cart_and_product_id(self, cart_id, product_id:int)->CartItem | None:
        statement = select(CartItem).where(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
        cart_item = self.db.scalars(statement).first()
        return cart_item
    def get_item_by_id(self, item_id:int)->CartItem |None:
        return self.db.get(CartItem, item_id)
    def create_item(self, item:CartItem)->CartItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    def update_item(self, payload:CartItem)->CartItem:
        self.db.commit()
        self.db.refresh(payload)
        return payload
    def delete_item(self, item:CartItem)->None:
        self.db.delete(item)
        self.db.commit()

    def clear_items(self, cart_id:int):
        delete(CartItem).where(CartItem.cart_id == cart_id)
        self.db.commit()





