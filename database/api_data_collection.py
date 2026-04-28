import requests
from data_storage import init_db, upsert_recipe, upsert_ingredient, link_recipe_ingredient

BASE_URL = "https://www.themealdb.com/api/json/v1/1/search.php"

def retrieve_recipe_data(search_keyword: str):
    resp = requests.get(BASE_URL, params={"s": search_keyword}, timeout=10)
    resp.raise_for_status()
    return resp.json()

def estimate_total_time(ingredient_count):
    # Simple, explainable logic for your report
    return 10 + (ingredient_count * 3)

def parse_api_response(api_data):
    meals = api_data.get("meals") or []
    recipes = []

    for meal in meals:
        ingredients = []
        for i in range(1, 21):
            ing = meal.get(f"strIngredient{i}")
            meas = meal.get(f"strMeasure{i}")
            if ing and ing.strip():
                ingredients.append({
                    "name": ing.strip(),
                    "measure": (meas or "").strip()
                })

        recipes.append({
            "api_key": meal.get("idMeal"),
            "name": meal.get("strMeal"),
            "category": meal.get("strCategory"),
            "ingredient_count": len(ingredients),
            "total_time_minutes": estimate_total_time(len(ingredients)),
            "instructions": meal.get("strInstructions"),
            "thumbnail_url": meal.get("strMealThumb"),
            "ingredients": ingredients
        })

    return recipes

if __name__ == "__main__":
    init_db()  # creates database and tables if needed

    raw = retrieve_recipe_data("cake")
    recipes = parse_api_response(raw)

    for r in recipes:
        recipe_id = upsert_recipe(r)

        for ing in r["ingredients"]:
            ingredient_id = upsert_ingredient(ing["name"])
            link_recipe_ingredient(
                recipe_id,
                ingredient_id,
                ing["measure"]
            )

    print(f"Saved {len(recipes)} recipes to database.")


