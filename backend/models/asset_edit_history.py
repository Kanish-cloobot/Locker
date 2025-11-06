"""
AssetEditHistory model for database operations.
"""
import json
from backend.database.db_setup import get_connection, get_timestamp


class AssetEditHistoryModel:
    """Model class for AssetEditHistory table operations."""
    
    @staticmethod
    def create(asset_id, edited_fields, old_values, new_values, edited_by='System'):
        """Create a new edit history record."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        
        # Convert dictionaries to JSON strings
        edited_fields_json = json.dumps(edited_fields)
        old_values_json = json.dumps(old_values)
        new_values_json = json.dumps(new_values)
        
        cursor.execute('''
            INSERT INTO AssetEditHistory (asset_id, edited_fields, old_values, 
                                         new_values, edited_at, edited_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (asset_id, edited_fields_json, old_values_json, 
              new_values_json, timestamp, edited_by))
        history_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return history_id
    
    @staticmethod
    def get_by_asset_id(asset_id):
        """Get all edit history records for a specific asset."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM AssetEditHistory 
            WHERE asset_id = ?
            ORDER BY edited_at DESC
        ''', (asset_id,))
        rows = cursor.fetchall()
        
        # Parse JSON fields
        history = []
        for row in rows:
            record = dict(row)
            record['edited_fields'] = json.loads(record['edited_fields'])
            record['old_values'] = json.loads(record['old_values'])
            record['new_values'] = json.loads(record['new_values'])
            history.append(record)
        
        conn.close()
        return history

