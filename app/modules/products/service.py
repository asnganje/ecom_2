from math import ceil

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.common.price import calculate_selling_price
from app.modules.products.model import Product
from app.modules.products.repository import ProductRepository
from app.modules.products.schema import ProductRead, ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db:Session):
        self.product_repository = ProductRepository(db)

    def _serialized_product(self, product:Product)->ProductRead:
        payload = ProductRead.model_validate(product)
        payload.selling_price = calculate_selling_price(payload.price, payload.discount_percent)
        return payload
    def list_products(self,
                      page:int,
                      limit:int,
                      category_id: int | None = None,
                      brand_name: str | None = None,
                      is_active: bool | None = None,
                      min_price: float | None = None,
                      max_price: float | None = None,
                      sort_price: str | None = None
                      )->dict:
        products, total = self.product_repository.get_all(page,
                                                          limit,
                                                          category_id,
                                                          brand_name,
                                                          is_active,
                                                          min_price,
                                                          max_price,
                                                          sort_price
                                                          )
        if len(products) <= 0:
            return {
                "products": [],
                "pagination": {
                    "limit": limit,
                    "page": page,
                    "total": total
            }}

        payload = [self._serialized_product(product) for product in products]
        return {
                "products":payload,
                "pagination":{
                "limit":limit,
                "page":page,
                "total":total,
                "total_pages":ceil(total/limit)
            }
        }
    def get_product(self, product_id:int)->ProductRead:
        product = self.product_repository.get_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return self._serialized_product(product)

    def create_product(self, payload:ProductCreate)->ProductRead:
        db_product = Product(**payload.model_dump())
        saved_product=self.product_repository.create_product(db_product)
        product = self._serialized_product(saved_product)
        return product
    def update_product(self, product_id:int, payload:ProductUpdate)->ProductRead:
        product = self.product_repository.get_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        changes = payload.model_dump(exclude_none=True, exclude_unset=True)
        for field, value in changes.items():
            setattr(product, field, value)
        updated_product = self.product_repository.update_product(product)
        return self._serialized_product(updated_product)
    def delete_product(self, product_id:int)->dict:
        product = self.product_repository.get_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        self.product_repository.delete_product(product)
        return {
            "msg":"Product deleted successfully!"
        }





