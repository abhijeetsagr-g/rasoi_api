from fastapi import APIRouter, Query

from app.models.recipe_model import convertToRecipeModel, RecipeModel
from app.database import get_collection

collection = get_collection()
router = APIRouter()

# / GET {LIMIT} recipes
@router.get("/")
async def get_recipes(
    name: str | None = None,
    cuisine: str | None = None,
    diet: str | None = None,
    course: str | None = None,
    max_prep: int | None = Query(None, ge=0),
    max_cook: int | None = Query(None, ge=0),
    max_total: int | None = Query(None, ge=0),
    sort: str | None = None,
    limit: int = Query(10, le=50)
):
    query = {}

    if name:
        query["RecipeName"] = {"$regex": name, "$options": "i"}
    if cuisine:
        query["Cuisine"] = cuisine
    if diet:
        query["Diet"] = diet
    if course:
        query["Course"] = course
    if max_prep is not None:
        query["PrepTimeInMins"] = {"$lte": max_prep}
    if max_cook is not None:
        query["CookTimeInMins"] = {"$lte": max_cook}

    sort_field = None
    sort_order = 1

    if sort:
        if sort.startswith("-"):
            sort_order = -1
            sort = sort[1:]

        sort_map = {
            "prep": "PrepTimeInMins",
            "cook": "CookTimeInMins",
            "name": "RecipeName"
        }

        sort_field = sort_map.get(sort)

    # If total sorting OR total filter is needed → aggregation
    if max_total is not None or sort == "total":
        pipeline = [
            {
                "$addFields": {
                    "TotalTime": {
                        "$add": ["$PrepTimeInMins", "$CookTimeInMins"]
                    }
                }
            }
        ]

        match_stage = query.copy()
        if max_total is not None:
            match_stage["TotalTime"] = {"$lte": max_total}

        pipeline.append({"$match": match_stage})

        if sort == "total":
            pipeline.append({"$sort": {"TotalTime": sort_order}})
        elif sort_field:
            pipeline.append({"$sort": {sort_field: sort_order}})

        pipeline.append({"$limit": limit})

        docs = await collection.aggregate(pipeline).to_list(length=limit)

    else:
        cursor = collection.find(query)

        if sort_field:
            cursor = cursor.sort(sort_field, sort_order)

        docs = await cursor.limit(limit).to_list(limit)

    return [convertToRecipeModel(doc) for doc in docs]

@router.get("/cuisines")
async def list_cuisines():
    cuisines = await collection.distinct("Cuisine")
    return sorted(cuisines)

@router.get("/course")
async def list_course():
    course = await collection.distinct("Course")
    return sorted(course)

@router.get("/diet")
async def list_diet():
    diet = await collection.distinct("Diet")
    return sorted(diet)
