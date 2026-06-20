"""
Porte-vue - Application Streamlit pour gérer des recettes de cuisine.

Cette application permet d'importer des images de recettes,
d'extraire le texte par OCR et de les organiser dans une galerie.
"""

import streamlit as st
import os
import pytesseract
from PIL import Image
from pathlib import Path

from src.database import init_db, save_recipe, get_all_recipes
from src.processing import crop_ui_elements


# Configuration des constantes
DATA_DIR = Path("data")
CROPPED_DIR = DATA_DIR / "cropped"
SUPPORTED_IMAGE_TYPES = ["jpg", "jpeg", "png"]


def setup_directories() -> None:
    """Crée les répertoires nécessaires s'ils n'existent pas."""
    CROPPED_DIR.mkdir(parents=True, exist_ok=True)


def initialize_app() -> None:
    """Initialise l'application (répertoories et base de données)."""
    setup_directories()
    init_db()


def display_add_recipe_page() -> None:
    """Affiche la page pour ajouter une nouvelle recette."""
    st.title("Nouvelle recette")
    
    uploaded_file = st.file_uploader(
        "Choisis une image",
        type=SUPPORTED_IMAGE_TYPES
    )
    
    if uploaded_file is not None:
        original_path = DATA_DIR / uploaded_file.name
        
        # Sauvegarde de l'image originale
        with open(original_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.image(str(original_path), caption="Image originale", use_container_width=True)
        
        if st.button("Traiter et Enregistrer"):
            with st.spinner("Traitement en cours..."):
                # Génération du nom de fichier rogné
                cropped_filename = f"crop_{uploaded_file.name}"
                cropped_path = CROPPED_DIR / cropped_filename
                
                # Traitement de l'image
                crop_ui_elements(str(original_path), str(cropped_path))
                
                # Extraction du texte par OCR
                img_to_ocr = Image.open(cropped_path)
                text = pytesseract.image_to_string(img_to_ocr, lang='fra')
                
                # Sauvegarde dans la base de données
                save_recipe(str(cropped_path), text, "")
                
                st.success("Recette enregistrée.")


def display_gallery_page() -> None:
    """Affiche la galerie des recettes."""
    st.title("Mon porte-vue")
    
    # Moteur de recherche
    search_term = st.text_input("Rechercher un ingrédient ou un mot-clé", "")
    recipes = get_all_recipes(search_term)
    
    if not recipes:
        st.info("Aucune recette à afficher.")
        return
    
    # Création d'une grille de 3 colonnes
    cols = st.columns(3)
    
    for index, recipe in enumerate(recipes):
        recipe_id, filename, ocr_text, tags, created_at = recipe
        
        with cols[index % 3]:
            st.container(border=True)
            if os.path.exists(filename):
                st.image(filename, use_container_width=True)
                
                # Le texte OCR est masqué par défaut dans un accordéon
                with st.expander("Voir le texte extrait"):
                    st.text(ocr_text)
            else:
                st.error("Fichier image introuvable.")


def main() -> None:
    """Fonction principale de l'application."""
    # Initialisation
    initialize_app()
    
    # Configuration de la page
    st.set_page_config(page_title="Porte-vue", layout="wide")
    
    # Navigation
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Menu", ["Galerie", "Ajouter une recette"])
    
    if menu == "Ajouter une recette":
        display_add_recipe_page()
    elif menu == "Galerie":
        display_gallery_page()


if __name__ == "__main__":
    main()