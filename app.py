import streamlit as st
import os
from PIL import Image
import pytesseract
from src.database import init_db, save_recipe

# Initialisation
if not os.path.exists("data"): os.makedirs("data")
init_db()

st.title("Porte-vue : gestion de recettes")

uploaded_file = st.file_uploader("Choisis une image de recette", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Sauvegarde locale
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.image(uploaded_file, caption="Recette chargée")
    
    if st.button("Lancer l'OCR"):
        # Extraction texte
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img, lang='fra')
        
        # Affichage résultat
        st.subheader("Texte extrait")
        st.text(text)
        
        # Sauvegarde BDD
        save_recipe(file_path, text, "")
        st.success("Recette enregistrée dans la base")