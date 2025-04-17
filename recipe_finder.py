import json

def load_recipes(file="recipes.json"):
    with open(file, "r") as f:
        return json.load(f)

def find_recipes(user_ingredients, max_missing=1):
    recipes = load_recipes()
    matched = []

    for recipe in recipes:
        missing = [ing for ing in recipe["ingredients"] if ing not in user_ingredients]
        if len(missing) <= max_missing:
            matched.append({
                "title": recipe["title"],
                "ingredients": recipe["ingredients"],
                "missing_ingredients": missing,
                "instructions": recipe["instructions"],
                "image": recipe.get("image", "")
            })

    return matched