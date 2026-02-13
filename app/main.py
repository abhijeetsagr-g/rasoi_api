from fastapi import FastAPI
from app.routers.recipe_router import router

app = FastAPI()
app.include_router(router, prefix="/recipes")


@app.get("/")
def greet():
    return {"message" : "Welcome to Rasoi API, use /recipes"}
