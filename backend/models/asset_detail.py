"""
Asset detail models for database operations.
Handles AssetDetail_Jewellery and AssetDetail_Document tables.
"""
from backend.database.db_setup import get_connection, get_timestamp


class AssetDetailJewelleryModel:
    """Model class for AssetDetail_Jewellery table operations."""
    
    @staticmethod
    def get_by_asset_id(asset_id):
        """Get active jewellery details for an asset."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AssetDetail_Jewellery WHERE asset_id = ? AND status = 'active'", (asset_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def create(asset_id, material_type=None, material_grade=None, gifting_details=None):
        """Create jewellery details for an asset."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            INSERT INTO AssetDetail_Jewellery (asset_id, material_type, material_grade, 
                                              gifting_details, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, 'active', ?, ?)
        ''', (asset_id, material_type, material_grade, gifting_details, timestamp, timestamp))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update(asset_id, material_type=None, material_grade=None, gifting_details=None):
        """Update jewellery details for an asset."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            UPDATE AssetDetail_Jewellery 
            SET material_type = ?, material_grade = ?, gifting_details = ?, updated_at = ?
            WHERE asset_id = ? AND status = 'active'
        ''', (material_type, material_grade, gifting_details, timestamp, asset_id))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @staticmethod
    def delete(asset_id):
        """Soft delete jewellery details for an asset."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            UPDATE AssetDetail_Jewellery 
            SET status = 'deleted', updated_at = ?
            WHERE asset_id = ?
        ''', (timestamp, asset_id))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0


class AssetDetailDocumentModel:
    """Model class for AssetDetail_Document table operations."""
    
    @staticmethod
    def get_by_asset_id(asset_id):
        """Get active document details for an asset."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AssetDetail_Document WHERE asset_id = ? AND status = 'active'", (asset_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def create(asset_id, document_type=None):
        """Create document details for an asset."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            INSERT INTO AssetDetail_Document (asset_id, document_type, status, created_at, updated_at)
            VALUES (?, ?, 'active', ?, ?)
        ''', (asset_id, document_type, timestamp, timestamp))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update(asset_id, document_type=None):
        """Update document details for an asset."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            UPDATE AssetDetail_Document 
            SET document_type = ?, updated_at = ?
            WHERE asset_id = ? AND status = 'active'
        ''', (document_type, timestamp, asset_id))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @staticmethod
    def delete(asset_id):
        """Soft delete document details for an asset."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            UPDATE AssetDetail_Document 
            SET status = 'deleted', updated_at = ?
            WHERE asset_id = ?
        ''', (timestamp, asset_id))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0

