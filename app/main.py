from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from app.model import RecipeModel, convertToRecipeModel
import os


# Load environment variables
load_dotenv()

app = FastAPI()

# Get MongoDB URL from .env
MONGO_URL = os.getenv("MONGO_URL")

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URL)
db = client["recipe_db"]
collection = db["recipes"]


@app.get("/recipes", response_model=list[RecipeModel])
async def get_recipes():
    docs = await collection.find().limit(10).to_list(length=10)
    return [convertToRecipeModel(doc) for doc in docs]
