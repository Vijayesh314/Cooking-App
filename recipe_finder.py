import json

def normalize(ingredient):
    replacements = [
        ("ground ", ""),
        ("shredded ", ""),
        ("romaine ", ""),
        ("fresh ", ""),
        ("diced ", ""),
        ("minced ", ""),
        ("chopped ", ""),
        ("crushed ", ""),
        ("sliced ", ""),
        ("shells", "shell"),
    ]
    ingredient = ingredient.lower()
    for old, new in replacements:
        ingredient = ingredient.replace(old, new)
    return ingredient.strip()

def find_recipes(detected_ingredients):
    with open("recipes.json", "r") as f:
        recipes = json.load(f)

    #Normalize detected ingredients too
    detected = [normalize(i) for i in detected_ingredients]

    result = []
    for recipe in recipes:
        if "ingredients" not in recipe:
            continue
        recipe_ingredients = [normalize(i) for i in recipe["ingredients"]]
        matched = [i for i in recipe_ingredients if i in detected]
        missing = [i for i in recipe_ingredients if i not in detected]

        if matched:
            result.append({
                "title": recipe["title"],
                "ingredients": recipe_ingredients,
                "missing_ingredients": missing,
                "instructions": recipe.get("instructions", "No instructions."),
                "image": recipe.get("image")
            })
    return result
