import streamlit as st
from recipe_manager import RecipeManager

st.title("🍽️ Meal Planning")

api_key = "03b0726598ff44d59ae27d0905b05c8f"
recipe_manager = RecipeManager(api_key, st.session_state.pantry)

diet = st.selectbox("Diet Preference", ["None", "Vegetarian", "Vegan", "Keto", "Paleo"])
allergies = st.multiselect("Allergies to Avoid", ["Dairy", "Gluten", "Peanuts", "Shellfish", "Soy"])

preferences = {
    "diet": diet.lower() if diet != "None" else "",
    "allergies": [allergy.lower() for allergy in allergies],
}

meal_plan = recipe_manager.meal_plan(preferences)

if meal_plan:
    for meal in meal_plan:
        st.write(f"**{meal['name']}**")
        st.write(f"Ingredients: {', '.join(meal['ingredients'])}")
        st.write(f"[View Recipe]({meal['url']})")
else:
    st.write("No meal plan found based on your preferences.")