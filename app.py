import streamlit as st
from detect_ingredients import detect_ingredients
from recipe_finder import find_recipes
import tempfile
import os
from PIL import Image
import io

# Constants
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

st.title("AI Cooking Recipe Recommender")
st.write("Upload a photo of your ingredients and get personalized recipes!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Validate file size
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("File size too large. Please upload an image smaller than 5MB.")
        st.stop()
    
    try:
        image = Image.open(io.BytesIO(uploaded_file.read()))
        image.verify() 
        uploaded_file.seek(0)
    except Exception as e:
        st.error("Invalid image file. Please upload a valid JPG, JPEG, or PNG image.")
        st.stop()

    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        tmp_file.write(uploaded_file.read())
        image_path = tmp_file.name

    try:
        st.image(image_path, caption="Your Uploaded Ingredients", use_column_width=True)
        
        with st.spinner("🔍 Detecting ingredients..."):
            ingredients_obj = detect_ingredients(image_path)
            ingredients = ingredients_obj()  # Call the object to get the list
        
        if not ingredients:
            st.error("Could not detect any ingredients in the image. Please try another photo.")
            st.stop()
            
        st.success(f"✅ Detected Ingredients: {', '.join(ingredients)}")

        with st.spinner("🍽️ Finding matching recipes..."):
            recipes = find_recipes(ingredients)

        if recipes:
            for recipe in recipes:
                with st.expander(recipe['title']):
                    if recipe['image']:
                        st.image(recipe['image'])
                    st.write("**Ingredients:**", ", ".join(recipe['ingredients']))
                    if recipe['missing_ingredients']:
                        st.warning(f"Missing: {', '.join(recipe['missing_ingredients'])}")
                    st.write("**Instructions:**", recipe['instructions'])
        else:
            st.error("No recipes found with your ingredients.")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    finally:
        try:
            os.unlink(image_path)
        except:
            pass
