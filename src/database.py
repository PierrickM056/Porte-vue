import sqlite3
from datetime import datetime
from contextlib import contextmanager
from pathlib import Path

DB_NAME = "data/porte_vue.db"


@contextmanager
def get_db_connection():
    """Context manager pour gérer les connexions à la base de données."""
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Initialise la base de données avec la table recipes si elle n'existe pas."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                ocr_text TEXT,
                tags TEXT,
                created_at TIMESTAMP
            )
        ''')
        conn.commit()


def save_recipe(filename: str, ocr_text: str, tags: str) -> int:
    """
    Enregistre une recette dans la base de données.
    
    Args:
        filename: Chemin du fichier image
        ocr_text: Texte extrait par OCR
        tags: Tags associés à la recette
    
    Returns:
        L'ID de la recette créée
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO recipes (filename, ocr_text, tags, created_at)
            VALUES (?, ?, ?, ?)
        ''', (filename, ocr_text, tags, datetime.now()))
        conn.commit()
        return cursor.lastrowid


def get_all_recipes(search_query: str = "") -> list:
    """
    Récupère toutes les recettes, optionnellement filtrées par un terme de recherche.
    
    Args:
        search_query: Terme de recherche optionnel pour filtrer les recettes
    
    Returns:
        Liste des recettes correspondant aux critères
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        if search_query:
            cursor.execute('''
                SELECT id, filename, ocr_text, tags, created_at 
                FROM recipes 
                WHERE ocr_text LIKE ? OR tags LIKE ?
                ORDER BY created_at DESC
            ''', (f'%{search_query}%', f'%{search_query}%'))
        else:
            cursor.execute('''
                SELECT id, filename, ocr_text, tags, created_at 
                FROM recipes 
                ORDER BY created_at DESC
            ''')
            
        return cursor.fetchall()