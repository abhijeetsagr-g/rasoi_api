from pydantic import BaseModel


class RecipeModel(BaseModel):
    recipe_name : str
    prep_time : int
    cook_time : int
    total_time : int
    cuisine : str
    course : str
    diet : str
    instructions : str
    url : str
    ingredients : list[str]


def convertToRecipeModel(doc: dict) -> RecipeModel:
    return RecipeModel(
        recipe_name=doc.get("TranslatedRecipeName", ""),
        prep_time=int(doc.get("PrepTimeInMins", 0)),
        cook_time=int(doc.get("CookTimeInMins", 0)),
        total_time=int(doc.get("TotalTimeInMins", 0)),
        cuisine=doc.get("Cuisine", ""),
        course=doc.get("Course", ""),
        diet=doc.get("Diet", ""),
        instructions=doc.get("TranslatedInstructions", ""),
        url=doc.get("URL", ""),
        ingredients=[
            ingredient.strip()
            for ingredient in doc.get("TranslatedIngredients", "").split(",")
        ]
    )
