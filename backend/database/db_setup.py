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
    
    # Add current_status column to Asset table (migration)
    try:
        cursor.execute("ALTER TABLE Asset ADD COLUMN current_status TEXT DEFAULT 'IN_LOCKER'")
        cursor.execute("UPDATE Asset SET current_status = 'IN_LOCKER' WHERE current_status IS NULL")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Create Transaction table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Transaction" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER NOT NULL,
            locker_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('DEPOSIT', 'WITHDRAW', 'PERMANENTLY_REMOVE')),
            reason TEXT,
            responsible_person TEXT,
            transaction_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'deleted')),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES Asset(id),
            FOREIGN KEY (locker_id) REFERENCES Locker(id)
        )
    ''')
    
    # Add missing columns to Transaction table if they don't exist (migrations)
    # Add locker_id column
    try:
        cursor.execute("ALTER TABLE \"Transaction\" ADD COLUMN locker_id INTEGER")
        # Populate locker_id from Asset table for existing transactions
        cursor.execute('''
            UPDATE "Transaction" 
            SET locker_id = (
                SELECT locker_id 
                FROM Asset 
                WHERE Asset.id = "Transaction".asset_id
            )
            WHERE locker_id IS NULL
        ''')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add transaction_date column
    try:
        cursor.execute("ALTER TABLE \"Transaction\" ADD COLUMN transaction_date TEXT")
        # Populate transaction_date from created_at for existing transactions, or use current timestamp
        timestamp = get_timestamp()
        cursor.execute('''
            UPDATE "Transaction" 
            SET transaction_date = COALESCE(created_at, ?)
            WHERE transaction_date IS NULL
        ''', (timestamp,))
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add status column
    try:
        cursor.execute("ALTER TABLE \"Transaction\" ADD COLUMN status TEXT DEFAULT 'active'")
        cursor.execute("UPDATE \"Transaction\" SET status = 'active' WHERE status IS NULL")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add created_at column
    try:
        cursor.execute("ALTER TABLE \"Transaction\" ADD COLUMN created_at TEXT")
        timestamp = get_timestamp()
        cursor.execute("UPDATE \"Transaction\" SET created_at = ? WHERE created_at IS NULL", (timestamp,))
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add updated_at column
    try:
        cursor.execute("ALTER TABLE \"Transaction\" ADD COLUMN updated_at TEXT")
        timestamp = get_timestamp()
        cursor.execute("UPDATE \"Transaction\" SET updated_at = ? WHERE updated_at IS NULL", (timestamp,))
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add reason column (if missing)
    try:
        cursor.execute("ALTER TABLE \"Transaction\" ADD COLUMN reason TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add responsible_person column (if missing)
    try:
        cursor.execute("ALTER TABLE \"Transaction\" ADD COLUMN responsible_person TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Create AssetFile table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AssetFile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER NOT NULL,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_type TEXT NOT NULL CHECK(file_type IN ('IMAGE', 'PDF')),
            file_size INTEGER,
            status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'deleted')),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (asset_id) REFERENCES Asset(id)
        )
    ''')
    
    # Add file_size column to AssetFile table if it doesn't exist (migration)
    try:
        cursor.execute("ALTER TABLE AssetFile ADD COLUMN file_size INTEGER")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Add updated_at column to AssetFile table if it doesn't exist (migration)
    try:
        cursor.execute("ALTER TABLE AssetFile ADD COLUMN updated_at TEXT")
        timestamp = get_timestamp()
        cursor.execute("UPDATE AssetFile SET updated_at = ? WHERE updated_at IS NULL", (timestamp,))
        # Set NOT NULL constraint by recreating the table (SQLite doesn't support ALTER COLUMN)
        # But we'll handle this in the model instead
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Create AssetEditHistory table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AssetEditHistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER NOT NULL,
            edited_fields TEXT NOT NULL,
            old_values TEXT NOT NULL,
            new_values TEXT NOT NULL,
            edited_at TEXT NOT NULL,
            edited_by TEXT DEFAULT 'System',
            FOREIGN KEY (asset_id) REFERENCES Asset(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


def get_timestamp():
    """Get current timestamp in YYYY-MM-DD HH:MM:SS format."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

