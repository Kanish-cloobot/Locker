"""
AssetFile model for database operations.
"""
from backend.database.db_setup import get_connection, get_timestamp


class AssetFileModel:
    """Model class for AssetFile table operations."""
    
    @staticmethod
    def create(asset_id, file_name, file_path, file_type, file_size=None):
        """Create a new asset file record."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        # Check if updated_at column exists (for backward compatibility with existing databases)
        cursor.execute("PRAGMA table_info(AssetFile)")
        columns = [col[1] for col in cursor.fetchall()]
        has_updated_at = 'updated_at' in columns
        
        if has_updated_at:
            cursor.execute('''
                INSERT INTO AssetFile (asset_id, file_name, file_path, file_type, 
                                     file_size, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
            ''', (asset_id, file_name, file_path, file_type, file_size, timestamp, timestamp))
        else:
            # Fallback for databases that don't have updated_at yet
            cursor.execute('''
                INSERT INTO AssetFile (asset_id, file_name, file_path, file_type, 
                                     file_size, status, created_at)
                VALUES (?, ?, ?, ?, ?, 'active', ?)
            ''', (asset_id, file_name, file_path, file_type, file_size, timestamp))
        file_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return file_id
    
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
    def get_by_id(file_id):
        """Get a file by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM AssetFile 
            WHERE id = ? AND status = 'active'
        ''', (file_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def delete(file_id):
        """Soft delete a file."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            UPDATE AssetFile 
            SET status = 'deleted', created_at = ?
            WHERE id = ? AND status = 'active'
        ''', (timestamp, file_id))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @staticmethod
    def get_file_path(file_id):
        """Get file path by file ID."""
        file_record = AssetFileModel.get_by_id(file_id)
        return file_record['file_path'] if file_record else None

