"""
Asset service/presenter for business logic.
"""
import json
from backend.models.asset import AssetModel
from backend.models.asset_detail import AssetDetailJewelleryModel, AssetDetailDocumentModel
from backend.models.transaction import TransactionModel
from backend.models.asset_file import AssetFileModel
from backend.models.asset_edit_history import AssetEditHistoryModel
from backend.database.db_setup import get_timestamp


class AssetService:
    """Service class for asset business logic."""
    
    @staticmethod
    def get_assets_by_locker(locker_id):
        """Get all assets for a locker with their detail information."""
        assets = AssetModel.get_by_locker_id(locker_id)
        
        for asset in assets:
            asset_id = asset['id']
            asset_type = asset['asset_type']
            
            if asset_type == 'JEWELLERY':
                detail = AssetDetailJewelleryModel.get_by_asset_id(asset_id)
                if detail:
                    asset['jewellery_details'] = {
                        'material_type': detail.get('material_type'),
                        'material_grade': detail.get('material_grade'),
                        'gifting_details': detail.get('gifting_details')
                    }
            elif asset_type == 'DOCUMENT':
                detail = AssetDetailDocumentModel.get_by_asset_id(asset_id)
                if detail:
                    asset['document_details'] = {
                        'document_type': detail.get('document_type')
                    }
        
        return assets
    
    @staticmethod
    def get_asset_by_id(asset_id):
        """Get an asset by ID with its detail information."""
        asset = AssetModel.get_by_id(asset_id)
        if not asset:
            return None
        
        asset_type = asset['asset_type']
        
        if asset_type == 'JEWELLERY':
            detail = AssetDetailJewelleryModel.get_by_asset_id(asset_id)
            if detail:
                asset['jewellery_details'] = {
                    'material_type': detail.get('material_type'),
                    'material_grade': detail.get('material_grade'),
                    'gifting_details': detail.get('gifting_details')
                }
        elif asset_type == 'DOCUMENT':
            detail = AssetDetailDocumentModel.get_by_asset_id(asset_id)
            if detail:
                asset['document_details'] = {
                    'document_type': detail.get('document_type')
                }
        
        return asset
    
    @staticmethod
    def create_asset(locker_id, data):
        """Create a new asset with appropriate detail record and initial transaction."""
        name = data.get('name')
        asset_type = data.get('asset_type')
        
        if not name or not asset_type:
            raise ValueError("Name and asset_type are required")
        
        if asset_type not in ['JEWELLERY', 'DOCUMENT', 'MISC']:
            raise ValueError("asset_type must be JEWELLERY, DOCUMENT, or MISC")
        
        # Create the asset
        asset_id = AssetModel.create(
            locker_id=locker_id,
            name=name,
            asset_type=asset_type,
            worth_on_creation=data.get('worth_on_creation'),
            details=data.get('details'),
            creation_date=data.get('creation_date'),
            current_status='IN_LOCKER'
        )
        
        # Create detail record based on asset type
        if asset_type == 'JEWELLERY':
            AssetDetailJewelleryModel.create(
                asset_id=asset_id,
                material_type=data.get('material_type'),
                material_grade=data.get('material_grade'),
                gifting_details=data.get('gifting_details')
            )
        elif asset_type == 'DOCUMENT':
            AssetDetailDocumentModel.create(
                asset_id=asset_id,
                document_type=data.get('document_type')
            )
        
        # Auto-create initial DEPOSIT transaction
        TransactionModel.create(
            asset_id=asset_id,
            locker_id=locker_id,
            transaction_type='DEPOSIT',
            reason='Initial deposit',
            responsible_person=data.get('responsible_person', 'System')
        )
        
        return AssetService.get_asset_by_id(asset_id)
    
    @staticmethod
    def update_asset(asset_id, data):
        """Update an asset and its detail record, tracking edit history."""
        asset = AssetModel.get_by_id(asset_id)
        if not asset:
            raise ValueError("Asset not found")
        
        current_type = asset['asset_type']
        new_type = data.get('asset_type', current_type)
        
        # Track changes for edit history
        edited_fields = []
        old_values = {}
        new_values = {}
        
        # Check each field for changes
        fields_to_check = ['name', 'asset_type', 'worth_on_creation', 'details', 'creation_date']
        for field in fields_to_check:
            old_val = asset.get(field)
            new_val = data.get(field, old_val)
            
            # Handle None comparisons
            if old_val != new_val and (old_val is not None or new_val is not None):
                edited_fields.append(field)
                old_values[field] = old_val
                new_values[field] = new_val
        
        # Update the asset
        AssetModel.update(
            asset_id=asset_id,
            name=data.get('name', asset['name']),
            asset_type=new_type,
            worth_on_creation=data.get('worth_on_creation', asset.get('worth_on_creation')),
            details=data.get('details', asset.get('details')),
            creation_date=data.get('creation_date', asset.get('creation_date'))
        )
        
        # Handle detail records - if type changed, delete old and create new
        if current_type != new_type:
            if current_type == 'JEWELLERY':
                AssetDetailJewelleryModel.delete(asset_id)
            elif current_type == 'DOCUMENT':
                AssetDetailDocumentModel.delete(asset_id)
        
        # Create or update detail record based on new type
        if new_type == 'JEWELLERY':
            existing = AssetDetailJewelleryModel.get_by_asset_id(asset_id)
            old_detail = existing if existing else {}
            new_detail = {
                'material_type': data.get('material_type'),
                'material_grade': data.get('material_grade'),
                'gifting_details': data.get('gifting_details')
            }
            
            # Track detail field changes
            detail_fields = ['material_type', 'material_grade', 'gifting_details']
            for field in detail_fields:
                old_val = old_detail.get(field)
                new_val = new_detail.get(field)
                if old_val != new_val and (old_val is not None or new_val is not None):
                    edited_fields.append(f'jewellery_{field}')
                    old_values[f'jewellery_{field}'] = old_val
                    new_values[f'jewellery_{field}'] = new_val
            
            if existing:
                AssetDetailJewelleryModel.update(
                    asset_id=asset_id,
                    material_type=data.get('material_type'),
                    material_grade=data.get('material_grade'),
                    gifting_details=data.get('gifting_details')
                )
            else:
                AssetDetailJewelleryModel.create(
                    asset_id=asset_id,
                    material_type=data.get('material_type'),
                    material_grade=data.get('material_grade'),
                    gifting_details=data.get('gifting_details')
                )
        elif new_type == 'DOCUMENT':
            existing = AssetDetailDocumentModel.get_by_asset_id(asset_id)
            old_detail = existing if existing else {}
            new_detail = {'document_type': data.get('document_type')}
            
            # Track detail field changes
            if old_detail.get('document_type') != new_detail.get('document_type'):
                edited_fields.append('document_type')
                old_values['document_type'] = old_detail.get('document_type')
                new_values['document_type'] = new_detail.get('document_type')
            
            if existing:
                AssetDetailDocumentModel.update(
                    asset_id=asset_id,
                    document_type=data.get('document_type')
                )
            else:
                AssetDetailDocumentModel.create(
                    asset_id=asset_id,
                    document_type=data.get('document_type')
                )
        
        # Create edit history record if any fields were changed
        if edited_fields:
            AssetEditHistoryModel.create(
                asset_id=asset_id,
                edited_fields=edited_fields,
                old_values=old_values,
                new_values=new_values,
                edited_by=data.get('edited_by', 'System')
            )
        
        return AssetService.get_asset_by_id(asset_id)
    
    @staticmethod
    def delete_asset(asset_id):
        """Delete an asset (cascade will delete detail records)."""
        asset = AssetModel.get_by_id(asset_id)
        if not asset:
            raise ValueError("Asset not found")
        
        return AssetModel.delete(asset_id)
    
    @staticmethod
    def get_asset_with_files(asset_id):
        """Get an asset with its files."""
        asset = AssetService.get_asset_by_id(asset_id)
        if not asset:
            return None
        
        files = AssetFileModel.get_by_asset_id(asset_id)
        asset['files'] = files
        return asset
    
    @staticmethod
    def get_asset_edit_history(asset_id):
        """Get edit history for an asset."""
        return AssetEditHistoryModel.get_by_asset_id(asset_id)

