from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.dependency import get_db, get_current_user
from app.modules.category.schema import CategoryRead, CategoryCreate, CategoryUpdate
from app.modules.category.service import CategoryService
from app.modules.users.model import User
from app.modules.users.schema import UserRole

router = APIRouter(
    prefix="/categories"
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CategoryRead])
def list_all(db: Session=Depends(get_db)):
    service = CategoryService(db)
    categories = service.list_categories()
    return categories
@router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryRead)
def get_category(category_id:int, db:Session=Depends(get_db)):
    service = CategoryService(db)
    category = service.get_category(category_id)
    return category

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryRead)
def create_category(payload:CategoryCreate, current_user:User = Depends(get_current_user), db:Session=Depends(get_db)):
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin can access the resource"
        )
    service = CategoryService(db)
    return service.create_category(payload)

@router.patch("/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryRead)
def update_category(category_id:int, payload:CategoryUpdate, db:Session=Depends(get_db)):
    service = CategoryService(db)
    return service.update_category(category_id, payload)

@router.delete("/{category_id}", status_code=status.HTTP_200_OK, response_model=dict)
def delete_category(category_id:int, db:Session=Depends(get_db)):
    service = CategoryService(db)
    service.delete_category(category_id)
    return {"msg":"delete success"}


