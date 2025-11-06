"""
Asset API routes/views.
"""
from flask import Blueprint, request, jsonify
from backend.presenters.asset_service import AssetService

asset_bp = Blueprint('asset', __name__)


@asset_bp.route('/api/lockers/<int:locker_id>/assets', methods=['GET'])
def get_assets_by_locker(locker_id):
    """Get all assets for a specific locker."""
    try:
        assets = AssetService.get_assets_by_locker(locker_id)
        return jsonify(assets), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@asset_bp.route('/api/lockers/<int:locker_id>/assets', methods=['POST'])
def create_asset(locker_id):
    """Create a new asset in a locker."""
    try:
        data = request.get_json()
        asset = AssetService.create_asset(locker_id, data)
        return jsonify(asset), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@asset_bp.route('/api/assets/<int:asset_id>', methods=['PUT'])
def update_asset(asset_id):
    """Update an existing asset."""
    try:
        data = request.get_json()
        asset = AssetService.update_asset(asset_id, data)
        return jsonify(asset), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@asset_bp.route('/api/assets/<int:asset_id>', methods=['DELETE'])
def delete_asset(asset_id):
    """Delete an asset."""
    try:
        AssetService.delete_asset(asset_id)
        return jsonify({'message': 'Asset deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@asset_bp.route('/api/assets/<int:asset_id>/edit-history', methods=['GET'])
def get_asset_edit_history(asset_id):
    """Get edit history for an asset."""
    try:
        history = AssetService.get_asset_edit_history(asset_id)
        return jsonify(history), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@asset_bp.route('/api/assets/<int:asset_id>/files', methods=['GET'])
def get_asset_files(asset_id):
    """Get all files for an asset."""
    try:
        asset = AssetService.get_asset_with_files(asset_id)
        if not asset:
            return jsonify({'error': 'Asset not found'}), 404
        return jsonify(asset.get('files', [])), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
