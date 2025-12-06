import sqlite3
import os
from src.settings import BASE_DIR

DB_FOLDER = BASE_DIR / "data"
DB_NAME = str(DB_FOLDER / "listings.db")

def init_db():
    """Initialize the database and create table if not exists."""
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id TEXT PRIMARY KEY,
            title TEXT,
            price TEXT,
            sq_meters TEXT,
            location TEXT,
            link TEXT,
            date_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def listing_exists(listing_id):
    """Check if listing exists in DB."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM listings WHERE id = ?", (listing_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_listing(listing):
    """Save a new listing to DB."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO listings (id, title, price, sq_meters, location, link)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (listing['id'], listing['title'], listing['price'], listing.get('sq_meters', 'N/A'), listing.get('location', 'N/A'), listing['link']))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Already exists
    finally:
        conn.close()
