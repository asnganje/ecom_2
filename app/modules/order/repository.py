from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.cart.model import CartItem
from app.modules.order.model import Order, OrderItem


class OrderRepository:
    def __init__(self, db:Session):
        self.db = db
    def get_order_by_id(self, order_id:int)->Order | None:
        return self.db.get(Order, order_id)
    def get_order_by_user_id(self, user_id:int)->list[Order]:
        query_statement= select(Order).where(Order.user_id == user_id).order_by(Order.id.desc())
        return self.db.scalars(query_statement).all()
    def get_all(self):
        query_statement=(select(Order).
                         order_by(Order.id.desc())
                         )
        return self.db.scalars(query_statement).all()
    def get_items_by_order_id(self, order_id:int)->list[OrderItem]:
        query_statement=select(OrderItem).where(OrderItem.order_id==order_id).order_by(OrderItem.id.asc())
        return self.db.scalars(query_statement).all()

    def place_order(self, order:Order, order_items:list[OrderItem], cart_items:list[CartItem]):
        self.db.add(order)
        self.db.flush()
        for item in order_items:
            item.order_id = order.id
            self.db.add(item)
        for item in cart_items:
            self.db.delete(item)
        self.db.commit()
        self.db.refresh(order)
        return order
    def update_order(self, order:Order)->Order:
        self.db.commit()
        self.db.refresh(order)
        return order





