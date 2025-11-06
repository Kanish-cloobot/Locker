"""
Locker file storage model for database operations.
Comprehensive file storage with proper mapping and metadata.
"""
from backend.database.db_setup import get_connection, get_timestamp
import os


class LockerFileStorageModel:
    """Model class for LockerFileStorage table operations."""
    
    @staticmethod
    def get_by_asset_id(asset_id):
        """Get all active files for a specific asset."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM LockerFileStorage 
            WHERE asset_id = ? AND status = 'active'
            ORDER BY created_at DESC
        ''', (asset_id,))
        files = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return files
    
    @staticmethod
    def get_images_by_asset_id(asset_id):
        """Get all image files for a specific asset."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM LockerFileStorage 
            WHERE asset_id = ? AND file_type = 'IMAGE' AND status = 'active'
            ORDER BY is_thumbnail DESC, created_at ASC
        ''', (asset_id,))
        files = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return files
    
    @staticmethod
    def get_thumbnail_by_asset_id(asset_id):
        """Get the thumbnail image for an asset, or first file (image or PDF) if no image thumbnail."""
        conn = get_connection()
        cursor = conn.cursor()
        # First try to get a marked thumbnail image
        cursor.execute('''
            SELECT * FROM LockerFileStorage 
            WHERE asset_id = ? AND file_type = 'IMAGE' AND is_thumbnail = 1 AND status = 'active'
            ORDER BY created_at ASC
            LIMIT 1
        ''', (asset_id,))
        row = cursor.fetchone()
        if row:
            conn.close()
            return dict(row)
        
        # If no thumbnail marked, get first image
        cursor.execute('''
            SELECT * FROM LockerFileStorage 
            WHERE asset_id = ? AND file_type = 'IMAGE' AND status = 'active'
            ORDER BY created_at ASC
            LIMIT 1
        ''', (asset_id,))
        row = cursor.fetchone()
        if row:
            conn.close()
            return dict(row)
        
        # If no image, get first PDF file
        cursor.execute('''
            SELECT * FROM LockerFileStorage 
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
        cursor.execute("SELECT * FROM LockerFileStorage WHERE id = ? AND status = 'active'", (file_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def create(asset_id, original_file_name, stored_file_name, file_path, file_type, 
               file_size=None, mime_type=None, thumbnail_path=None, is_thumbnail=False, 
               org_id=1, user_id=1):
        """Create a new file record."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            INSERT INTO LockerFileStorage (asset_id, original_file_name, stored_file_name, file_path, 
                                         file_type, file_size, mime_type, thumbnail_path, is_thumbnail,
                                         org_id, user_id, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', ?, ?)
        ''', (asset_id, original_file_name, stored_file_name, file_path, file_type, 
              file_size, mime_type, thumbnail_path, 1 if is_thumbnail else 0,
              org_id, user_id, timestamp, timestamp))
        file_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return file_id
    
    @staticmethod
    def set_as_thumbnail(file_id):
        """Set a file as the thumbnail for its asset."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        
        # Get asset_id first
        cursor.execute("SELECT asset_id FROM LockerFileStorage WHERE id = ?", (file_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False
        
        asset_id = dict(row)['asset_id']
        
        # Unset other thumbnails for this asset
        cursor.execute('''
            UPDATE LockerFileStorage 
            SET is_thumbnail = 0, updated_at = ?
            WHERE asset_id = ? AND is_thumbnail = 1 AND status = 'active'
        ''', (timestamp, asset_id))
        
        # Set this file as thumbnail
        cursor.execute('''
            UPDATE LockerFileStorage 
            SET is_thumbnail = 1, updated_at = ?
            WHERE id = ? AND status = 'active'
        ''', (timestamp, file_id))
        
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @staticmethod
    def delete(file_id):
        """Soft delete a file by setting status to 'deleted'."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        
        # Get file path before deleting
        cursor.execute("SELECT file_path FROM LockerFileStorage WHERE id = ?", (file_id,))
        row = cursor.fetchone()
        file_path = dict(row)['file_path'] if row else None
        
        cursor.execute('''
            UPDATE LockerFileStorage 
            SET status = 'deleted', updated_at = ?
            WHERE id = ? AND status = 'active'
        ''', (timestamp, file_id))
        conn.commit()
        conn.close()
        
        # Optionally delete physical file
        if file_path:
            try:
                absolute_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), file_path)
                if os.path.exists(absolute_path):
                    os.remove(absolute_path)
            except Exception:
                pass  # Ignore file deletion errors
        
        return cursor.rowcount > 0

