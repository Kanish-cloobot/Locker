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
            status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'deleted')),
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
            status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'deleted')),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (locker_id) REFERENCES Locker(id)
        )
    ''')
    
    # Create AssetDetail_Jewellery table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AssetDetail_Jewellery (
            asset_id INTEGER PRIMARY KEY,
            material_type TEXT,
            material_grade TEXT,
            gifting_details TEXT,
            status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'deleted')),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES Asset(id)
        )
    ''')
    
    # Create AssetDetail_Document table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AssetDetail_Document (
            asset_id INTEGER PRIMARY KEY,
            document_type TEXT,
            status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'deleted')),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES Asset(id)
        )
    ''')
    
    # Add status column to existing tables if they don't have it (migration)
    try:
        cursor.execute("ALTER TABLE Locker ADD COLUMN status TEXT DEFAULT 'active'")
        cursor.execute("UPDATE Locker SET status = 'active' WHERE status IS NULL")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE Asset ADD COLUMN status TEXT DEFAULT 'active'")
        cursor.execute("UPDATE Asset SET status = 'active' WHERE status IS NULL")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE AssetDetail_Jewellery ADD COLUMN status TEXT DEFAULT 'active'")
        cursor.execute("UPDATE AssetDetail_Jewellery SET status = 'active' WHERE status IS NULL")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE AssetDetail_Document ADD COLUMN status TEXT DEFAULT 'active'")
        cursor.execute("UPDATE AssetDetail_Document SET status = 'active' WHERE status IS NULL")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def get_timestamp():
    """Get current timestamp in YYYY-MM-DD HH:MM:SS format."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

