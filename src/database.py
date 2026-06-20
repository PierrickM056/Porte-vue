"""
Module de gestion de la base de données pour Porte-vue.

Gère le stockage et la récupération des articles archivés.
"""

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
    """Initialise la base de données avec la table articles si elle n'existe pas."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                ocr_text TEXT,
                tags TEXT,
                created_at TIMESTAMP
            )
        ''')
        conn.commit()


def save_article(filename: str, ocr_text: str, tags: str) -> int:
    """
    Enregistre un article dans la base de données.
    
    Args:
        filename: Chemin du fichier image
        ocr_text: Texte extrait par OCR
        tags: Tags associés à l'article
    
    Returns:
        L'ID de l'article créé
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO articles (filename, ocr_text, tags, created_at)
            VALUES (?, ?, ?, ?)
        ''', (filename, ocr_text, tags, datetime.now()))
        conn.commit()
        return cursor.lastrowid


def get_all_articles(search_query: str = "") -> list:
    """
    Récupère tous les articles, optionnellement filtrés par un terme de recherche.
    
    Args:
        search_query: Terme de recherche optionnel pour filtrer les articles
    
    Returns:
        Liste des articles correspondant aux critères
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        if search_query:
            cursor.execute('''
                SELECT id, filename, ocr_text, tags, created_at 
                FROM articles 
                WHERE ocr_text LIKE ? OR tags LIKE ?
                ORDER BY created_at DESC
            ''', (f'%{search_query}%', f'%{search_query}%'))
        else:
            cursor.execute('''
                SELECT id, filename, ocr_text, tags, created_at 
                FROM articles 
                ORDER BY created_at DESC
            ''')
            
        return cursor.fetchall()