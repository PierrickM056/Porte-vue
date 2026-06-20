import sqlite3
from datetime import datetime

DB_NAME = "data/porte_vue.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
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
    conn.close()

def save_recipe(filename, ocr_text, tags):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO recipes (filename, ocr_text, tags, created_at)
        VALUES (?, ?, ?, ?)
    ''', (filename, ocr_text, tags, datetime.now()))
    conn.commit()
    conn.close()

def get_all_recipes(search_query=""):
    conn = sqlite3.connect(DB_NAME)
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
        
    rows = cursor.fetchall()
    conn.close()
    return rows