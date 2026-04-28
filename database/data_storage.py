import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "baking_recipes.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key TEXT UNIQUE,
            name TEXT,
            category TEXT,
            ingredient_count INTEGER
        )
    """)

    try:
        cur.execute("ALTER TABLE recipes ADD COLUMN total_time_minutes INTEGER")
    except sqlite3.OperationalError:
        pass

    try:
        cur.execute("ALTER TABLE recipes ADD COLUMN instructions TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        cur.execute("ALTER TABLE recipes ADD COLUMN thumbnail_url TEXT")
    except sqlite3.OperationalError:
        pass

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            recipe_id INTEGER,
            ingredient_id INTEGER,
            measure TEXT,
            PRIMARY KEY (recipe_id, ingredient_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id),
            FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
        )
    """)

    conn.commit()
    conn.close()

def upsert_recipe(recipe):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO recipes (
            api_key, name, category, ingredient_count,
            total_time_minutes, instructions, thumbnail_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(api_key) DO UPDATE SET
            name=excluded.name,
            category=excluded.category,
            ingredient_count=excluded.ingredient_count,
            total_time_minutes=excluded.total_time_minutes,
            instructions=excluded.instructions,
            thumbnail_url=excluded.thumbnail_url
    """, (
        recipe["api_key"],
        recipe["name"],
        recipe["category"],
        recipe["ingredient_count"],
        recipe.get("total_time_minutes"),
        recipe.get("instructions"),
        recipe.get("thumbnail_url")
    ))

    conn.commit()

    cur.execute("SELECT id FROM recipes WHERE api_key = ?", (recipe["api_key"],))
    recipe_id = cur.fetchone()[0]

    conn.close()
    return recipe_id

def upsert_ingredient(name: str) -> int:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO ingredients (name) VALUES (?)", (name,))
    conn.commit()

    cur.execute("SELECT id FROM ingredients WHERE name = ?", (name,))
    ingredient_id = cur.fetchone()[0]

    conn.close()
    return ingredient_id

def link_recipe_ingredient(recipe_id: int, ingredient_id: int, measure: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO recipe_ingredients (recipe_id, ingredient_id, measure)
        VALUES (?, ?, ?)
    """, (recipe_id, ingredient_id, measure))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(recipes)")
    print("RECIPES COLUMNS:")
    for col in cur.fetchall():
        print(col)

    cur.execute("SELECT id, name, total_time_minutes, instructions, thumbnail_url FROM recipes LIMIT 5")
    print("\nRECIPES DATA:")
    for row in cur.fetchall():
        print(row)

    conn.close()

