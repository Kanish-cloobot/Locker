"""
Database setup and initialization module.
Creates SQLite database and all required tables.
"""
import sqlite3
import os
from datetime import datetime


def get_db_path():
    """Get the path to the SQLite database file."""
    db_dir = os.path.join(os.path.dirname(__file__), '..')
    return os.path.join(db_dir, 'locker.db')


def get_connection():
    """Get a database connection."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize the database and create all tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create Locker table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Locker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            org_id INTEGER NOT NULL DEFAULT 1,
            user_id INTEGER NOT NULL DEFAULT 1,
            name TEXT NOT NULL,
            location_name TEXT NOT NULL,
            address TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    
    # Create Asset table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Asset (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            locker_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL DEFAULT 1,
            user_id INTEGER NOT NULL DEFAULT 1,
            name TEXT NOT NULL,
            asset_type TEXT NOT NULL CHECK(asset_type IN ('JEWELLERY', 'DOCUMENT', 'MISC')),
            worth_on_creation REAL,
            details TEXT,
            creation_date TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (locker_id) REFERENCES Locker(id) ON DELETE CASCADE
        )
    ''')
    
    # Create AssetDetail_Jewellery table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AssetDetail_Jewellery (
            asset_id INTEGER PRIMARY KEY,
            material_type TEXT,
            material_grade TEXT,
            gifting_details TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES Asset(id) ON DELETE CASCADE
        )
    ''')
    
    # Create AssetDetail_Document table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AssetDetail_Document (
            asset_id INTEGER PRIMARY KEY,
            document_type TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES Asset(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def get_timestamp():
    """Get current timestamp in YYYY-MM-DD HH:MM:SS format."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

