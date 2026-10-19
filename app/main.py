from fastapi import FastAPI

from app.database.session import settings
from app.modules.auth.router import router as auth_router

app = FastAPI(
    title="Ecommerce Application",
    description="An electronics ecommerce application",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "msg":"Welcome to the ecommerce intelligence API"
    }
app.include_router(auth_router, prefix=settings.api_path, tags=["Auth"])