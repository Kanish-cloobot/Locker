"""
Locker model for database operations.
"""
from backend.database.db_setup import get_connection, get_timestamp


class LockerModel:
    """Model class for Locker table operations."""
    
    @staticmethod
    def get_all():
        """Get all active lockers."""
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Locker WHERE status = 'active' ORDER BY created_at DESC")
            lockers = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return lockers
        except Exception as e:
            if conn:
                conn.close()
            raise Exception(f"Database error while fetching lockers: {str(e)}")
    
    @staticmethod
    def get_by_id(locker_id):
        """Get an active locker by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Locker WHERE id = ? AND status = 'active'", (locker_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def create(name, location_name, address, org_id=1, user_id=1):
        """Create a new locker."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            INSERT INTO Locker (org_id, user_id, name, location_name, address, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
        ''', (org_id, user_id, name, location_name, address, timestamp, timestamp))
        locker_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return locker_id
    
    @staticmethod
    def update(locker_id, name, location_name, address):
        """Update an existing locker."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            UPDATE Locker 
            SET name = ?, location_name = ?, address = ?, updated_at = ?
            WHERE id = ? AND status = 'active'
        ''', (name, location_name, address, timestamp, locker_id))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @staticmethod
    def delete(locker_id):
        """Soft delete a locker by setting status to 'deleted'."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        # Check if locker exists and is active
        cursor.execute("SELECT id FROM Locker WHERE id = ? AND status = 'active'", (locker_id,))
        if not cursor.fetchone():
            conn.close()
            return False
        # Soft delete the locker
        cursor.execute('''
            UPDATE Locker 
            SET status = 'deleted', updated_at = ?
            WHERE id = ? AND status = 'active'
        ''', (timestamp, locker_id))
        # Also soft delete all associated active assets
        cursor.execute('''
            UPDATE Asset 
            SET status = 'deleted', updated_at = ?
            WHERE locker_id = ? AND status = 'active'
        ''', (timestamp, locker_id))
        # Soft delete asset details for assets in this locker
        cursor.execute('''
            UPDATE AssetDetail_Jewellery 
            SET status = 'deleted', updated_at = ?
            WHERE asset_id IN (SELECT id FROM Asset WHERE locker_id = ?) AND status = 'active'
        ''', (timestamp, locker_id))
        cursor.execute('''
            UPDATE AssetDetail_Document 
            SET status = 'deleted', updated_at = ?
            WHERE asset_id IN (SELECT id FROM Asset WHERE locker_id = ?) AND status = 'active'
        ''', (timestamp, locker_id))
        conn.commit()
        conn.close()
        return True

