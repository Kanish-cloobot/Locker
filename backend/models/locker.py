"""
Locker model for database operations.
"""
from backend.database.db_setup import get_connection, get_timestamp


class LockerModel:
    """Model class for Locker table operations."""
    
    @staticmethod
    def get_all():
        """Get all lockers."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Locker ORDER BY created_at DESC')
        lockers = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return lockers
    
    @staticmethod
    def get_by_id(locker_id):
        """Get a locker by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Locker WHERE id = ?', (locker_id,))
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
            INSERT INTO Locker (org_id, user_id, name, location_name, address, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
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
            WHERE id = ?
        ''', (name, location_name, address, timestamp, locker_id))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @staticmethod
    def delete(locker_id):
        """Delete a locker (cascade will delete associated assets)."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Locker WHERE id = ?', (locker_id,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0

