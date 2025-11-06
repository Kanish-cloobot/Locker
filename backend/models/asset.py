"""
Asset model for database operations.
"""
from backend.database.db_setup import get_connection, get_timestamp


class AssetModel:
    """Model class for Asset table operations."""
    
    @staticmethod
    def get_by_locker_id(locker_id):
        """Get all assets for a specific locker."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Asset 
            WHERE locker_id = ? 
            ORDER BY created_at DESC
        ''', (locker_id,))
        assets = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return assets
    
    @staticmethod
    def get_by_id(asset_id):
        """Get an asset by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Asset WHERE id = ?', (asset_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def create(locker_id, name, asset_type, worth_on_creation=None, details=None, 
               creation_date=None, org_id=1, user_id=1):
        """Create a new asset."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            INSERT INTO Asset (locker_id, org_id, user_id, name, asset_type, 
                             worth_on_creation, details, creation_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (locker_id, org_id, user_id, name, asset_type, worth_on_creation, 
              details, creation_date, timestamp, timestamp))
        asset_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return asset_id
    
    @staticmethod
    def update(asset_id, name, asset_type, worth_on_creation=None, details=None, creation_date=None):
        """Update an existing asset."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            UPDATE Asset 
            SET name = ?, asset_type = ?, worth_on_creation = ?, 
                details = ?, creation_date = ?, updated_at = ?
            WHERE id = ?
        ''', (name, asset_type, worth_on_creation, details, creation_date, timestamp, asset_id))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @staticmethod
    def delete(asset_id):
        """Delete an asset (cascade will delete associated detail records)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Asset WHERE id = ?', (asset_id,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0

