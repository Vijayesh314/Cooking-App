import requests
import base64
from config import GOOGLE_VISION_API_KEY

class Ingredients:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    def __str__(self):
        return ', '.join(self.ingredients)

    def __repr__(self):
        return f"Ingredients({self.ingredients})"

    def __call__(self, *args, **kwargs):
        return self.ingredients

def detect_ingredients(image_path):
    with open(image_path, "rb") as image_file:
        content = base64.b64encode(image_file.read()).decode("utf-8")

    url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}"
    headers = {"Content-Type": "application/json"}
    body = {
        "requests": [
            {
                "image": {"content": content},
                "features": [{"type": "LABEL_DETECTION", "maxResults": 10}]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    labels = response.json()["responses"][0].get("labelAnnotations", [])
    ingredients = [label["description"].lower() for label in labels]
    return Ingredients(ingredients)
