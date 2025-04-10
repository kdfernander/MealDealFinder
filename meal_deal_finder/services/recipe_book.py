class RecipeBook:
    def __init__(self, session_state):
        self.session_state = session_state
        if 'recipe_book' not in self.session_state:
            self.session_state.recipe_book = []

    def save_recipe(self, recipe_details):
        recipe_data = {
            "id": recipe_details.get("id", f"custom_{len(self.session_state.recipe_book)}"),
            "title": recipe_details["title"],
            "image": recipe_details.get("image", ""),
            "ingredients": [i.get("original", i.get("name", "Unknown")) for i in recipe_details.get("extendedIngredients", [])],
            "ingredient_names": [i.get("name", "").lower() for i in recipe_details.get("extendedIngredients", [])],
            "instructions": recipe_details.get("instructions", "No instructions provided."),
            "meal_type": recipe_details.get("meal_type", "unspecified"),
            "source": recipe_details.get("source", "api")
        }

        if not any(r["title"] == recipe_data["title"] for r in self.session_state.recipe_book):
            self.session_state.recipe_book.append(recipe_data)

    def add_custom_recipe(self, title, ingredients_text, instructions, meal_type="unspecified"):
        ingredients = [line.strip() for line in ingredients_text.split("\n") if line.strip()]
        ingredient_names = [line.split()[0].lower() for line in ingredients]

        recipe_data = {
            "id": f"custom_{len(self.session_state.recipe_book)}",
            "title": title,
            "image": "",  # No image for custom entries
            "ingredients": ingredients,
            "ingredient_names": ingredient_names,
            "instructions": instructions,
            "meal_type": meal_type,
            "source": "custom"
        }

        self.session_state.recipe_book.append(recipe_data)

    def get_saved_recipes(self):
        return self.session_state.recipe_book

    def remove_recipe(self, recipe_id):
        self.session_state.recipe_book = [
            r for r in self.session_state.recipe_book if r["id"] != recipe_id
        ]

    def plan_meal(self, recipe_id):
        recipe = next((r for r in self.session_state.recipe_book if r["id"] == recipe_id), None)
        if recipe:
            pantry_names = set(self.session_state.pantry["Item Name"].str.lower())
            missing = [i for i in recipe["ingredient_names"] if i not in pantry_names]

            from services.shopping_cart import ShoppingCart
            cart = ShoppingCart(self.session_state)
            cart.add_missing_ingredients(missing)