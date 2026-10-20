from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.category.model import Category


class CategoryRepository:
    def __init__(self, db:Session):
        self.db = db
    def get_all(self)->list[Category]:
        statement=select(Category).order_by(Category.id)
        return self.db.scalars(statement).all()
    def get_by_id(self, category_id:int)->Category | None:
        return self.db.get(Category, category_id)
    def create_category(self, category:Category)->Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    def update(self, category:Category)->Category:
        self.db.commit()
        self.db.refresh(category)
        return category
    def delete(self, category:Category)->None:
        self.db.delete(category)
        self.db.commit()

