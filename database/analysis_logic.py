import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "baking_recipes.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def get_top_ingredients(limit=10):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT ingredients.name, COUNT(*) AS usage_count
        FROM recipe_ingredients
        JOIN ingredients ON ingredients.id = recipe_ingredients.ingredient_id
        GROUP BY ingredients.name
        ORDER BY usage_count DESC
        LIMIT ?
    """, (limit,))

    results = cur.fetchall()
    conn.close()
    return results


def get_beginner_friendly_recipes(max_ingredients=8, max_time=35):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, category, ingredient_count, total_time_minutes
        FROM recipes
        WHERE ingredient_count <= ? AND total_time_minutes <= ?
        ORDER BY ingredient_count ASC, total_time_minutes ASC
    """, (max_ingredients, max_time))

    results = cur.fetchall()
    conn.close()
    return results


def get_time_category_counts():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            CASE
                WHEN total_time_minutes <= 30 THEN 'Quick'
                WHEN total_time_minutes <= 45 THEN 'Medium'
                ELSE 'Long'
            END AS time_category,
            COUNT(*) AS recipe_count
        FROM recipes
        GROUP BY time_category
        ORDER BY recipe_count DESC
    """)

    results = cur.fetchall()
    conn.close()
    return results


def get_recipe_complexity(limit=None):
    conn = get_conn()
    cur = conn.cursor()

    query = """
        SELECT
            name,
            category,
            ingredient_count,
            CASE
                WHEN ingredient_count <= 8 THEN 'Low'
                WHEN ingredient_count <= 12 THEN 'Medium'
                ELSE 'High'
            END AS complexity_level
        FROM recipes
        ORDER BY ingredient_count ASC
    """

    if limit:
        query += " LIMIT ?"
        cur.execute(query, (limit,))
    else:
        cur.execute(query)

    results = cur.fetchall()
    conn.close()
    return results


def get_recipe_category_counts():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT category, COUNT(*) AS recipe_count
        FROM recipes
        GROUP BY category
        ORDER BY recipe_count DESC
    """)

    results = cur.fetchall()
    conn.close()
    return results


def get_all_recipes():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, category, ingredient_count, total_time_minutes
        FROM recipes
        ORDER BY name
    """)

    results = cur.fetchall()
    conn.close()
    return results


def get_recipe_details(recipe_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, category, ingredient_count, total_time_minutes, instructions, thumbnail_url
        FROM recipes
        WHERE id = ?
    """, (recipe_id,))

    recipe = cur.fetchone()

    cur.execute("""
        SELECT ingredients.name, recipe_ingredients.measure
        FROM recipe_ingredients
        JOIN ingredients ON ingredients.id = recipe_ingredients.ingredient_id
        WHERE recipe_ingredients.recipe_id = ?
        ORDER BY ingredients.name
    """, (recipe_id,))

    ingredients = cur.fetchall()

    conn.close()
    return recipe, ingredients


def get_saved_recipes(saver_name):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT recipes.id, recipes.name, recipes.category,
               recipes.ingredient_count, recipes.total_time_minutes
        FROM saved_recipes
        JOIN recipes ON recipes.id = saved_recipes.recipe_id
        WHERE saved_recipes.saver_name = ?
        ORDER BY saved_recipes.saved_at DESC
    """, (saver_name,))

    results = cur.fetchall()
    conn.close()
    return results


def is_recipe_saved(saver_name, recipe_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 1 FROM saved_recipes
        WHERE saver_name = ? AND recipe_id = ?
    """, (saver_name, recipe_id))

    result = cur.fetchone()
    conn.close()
    return result is not None


if __name__ == "__main__":
    print("Top ingredients:")
    for name, count in get_top_ingredients():
        print(f"{name}: {count}")

    print("\nBeginner-friendly recipes:")
    for name, category, ingredient_count, total_time in get_beginner_friendly_recipes():
        print(
            f"{name} | {category} | Ingredients: {ingredient_count} | Time: {total_time} min")

    print("\nTime category counts:")
    for time_category, recipe_count in get_time_category_counts():
        print(f"{time_category}: {recipe_count}")

    print("\nRecipe complexity:")
    for name, category, ingredient_count, complexity in get_recipe_complexity():
        print(
            f"{name} | {category} | Ingredients: {ingredient_count} | Complexity: {complexity}")

    print("\nRecipe category counts:")
    for category, recipe_count in get_recipe_category_counts():
        print(f"{category}: {recipe_count}")
