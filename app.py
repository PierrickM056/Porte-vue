import streamlit as st
import os
import pytesseract
from PIL import Image
from src.database import init_db, save_recipe, get_all_recipes
from src.processing import crop_ui_elements

# Initialisation
if not os.path.exists("data/cropped"): os.makedirs("data/cropped")
init_db()

# Configuration de la page
st.set_page_config(page_title="Porte-vue", layout="wide")

# Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Menu", ["Galerie", "Ajouter une recette"])

if menu == "Ajouter une recette":
    st.title("Nouvelle recette")
    
    uploaded_file = st.file_uploader("Choisis une image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        original_path = os.path.join("data", uploaded_file.name)
        with open(original_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.image(original_path, caption="Image originale", use_container_width=True)
        
        if st.button("Traiter et Enregistrer"):
            with st.spinner("Traitement en cours..."):
                cropped_filename = f"crop_{uploaded_file.name}"
                cropped_path = os.path.join("data/cropped", cropped_filename)
                
                crop_ui_elements(original_path, cropped_path)
                
                img_to_ocr = Image.open(cropped_path)
                text = pytesseract.image_to_string(img_to_ocr, lang='fra')
                
                save_recipe(cropped_path, text, "")
                st.success("Recette enregistrée.")

elif menu == "Galerie":
    st.title("Mon porte-vue")
    
    # Moteur de recherche
    search_term = st.text_input("Rechercher un ingrédient ou un mot-clé", "")
    recipes = get_all_recipes(search_term)
    
    if not recipes:
        st.info("Aucune recette à afficher.")
    else:
        # Création d'une grille de 3 colonnes
        cols = st.columns(3)
        
        for index, recipe in enumerate(recipes):
            recipe_id, filename, ocr_text, tags, created_at = recipe
            
            # Répartition dans les colonnes (0, 1, 2, 0, 1, 2...)
            with cols[index % 3]:
                st.container(border=True)
                if os.path.exists(filename):
                    st.image(filename, use_container_width=True)
                    
                    # Le texte OCR est masqué par défaut dans un accordéon
                    with st.expander("Voir le texte extrait"):
                        st.text(ocr_text)
                else:
                    st.error("Fichier image introuvable.")