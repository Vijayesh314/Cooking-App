import base64
import requests
from config import GOOGLE_VISION_API_KEY

class Ingredients:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    def __str__(self):
        return ', '.join(self.ingredients)
    
    def __repr__(self):
        return f"Ingredients({self.ingredients})"
    
    def __call__(self):
        return self.ingredients

def detect_ingredients(image_path):
    try:
        with open(image_path, "rb") as image_file:
            content = base64.b64encode(image_file.read()).decode("utf-8")

        url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}"
        request_body = {
            "requests": [
                {
                    "image": {"content": content},
                    "features": [{"type": "LABEL_DETECTION", "maxResults": 10}]
                }
            ]
        }

        response = requests.post(url, json=request_body)
        response.raise_for_status()
        
        data = response.json()
        if "responses" not in data or not data["responses"]:
            return Ingredients([])
            
        labels = data["responses"][0].get("labelAnnotations", [])
        ingredients_list = [label["description"].lower() for label in labels]

        return Ingredients(ingredients_list)
        
    except Exception as e:
        print(f"Error detecting ingredients: {str(e)}")
        return Ingredients([])
