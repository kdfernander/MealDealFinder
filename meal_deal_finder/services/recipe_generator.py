import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SPOONACULAR_API_KEY")

class RecipeGenerator:
    def __init__(self, pantry_df):
        self.api_key = API_KEY
        self.pantry_items = self._clean_pantry_items(pantry_df)

    def _clean_pantry_items(self, pantry_df):
        items = []
        for item in pantry_df["Item Name"].dropna():
            if isinstance(item, str) and item.strip():
                # Lowercase and take the first word for simplicity
                cleaned = re.sub(r"[^a-zA-Z\\s]", "", item.lower()).strip().split()[0]
                items.append(cleaned)
        return list(set(items))  # Remove duplicates

    def find_recipes(self, number=5, diet=None, intolerances=None):
        if not self.pantry_items or len(self.pantry_items) < 2:
            print("⚠️ Not enough pantry items.")
            return []

        url = "https://api.spoonacular.com/recipes/complexSearch"

        params = {
            "apiKey": self.api_key,
            "includeIngredients": ",".join(self.pantry_items),
            "number": number * 3,  # Get more to filter down to good ones
            "addRecipeInformation": True,
            "instructionsRequired": True,
            "fillIngredients": True
        }

        if diet:
            params["diet"] = diet
        if intolerances:
            params["intolerances"] = ",".join(intolerances)

        print("📡 Querying Spoonacular with:")
        for k, v in params.items():
            print(f"  {k}: {v}")

        response = requests.get(url, params=params)
        if response.status_code == 200:
            recipes = response.json().get("results", [])
            # Keep only recipes with at least 2 matching pantry ingredients
            filtered = [
                r for r in recipes
                if r.get("instructions") and r.get("extendedIngredients")
                and sum(ing["name"].lower() in self.pantry_items for ing in r["extendedIngredients"]) >= 2
            ]
            print(f"✅ Found {len(filtered)} recipes with at least 2 matching ingredients.")
            return filtered[:number]  # Return top N
        else:
            print("🚨 API ERROR:", response.status_code, response.text)
            return []