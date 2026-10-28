from fastapi import FastAPI
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.category.router import router as category_router
from app.modules.products.router import router as product_router
from app.modules.cart.router import router as cart_router
from app.modules.users.service import UserService
from app.database.session import SessionLocal

app = FastAPI(
    title="Ecommerce Application",
    description="An electronics ecommerce application",
    version="1.0.0"
)

db=SessionLocal()
UserService(db).ensure_admin_user()
@app.get("/")
def root():
    return {
        "msg":"Welcome to the ecommerce intelligence API"
    }
api_path="/api/v1"
app.include_router(auth_router, prefix=api_path, tags=["Auth"])
app.include_router(users_router, prefix=api_path, tags=["Users"])
app.include_router(category_router, prefix=api_path, tags=["Categories"])
app.include_router(product_router, prefix=api_path, tags=["Products"])
app.include_router(cart_router, prefix=api_path, tags=["Carts"])