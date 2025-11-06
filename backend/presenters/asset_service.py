"""
Asset service/presenter for business logic.
"""
from backend.models.asset import AssetModel
from backend.models.asset_detail import AssetDetailJewelleryModel, AssetDetailDocumentModel
from backend.models.transaction import TransactionModel
from backend.models.asset_edit_log import AssetEditLogModel
from backend.models.asset_file import AssetFileModel
from backend.models.locker_file_storage import LockerFileStorageModel


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
            
            # Get thumbnail file from LockerFileStorage first
            thumbnail = LockerFileStorageModel.get_thumbnail_by_asset_id(asset_id)
            if thumbnail:
                asset['thumbnail'] = thumbnail
            else:
                # Fallback to AssetFile for backward compatibility
                thumbnail = AssetFileModel.get_thumbnail_by_asset_id(asset_id)
                if thumbnail:
                    # Convert AssetFile format to match expected format
                    asset['thumbnail'] = {
                        'id': thumbnail['id'],
                        'file_path': thumbnail['file_path'],
                        'file_name': thumbnail['file_name'],
                        'file_type': thumbnail['file_type'],
                        'thumbnail_path': None  # Old files don't have thumbnails
                    }
            
            # Get edit logs for each asset
            edit_logs = AssetEditLogModel.get_by_asset_id(asset_id)
            asset['edit_logs'] = edit_logs
        
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
        
        # Get files from LockerFileStorage
        files = LockerFileStorageModel.get_by_asset_id(asset_id)
        if not files:
            # Fallback to AssetFile
            files = AssetFileModel.get_by_asset_id(asset_id)
        asset['files'] = files
        
        # Get thumbnail
        thumbnail = LockerFileStorageModel.get_thumbnail_by_asset_id(asset_id)
        if thumbnail:
            asset['thumbnail'] = thumbnail
        else:
            # Fallback to AssetFile for backward compatibility
            thumbnail = AssetFileModel.get_thumbnail_by_asset_id(asset_id)
            if thumbnail:
                # Convert AssetFile format to match expected format
                asset['thumbnail'] = {
                    'id': thumbnail['id'],
                    'file_path': thumbnail['file_path'],
                    'file_name': thumbnail['file_name'],
                    'file_type': thumbnail['file_type'],
                    'thumbnail_path': None  # Old files don't have thumbnails
                }
        
        # Get edit logs
        edit_logs = AssetEditLogModel.get_by_asset_id(asset_id)
        asset['edit_logs'] = edit_logs
        
        return asset
    
    @staticmethod
    def create_asset(locker_id, data):
        """Create a new asset with appropriate detail record."""
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
            creation_date=data.get('creation_date')
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
        
        # Create initial DEPOSIT transaction
        TransactionModel.create(
            asset_id=asset_id,
            transaction_type='DEPOSIT',
            reason='Initial deposit upon asset creation',
            responsible_person=data.get('responsible_person')
        )
        
        return AssetService.get_asset_by_id(asset_id)
    
    @staticmethod
    def update_asset(asset_id, data):
        """Update an asset and its detail record."""
        asset = AssetModel.get_by_id(asset_id)
        if not asset:
            raise ValueError("Asset not found")
        
        # Store old asset data for edit logging
        old_asset = AssetService.get_asset_by_id(asset_id)
        
        current_type = asset['asset_type']
        new_type = data.get('asset_type', current_type)
        
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
        
        # Log all field changes
        updated_asset = AssetService.get_asset_by_id(asset_id)
        AssetEditLogModel.log_asset_update(asset_id, old_asset, data)
        
        return updated_asset
    
    @staticmethod
    def delete_asset(asset_id):
        """Delete an asset (cascade will delete detail records)."""
        asset = AssetModel.get_by_id(asset_id)
        if not asset:
            raise ValueError("Asset not found")
        
        return AssetModel.delete(asset_id)

