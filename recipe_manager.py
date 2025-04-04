import requests

class RecipeManager:
    def __init__(self, api_key, pantry):
        self.api_key = api_key
        self.pantry = pantry

    def meal_plan(self, preferences):
        url = "https://api.spoonacular.com/recipes/complexSearch"
        params = {
            "apiKey": self.api_key,
            "includeIngredients": ",".join(self.pantry.keys()),  # Use pantry items
            "diet": preferences.get("diet", ""),  # E.g., "vegetarian"
            "intolerances": ",".join(preferences.get("allergies", [])),  # E.g., "dairy, gluten"
            "number": 5,  # Get 5 results
            "instructionsRequired": True,
            "addRecipeInformation": True
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            recipes = response.json().get("results", [])
            return [
                {
                    "name": recipe["title"],
                    "ingredients": [ingredient["name"] for ingredient in recipe.get("extendedIngredients", [])],
                    "url": recipe["sourceUrl"]
                }
                for recipe in recipes
            ]
        else:
            return None