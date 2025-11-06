"""
Asset file model for database operations.
"""
from backend.database.db_setup import get_connection, get_timestamp
import os


class AssetFileModel:
    """Model class for AssetFile table operations."""
    
    @staticmethod
    def get_by_asset_id(asset_id):
        """Get all active files for a specific asset."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM AssetFile 
            WHERE asset_id = ? AND status = 'active'
            ORDER BY created_at DESC
        ''', (asset_id,))
        files = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return files
    
    @staticmethod
    def get_thumbnail_by_asset_id(asset_id):
        """Get the first image file for an asset (for thumbnail), or PDF if no image."""
        conn = get_connection()
        cursor = conn.cursor()
        # First try to get an image
        cursor.execute('''
            SELECT * FROM AssetFile 
            WHERE asset_id = ? AND file_type = 'IMAGE' AND status = 'active'
            ORDER BY created_at ASC
            LIMIT 1
        ''', (asset_id,))
        row = cursor.fetchone()
        if row:
            conn.close()
            return dict(row)
        
        # If no image, get first PDF
        cursor.execute('''
            SELECT * FROM AssetFile 
            WHERE asset_id = ? AND file_type = 'PDF' AND status = 'active'
            ORDER BY created_at ASC
            LIMIT 1
        ''', (asset_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def get_by_id(file_id):
        """Get a file by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AssetFile WHERE id = ? AND status = 'active'", (file_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def create(asset_id, file_name, file_path, file_type, org_id=1, user_id=1):
        """Create a new file record."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            INSERT INTO AssetFile (asset_id, file_name, file_path, file_type, 
                                 org_id, user_id, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
        ''', (asset_id, file_name, file_path, file_type, org_id, user_id, timestamp, timestamp))
        file_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return file_id
    
    @staticmethod
    def delete(file_id):
        """Soft delete a file by setting status to 'deleted'."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        
        # Get file path before deleting
        cursor.execute("SELECT file_path FROM AssetFile WHERE id = ?", (file_id,))
        row = cursor.fetchone()
        file_path = dict(row)['file_path'] if row else None
        
        cursor.execute('''
            UPDATE AssetFile 
            SET status = 'deleted', updated_at = ?
            WHERE id = ? AND status = 'active'
        ''', (timestamp, file_id))
        conn.commit()
        conn.close()
        
        # Optionally delete physical file
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # Ignore file deletion errors
        
        return cursor.rowcount > 0

