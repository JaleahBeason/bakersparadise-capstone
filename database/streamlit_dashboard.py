import streamlit as st
import pandas as pd

from analysis_logic import (
    get_top_ingredients,
    get_beginner_friendly_recipes,
    get_time_category_counts,
    get_recipe_complexity,
    get_recipe_category_counts,
    get_all_recipes,
    get_recipe_details
)

st.set_page_config(
    page_title="BakersParadise Dashboard",
    page_icon="🧁",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f8f6f2;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #eadfd6;
    padding: 16px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
div[data-testid="stSidebar"] {
    background-color: #fffaf5;
}
h1, h2, h3 {
    color: #3b2f2a;
}
</style>
""", unsafe_allow_html=True)

st.title("BakersParadise Dashboard")
st.caption("Automated Baking Recipe Analytics System")

# Session state page control
if "page" not in st.session_state:
    st.session_state["page"] = "Analytics Dashboard"

page = st.sidebar.radio(
    "Go to",
    ["Analytics Dashboard", "Recipe Explorer"],
    index=0 if st.session_state["page"] == "Analytics Dashboard" else 1
)

st.session_state["page"] = page


if page == "Analytics Dashboard":
    st.header("Analytics Dashboard")
    st.write("This page presents dataset-wide recipe analytics from the BakersParadise database.")

    top_ingredients = get_top_ingredients()
    beginner_recipes = get_beginner_friendly_recipes()
    time_categories = get_time_category_counts()
    recipe_categories = get_recipe_category_counts()

    top_ingredient_name = top_ingredients[0][0] if top_ingredients else "N/A"
    top_ingredient_count = top_ingredients[0][1] if top_ingredients else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Top Ingredient", top_ingredient_name)
    col2.metric("Ingredient Uses", top_ingredient_count)
    col3.metric("Beginner-Friendly Recipes", len(beginner_recipes))
    col4.metric("Recipe Categories", len(recipe_categories))

    st.divider()

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown("## Top Ingredients")
        ingredients_df = pd.DataFrame(top_ingredients, columns=["Ingredient", "Usage Count"])
        st.dataframe(ingredients_df, use_container_width=True)
        st.bar_chart(ingredients_df.set_index("Ingredient"))

    with right_col:
        st.markdown("## Beginner-Friendly Recipes")
        beginner_df = pd.DataFrame(
            beginner_recipes,
            columns=["Recipe", "Category", "Ingredient Count", "Total Time (min)"]
        )
        st.dataframe(beginner_df, use_container_width=True)

    st.divider()

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown("## Preparation Time Categories")
        time_df = pd.DataFrame(time_categories, columns=["Time Category", "Recipe Count"])
        st.dataframe(time_df, use_container_width=True)
        st.bar_chart(time_df.set_index("Time Category"))

    with right_col:
        st.markdown("## Recipe Category Counts")
        category_df = pd.DataFrame(recipe_categories, columns=["Category", "Recipe Count"])
        st.dataframe(category_df, use_container_width=True)
        st.bar_chart(category_df.set_index("Category"))

    st.divider()

    st.markdown("## Recipe Complexity")
    complexity_df = pd.DataFrame(
        get_recipe_complexity(),
        columns=["Recipe", "Category", "Ingredient Count", "Complexity"]
    )
    st.dataframe(complexity_df.head(12), use_container_width=True)
    st.caption("Complexity is based on ingredient count: Low (≤8), Medium (9–12), High (13+).")

    st.divider()

    st.markdown("## Explore a Recipe")
    st.write("Select a recipe from the database to open its full recipe detail page.")

    recipes = get_all_recipes()

    recipe_options = {
        f"{name} ({category})": recipe_id
        for recipe_id, name, category, ingredient_count, total_time in recipes
    }

    selected_recipe_label = st.selectbox(
        "Select a recipe to view in Recipe Explorer",
        list(recipe_options.keys()),
        key="analytics_recipe_select"
    )

    if st.button("Go to Recipe Explorer"):
        st.session_state["selected_recipe_id"] = recipe_options[selected_recipe_label]
        st.session_state["page"] = "Recipe Explorer"
        st.rerun()


elif page == "Recipe Explorer":
    st.header("Recipe Explorer")
    st.write("Select a recipe to view its image, ingredients, and instructions.")

    if st.button("← Back to Analytics Dashboard"):
        st.session_state["page"] = "Analytics Dashboard"
        st.rerun()

    recipes = get_all_recipes()

    recipe_options = {
        f"{name} ({category})": recipe_id
        for recipe_id, name, category, ingredient_count, total_time in recipes
    }

    default_index = 0
    if "selected_recipe_id" in st.session_state:
        recipe_ids = list(recipe_options.values())
        if st.session_state["selected_recipe_id"] in recipe_ids:
            default_index = recipe_ids.index(st.session_state["selected_recipe_id"])

    selected_label = st.selectbox(
        "Select a recipe",
        list(recipe_options.keys()),
        index=default_index
    )

    recipe_id = recipe_options[selected_label]
    recipe, ingredients = get_recipe_details(recipe_id)

    if recipe:
        name, category, ingredient_count, total_time, instructions, thumbnail_url = recipe

        st.subheader(name)

        if thumbnail_url:
            st.image(thumbnail_url, width=320)

        col1, col2, col3 = st.columns(3)
        col1.metric("Category", category)
        col2.metric("Ingredients", ingredient_count)
        col3.metric("Estimated Time", f"{total_time} min")

        left, right = st.columns([1, 2])

        with left:
            st.markdown("### Ingredients")
            for ingredient_name, measure in ingredients:
                st.write(f"- {ingredient_name}: {measure}")

        with right:
            st.markdown("### Instructions")
            st.write(instructions if instructions else "No instructions available.")