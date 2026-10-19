from fastapi import FastAPI

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