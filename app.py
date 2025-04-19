from PIL import Image
import streamlit as st
import base64
import requests
import json
from recipe_finder import find_recipes
from config import GOOGLE_VISION_API_KEY
from model import RecipeGenerator  # Import the recipe generation model

# Function to call Google Vision API
def detect_ingredients(image_data, api_key):
    vision_api_url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    image_content = base64.b64encode(image_data).decode('utf-8')
    request_body = {
        "requests": [{
            "image": {"content": image_content},
            "features": [{"type": "LABEL_DETECTION", "maxResults": 15}]
        }]
    }
    response = requests.post(vision_api_url, json=request_body)
    response.raise_for_status()
    labels = response.json()['responses'][0].get('labelAnnotations', [])
    return [label['description'].lower() for label in labels]

# Load recipes from JSON file
with open('recipes.json', 'r') as f:
    recipes = json.load(f)

# Initialize Recipe Generator
recipe_generator = RecipeGenerator()

# Streamlit app UI
st.set_page_config(page_title="AI Recipe Recommender", layout="centered")
st.title("🥘 AI Cooking Recipe Recommender")
st.write("Upload an image of ingredients and get personalized recipes!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    try:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Step 1: Detect ingredients using Google Vision API
        image_bytes = uploaded_file.read()
        detected_ingredients = detect_ingredients(image_bytes, GOOGLE_VISION_API_KEY)

        st.subheader("✅ Detected Ingredients")
        st.write(', '.join(detected_ingredients))

        # Step 2: Generate a recipe using the model
        generated_recipe = recipe_generator.generate(image)  # Generate recipe from the image

        st.subheader("🍽️ Generated Recipe")
        st.markdown(f"### {generated_recipe['title']}")
        st.write("**Ingredients:**", ', '.join(generated_recipe.get('ingredients', [])))
        st.write("**Instructions:**", generated_recipe.get('instructions', 'No instructions provided.'))
        if generated_recipe.get('image'):
            st.image(generated_recipe['image'], use_column_width=True)

        # Step 3: Match the detected ingredients with the recipes
        matched_recipes = find_recipes(detected_ingredients, recipes)

        if matched_recipes:
            st.subheader("🍽️ Matching Recipes")
            for recipe in matched_recipes:
                st.markdown(f"### {recipe['title']}")
                st.write("**Ingredients:**", ', '.join(recipe.get('ingredients', [])))
                st.write("**Instructions:**", recipe.get('instructions', 'No instructions provided.'))
                if recipe.get('image'):
                    st.image(recipe['image'], use_column_width=True)
        else:
            st.warning("No matching recipes found.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
