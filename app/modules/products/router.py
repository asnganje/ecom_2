from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependency import get_db, get_current_user
from app.modules.products.schema import ProductRead, ProductCreate, ProductUpdate
from app.modules.products.service import ProductService
from app.modules.users.model import User
from app.modules.users.schema import UserRole

router = APIRouter(prefix="/products")

@router.get("/", status_code=status.HTTP_200_OK, response_model=dict)
def list_products(
        page:int = Query(default=1, ge=1),
        limit:int = Query(default=1, ge=1, le=100),
        category_id: int | None = Query(default=None, ge=1),
        brand_name: str | None = Query(default=None, min_length=1),
        is_active: bool | None = Query(default=None),
        min_price: float | None = Query(default=None, ge=0),
        max_price: float | None = Query(default=None, ge=0),
        sort_price: str | None = Query(default=None, pattern="^(asc|desc)"),
        db: Session=Depends(get_db)
        ):
    service = ProductService(db)
    response = service.list_products(page, limit, category_id, brand_name, is_active, min_price, max_price, sort_price)
    return response

@router.get("/search", status_code=status.HTTP_200_OK, response_model=list[ProductRead])
def search_product(query:str=Query(..., min_length=1), db:Session=Depends(get_db)):
    service = ProductService(db)
    products = service.search_product(query)
    return products

@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductRead)
def get_product(product_id:int, db:Session=Depends(get_db)):
    service = ProductService(db)
    product = service.get_product(product_id)
    return product

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductRead)
def create_product(payload:ProductCreate, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    service = ProductService(db)
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin can access this resource"
        )
    product = service.create_product(payload)
    return product

@router.patch("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductRead)
def update_product(product_id:int, payload:ProductUpdate, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin can access this resource"
        )
    service = ProductService(db)
    updated_product = service.update_product(product_id, payload)
    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_200_OK, response_model=dict)
def delete_product(product_id:int, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin can access this resource"
        )
    service = ProductService(db)
    service.delete_product(product_id)
    return {
        "msg":"Product successfully deleted"
    }


