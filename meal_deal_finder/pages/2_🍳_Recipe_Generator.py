import streamlit as st
from services.pantry_manager import PantryManager
from services.recipe_generator import RecipeGenerator

st.set_page_config(page_title="Recipe Generator", layout="centered")

st.title("🍳 Recipe Generator")
st.markdown("Recipes based on your pantry, diet, and allergies.")

# --- Load Pantry ---
pantry_manager = PantryManager(st.session_state)
pantry_df = pantry_manager.get_pantry()

if pantry_df.empty:
    st.warning("Your pantry is empty. Add ingredients in the Pantry Manager.")
    st.stop()

# --- Filters Form ---
with st.form("filter_form"):
    st.subheader("⚙️ Recipe Filters")

    col1, col2 = st.columns(2)

    diet = col1.selectbox("Dietary Preference", [
        "", "vegetarian", "vegan", "pescetarian", "ketogenic", "gluten free"
    ])

    intolerances = col2.multiselect("Allergies / Intolerances", [
        "dairy", "egg", "gluten", "grain", "peanut", "seafood", "sesame",
        "shellfish", "soy", "sulfite", "tree nut", "wheat"
    ])

    submitted = st.form_submit_button("🔄 Generate Recipes")

if submitted:
    generator = RecipeGenerator(pantry_df)
    recipes = generator.find_recipes(
        number=5,
        diet=diet if diet else None,
        intolerances=intolerances
    )

    if not recipes:
        st.error("🚫 No recipes found. Try fewer restrictions or different pantry items.")
    else:
        st.success(f"✅ Found {len(recipes)} recipes.")
        for recipe in recipes:
            with st.expander(recipe["title"]):
                st.image(recipe["image"], width=300)

                st.subheader("📝 Ingredients")
                for ing in recipe.get("extendedIngredients", []):
                    st.markdown(f"- {ing.get('original', ing.get('name', 'Unknown'))}")

                st.subheader("📋 Instructions")
                st.markdown(recipe.get("instructions", "No instructions provided."), unsafe_allow_html=True)