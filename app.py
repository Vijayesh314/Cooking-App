import streamlit as st
from detect_ingredients import detect_ingredients
from recipe_finder import find_recipes
import tempfile

st.title("🍳 AI Cooking Recipe Recommender")
st.write("Upload a photo of your ingredients and get personalized recipes!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        image_path = tmp_file.name

    st.image(image_path, caption="Your Uploaded Ingredients", use_column_width=True)
    st.write("🔍 Detecting ingredients...")

    ingredients_obj = detect_ingredients(image_path)
    ingredients = ingredients_obj()  # Call the object to get the list
    st.success(f"✅ Detected Ingredients: {ingredients_obj}")

    st.write("🍽️ Finding matching recipes...")
    recipes = find_recipes(ingredients)

    if recipes:
        for recipe in recipes:
            st.subheader(recipe['title'])
            if recipe['image']:
                st.image(recipe['image'])
            st.write("**Ingredients:**", ", ".join(recipe['ingredients']))
            if recipe['missing_ingredients']:
                st.warning(f"Missing: {', '.join(recipe['missing_ingredients'])}")
            st.write("**Instructions:**", recipe['instructions'])
    else:
        st.error("No recipes found with your ingredients.")