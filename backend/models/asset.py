"""
Asset model for database operations.
"""
from backend.database.db_setup import get_connection, get_timestamp


class AssetModel:
    """Model class for Asset table operations."""
    
    @staticmethod
    def get_by_locker_id(locker_id):
        """Get all active assets for a specific locker."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Asset 
            WHERE locker_id = ? AND status = 'active'
            ORDER BY created_at DESC
        ''', (locker_id,))
        assets = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return assets
    
    @staticmethod
    def get_by_id(asset_id):
        """Get an active asset by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Asset WHERE id = ? AND status = 'active'", (asset_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def create(locker_id, name, asset_type, worth_on_creation=None, details=None, 
               creation_date=None, org_id=1, user_id=1, current_status='IN_LOCKER'):
        """Create a new asset."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            INSERT INTO Asset (locker_id, org_id, user_id, name, asset_type, 
                             worth_on_creation, details, creation_date, current_status, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', ?, ?)
        ''', (locker_id, org_id, user_id, name, asset_type, worth_on_creation, 
              details, creation_date, current_status, timestamp, timestamp))
        asset_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return asset_id
    
    @staticmethod
    def update(asset_id, name, asset_type, worth_on_creation=None, details=None, 
               creation_date=None, current_status=None):
        """Update an existing asset."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        
        # Build dynamic update query
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if asset_type is not None:
            updates.append("asset_type = ?")
            params.append(asset_type)
        if worth_on_creation is not None:
            updates.append("worth_on_creation = ?")
            params.append(worth_on_creation)
        if details is not None:
            updates.append("details = ?")
            params.append(details)
        if creation_date is not None:
            updates.append("creation_date = ?")
            params.append(creation_date)
        if current_status is not None:
            updates.append("current_status = ?")
            params.append(current_status)
        
        if not updates:
            conn.close()
            return False
        
        updates.append("updated_at = ?")
        params.append(timestamp)
        params.append(asset_id)
        
        query = f"UPDATE Asset SET {', '.join(updates)} WHERE id = ? AND status = 'active'"
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @staticmethod
    def get_current_status(asset_id):
        """Get current status of an asset."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT current_status FROM Asset 
            WHERE id = ? AND status = 'active'
        ''', (asset_id,))
        row = cursor.fetchone()
        conn.close()
        return row['current_status'] if row else None
    
    @staticmethod
    def delete(asset_id):
        """Soft delete an asset by setting status to 'deleted'."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        # Check if asset exists and is active
        cursor.execute("SELECT id FROM Asset WHERE id = ? AND status = 'active'", (asset_id,))
        if not cursor.fetchone():
            conn.close()
            return False
        # Soft delete the asset
        cursor.execute('''
            UPDATE Asset 
            SET status = 'deleted', updated_at = ?
            WHERE id = ? AND status = 'active'
        ''', (timestamp, asset_id))
        # Soft delete associated detail records
        cursor.execute('''
            UPDATE AssetDetail_Jewellery 
            SET status = 'deleted', updated_at = ?
            WHERE asset_id = ? AND status = 'active'
        ''', (timestamp, asset_id))
        cursor.execute('''
            UPDATE AssetDetail_Document 
            SET status = 'deleted', updated_at = ?
            WHERE asset_id = ? AND status = 'active'
        ''', (timestamp, asset_id))
        conn.commit()
        conn.close()
        return True

