from analysis_logic import (
    get_top_ingredients,
    get_beginner_friendly_recipes,
    get_time_category_counts,
    get_recipe_complexity,
    get_recipe_category_counts
)

def show_top_ingredients():
    print("\n--- Top Ingredients ---")
    results = get_top_ingredients()
    for name, count in results:
        print(f"{name}: {count}")

def show_beginner_friendly():
    print("\n--- Beginner-Friendly Recipes ---")
    results = get_beginner_friendly_recipes()
    for name, category, ingredient_count, total_time in results:
        print(f"{name} | {category} | Ingredients: {ingredient_count} | Time: {total_time} min")

def show_time_categories():
    print("\n--- Time Category Counts ---")
    results = get_time_category_counts()
    for time_category, recipe_count in results:
        print(f"{time_category}: {recipe_count}")

def show_recipe_complexity():
    print("\n--- Recipe Complexity ---")
    results = get_recipe_complexity(limit=12)
    for name, category, ingredient_count, complexity in results:
        print(f"{name} | {category} | Ingredients: {ingredient_count} | Complexity: {complexity}")

def show_recipe_categories():
    print("\n--- Recipe Category Counts ---")
    results = get_recipe_category_counts()
    for category, recipe_count in results:
        print(f"{category}: {recipe_count}")

def main():
    while True:
        print("\nWelcome to BakersParadise!")
        print("Explore baking recipe analytics from the database.")
        print("1. Show top ingredients")
        print("2. Show beginner-friendly recipes")
        print("3. Show time category counts")
        print("4. Show recipe complexity")
        print("5. Show recipe category counts")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_top_ingredients()
        elif choice == "2":
            show_beginner_friendly()
        elif choice == "3":
            show_time_categories()
        elif choice == "4":
            show_recipe_complexity()
        elif choice == "5":
            show_recipe_categories()
        elif choice == "6":
            print("Exiting BakersParadise Dashboard.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()
