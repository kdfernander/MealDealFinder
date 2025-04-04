import streamlit as st
import json
import os
import streamlit_nested_layout  # Required for nesting columns

PANTRY_FILE = "pantry_data.json"

if "pantry" not in st.session_state:
    if os.path.exists(PANTRY_FILE):
        with open(PANTRY_FILE, "r") as f:
            st.session_state.pantry = json.load(f)
    else:
        st.session_state.pantry = {
            "Dairy": {},
            "Produce": {},
            "Grains": {},
            "Proteins": {},
            "Others": {}
        }



# Function to save pantry data
def save_pantry():
    with open(PANTRY_FILE, "w") as f:
        json.dump(st.session_state.pantry, f, indent=4)

# Initialize session state variables
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = {}

if "buy_again" not in st.session_state:
    st.session_state.buy_again = {}

# Move items to "Buy Again" list if marked for restock
for category, items in list(st.session_state.pantry.items()):
    for ingredient, details in list(items.items()):
        if details.get("restock", False):
            if category not in st.session_state.buy_again:
                st.session_state.buy_again[category] = {}

            # Move item to "Buy Again"
            st.session_state.buy_again[category][ingredient] = details
            del st.session_state.pantry[category][ingredient]
            save_pantry()

st.markdown("<br>", unsafe_allow_html=True)

# "Buy Again" Section
with st.expander("🛒 Buy Again", expanded=True):
    if st.session_state.buy_again:
        for category, ingredient_data in list(st.session_state.buy_again.items()):
            for ingredient, details in list(ingredient_data.items()):
                cols = st.columns([3, 2, 2, 1.5])
                with cols[0]:
                    st.markdown(f"**{ingredient}**")
                with cols[1]:
                    st.markdown(f"{details['amount']}")
                with cols[2]:
                    st.markdown("🔴 Needs Restock")
                with cols[3]:
                    if st.button("✅ Mark as Restocked", key=f"restock_{category}_{ingredient}"):
                        # Move item back to pantry
                        if category not in st.session_state.pantry:
                            st.session_state.pantry[category] = {}
                        st.session_state.pantry[category][ingredient] = {"amount": details["amount"], "restock": False}

                        # Remove from Buy Again list
                        del st.session_state.buy_again[category][ingredient]
                        if not st.session_state.buy_again[category]:
                            del st.session_state.buy_again[category]

                        save_pantry()

    else:
        st.markdown("🎉 All items are in stock!")

st.markdown("<br>", unsafe_allow_html=True)

# Pantry Management Section
with st.expander("🗂️ Pantry", expanded=True):
    # "Add an Ingredient" Section
    with st.expander("➕ Add an Ingredient", expanded=True):
        with st.form("ingredient_form"):
            ingredient = st.text_input("Ingredient Name")
            category = st.selectbox("Category", ["Dairy", "Produce", "Grains", "Proteins", "Others"])
            amount = st.text_input("Amount (e.g., '1 liter', '500 g', '2 packs')")
            submit = st.form_submit_button("Add Ingredient")

            if submit and ingredient.strip() and amount.strip():
                st.session_state.pantry[category][ingredient.strip()] = {"amount": amount.strip(), "restock": False}
                save_pantry()
                st.success(f"Added {ingredient} ({amount}) to {category}!")

    st.markdown("<br>", unsafe_allow_html=True)

    # Display categorized ingredients in expandable sections
    for category, items in list(st.session_state.pantry.items()):
        if items:
            with st.expander(f"📂 {category}", expanded=True):
                with st.container(border=True):
                    cols = st.columns([3, 2, 2, 1.5, 1])

                    with cols[0]:
                        st.markdown("**Ingredient**")
                    with cols[1]:
                        st.markdown("**Quantity**")
                    with cols[2]:
                        st.markdown("**Restock**")
                    with cols[3]:
                        st.markdown("**Edit**")
                    with cols[4]:
                        st.markdown("**Delete**")

                    st.markdown("<hr>", unsafe_allow_html=True)

                    # Display each ingredient
                    for ingredient, details in list(items.items()):
                        cols = st.columns([3, 2, 2, 1.5, 1])

                        if (category, ingredient) in st.session_state.edit_mode and st.session_state.edit_mode[
                            (category, ingredient)]:
                            # Editable Fields
                            with cols[0]:
                                new_name = st.text_input("Ingredient Name", value=ingredient, key=f"name_{category}_{ingredient}")
                            with cols[1]:
                                new_amount = st.text_input("Amount", value=details["amount"], key=f"amount_{category}_{ingredient}")
                            with cols[2]:
                                new_restock = st.checkbox("Restock", value=details["restock"], key=f"restock_{category}_{ingredient}")
                            with cols[3]:
                                if st.button("💾", key=f"save_{category}_{ingredient}"):
                                    st.session_state.pantry[category][new_name] = {
                                        "amount": new_amount,
                                        "restock": new_restock
                                    }
                                    if new_name != ingredient:
                                        del st.session_state.pantry[category][ingredient]

                                    save_pantry()
                                    st.session_state.edit_mode[(category, ingredient)] = False
                            with cols[4]:
                                if st.button("❌", key=f"delete_{category}_{ingredient}"):
                                    del st.session_state.pantry[category][ingredient]
                                    save_pantry()
                        else:
                            # Display Static Text
                            with cols[0]:
                                st.markdown(f"**{ingredient}**")
                            with cols[1]:
                                st.markdown(f"{details['amount']}")
                            with cols[2]:
                                restock_text = "🔴 Needs Restock" if details["restock"] else "🟢 In Stock"
                                st.markdown(f"{restock_text}")
                            with cols[3]:
                                if st.button("✏️", key=f"edit_{category}_{ingredient}"):
                                    st.session_state.edit_mode[(category, ingredient)] = True
                            with cols[4]:
                                if st.button("❌", key=f"delete_{category}_{ingredient}"):
                                    del st.session_state.pantry[category][ingredient]
                                    save_pantry()

st.markdown("<br><br>", unsafe_allow_html=True)

# Footer
st.write("👨‍🍳 Plan your meals, find the best deals, and make grocery shopping easier!")
