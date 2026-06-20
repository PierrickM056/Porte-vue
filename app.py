"""
Porte-vue - Application Streamlit pour l'archivage et la recherche de documents.

Cette application permet d'importer des images de documents (articles de presse, etc.),
d'extraire le texte par OCR et de les organiser dans un fonds documentaire.
"""

import streamlit as st
import os
import pytesseract
from PIL import Image
from pathlib import Path
from typing import Optional

from src.database import init_db, save_article, get_all_articles
from src.processing import crop_ui_elements


# Configuration des constantes
DATA_DIR = Path("data")
CROPPED_DIR = DATA_DIR / "cropped"
SUPPORTED_IMAGE_TYPES = ["jpg", "jpeg", "png"]


def setup_directories() -> None:
    """Crée les répertoires nécessaires s'ils n'existent pas."""
    CROPPED_DIR.mkdir(parents=True, exist_ok=True)


def initialize_app() -> None:
    """Initialise l'application (répertoires et base de données)."""
    setup_directories()
    init_db()


def display_add_article_page() -> None:
    """Affiche la page pour ajouter un nouvel article."""
    st.title("Nouvel article")
    
    uploaded_file = st.file_uploader(
        "Choisis une image de document",
        type=SUPPORTED_IMAGE_TYPES
    )
    
    if uploaded_file is not None:
        original_path = DATA_DIR / uploaded_file.name
        
        # Sauvegarde de l'image originale
        with open(original_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.image(str(original_path), caption="Image originale", use_container_width=True)
        
        # Option pour rogner les bordures (utile pour les captures d'écran)
        should_crop = st.checkbox(
            "Rogner les bordures (optimisation captures d'écran)",
            value=False,
            help="Cochez cette case si l'image contient des barres d'interface à supprimer"
        )
        
        if st.button("Traiter et Enregistrer"):
            with st.spinner("Traitement en cours..."):
                # Traitement de l'image (conditionnel)
                if should_crop:
                    cropped_filename = f"crop_{uploaded_file.name}"
                    image_to_process = CROPPED_DIR / cropped_filename
                    crop_ui_elements(str(original_path), str(image_to_process))
                else:
                    image_to_process = original_path
                
                # Extraction du texte par OCR
                img_to_ocr = Image.open(image_to_process)
                text = pytesseract.image_to_string(img_to_ocr, lang='fra')
                
                # Sauvegarde dans la base de données
                save_article(str(image_to_process), text, "")
                
                st.success("Article enregistré.")


def display_archives_page() -> None:
    """Affiche le fonds documentaire (archives)."""
    st.title("Fonds documentaire")
    
    # Moteur de recherche
    search_term = st.text_input("Rechercher un mot-clé dans les documents", "")
    articles = get_all_articles(search_term)
    
    if not articles:
        st.info("Aucun document à afficher.")
        return
    
    # Création d'une grille de 3 colonnes
    cols = st.columns(3)
    
    for index, article in enumerate(articles):
        article_id, filename, ocr_text, tags, created_at = article
        
        with cols[index % 3]:
            st.container(border=True)
            if os.path.exists(filename):
                st.image(filename, use_container_width=True)
                
                # Le texte OCR est masqué par défaut dans un accordéon
                with st.expander("Lire la transcription"):
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
    menu = st.sidebar.radio("Menu", ["Fonds documentaire", "Ajouter un article"])
    
    if menu == "Ajouter un article":
        display_add_article_page()
    elif menu == "Fonds documentaire":
        display_archives_page()


if __name__ == "__main__":
    main()