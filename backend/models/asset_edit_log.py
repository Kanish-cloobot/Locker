"""
Asset edit log model for database operations.
"""
from backend.database.db_setup import get_connection, get_timestamp


class AssetEditLogModel:
    """Model class for AssetEditLog table operations."""
    
    @staticmethod
    def get_by_asset_id(asset_id):
        """Get all edit logs for a specific asset ordered by created_at DESC."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM AssetEditLog 
            WHERE asset_id = ?
            ORDER BY created_at DESC
        ''', (asset_id,))
        logs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return logs
    
    @staticmethod
    def create(asset_id, field_name, old_value=None, new_value=None, org_id=1, user_id=1):
        """Create a new edit log entry."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            INSERT INTO AssetEditLog (asset_id, field_name, old_value, new_value, 
                                    org_id, user_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (asset_id, field_name, old_value, new_value, org_id, user_id, timestamp))
        conn.commit()
        conn.close()
    
    @staticmethod
    def log_asset_update(asset_id, old_asset, new_data):
        """Log all changed fields when an asset is updated."""
        fields_to_check = ['name', 'asset_type', 'worth_on_creation', 'details', 'creation_date']
        
        for field in fields_to_check:
            old_val = old_asset.get(field)
            new_val = new_data.get(field)
            
            # Handle None vs empty string
            if old_val is None:
                old_val = None
            if new_val is None or new_val == '':
                new_val = None
            
            # Only log if value actually changed
            if str(old_val) != str(new_val):
                AssetEditLogModel.create(
                    asset_id=asset_id,
                    field_name=field,
                    old_value=str(old_val) if old_val is not None else None,
                    new_value=str(new_val) if new_val is not None else None
                )
        
        # Check detail fields based on asset type
        asset_type = new_data.get('asset_type', old_asset.get('asset_type'))
        
        if asset_type == 'JEWELLERY':
            detail_fields = ['material_type', 'material_grade', 'gifting_details']
            old_details = old_asset.get('jewellery_details', {})
            if not isinstance(old_details, dict):
                old_details = {}
            
            for field in detail_fields:
                old_val = old_details.get(field)
                new_val = new_data.get(field)
                
                if str(old_val) != str(new_val):
                    AssetEditLogModel.create(
                        asset_id=asset_id,
                        field_name=f'jewellery_{field}',
                        old_value=str(old_val) if old_val is not None else None,
                        new_value=str(new_val) if new_val is not None else None
                    )
        elif asset_type == 'DOCUMENT':
            old_val = old_asset.get('document_details', {}).get('document_type') if isinstance(old_asset.get('document_details'), dict) else None
            new_val = new_data.get('document_type')
            
            if str(old_val) != str(new_val):
                AssetEditLogModel.create(
                    asset_id=asset_id,
                    field_name='document_type',
                    old_value=str(old_val) if old_val is not None else None,
                    new_value=str(new_val) if new_val is not None else None
                )

