"""
File API routes/views.
"""
import os
from flask import Blueprint, request, jsonify, send_from_directory
from backend.presenters.file_service import FileService
from backend.models.asset_file import AssetFileModel
from backend.database.db_setup import get_db_path

file_bp = Blueprint('file', __name__)


@file_bp.route('/api/assets/<int:asset_id>/files', methods=['POST'])
def upload_file(asset_id):
    """Upload a file for an asset."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        file_record = FileService.save_file(file, asset_id)
        return jsonify(file_record), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@file_bp.route('/api/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Delete a file."""
    try:
        FileService.delete_file(file_id)
        return jsonify({'message': 'File deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@file_bp.route('/api/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    """Serve a file."""
    try:
        file_record = AssetFileModel.get_by_id(file_id)
        if not file_record:
            return jsonify({'error': 'File not found'}), 404
        
        file_path = file_record['file_path']
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found on disk'}), 404
        
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        
        # Determine MIME type based on file extension
        from mimetypes import guess_type
        mimetype, _ = guess_type(file_path)
        if not mimetype:
            # Default MIME types
            if file_record['file_type'] == 'IMAGE':
                mimetype = 'image/jpeg'
            elif file_record['file_type'] == 'PDF':
                mimetype = 'application/pdf'
            else:
                mimetype = 'application/octet-stream'
        
        return send_from_directory(
            directory, 
            filename, 
            mimetype=mimetype,
            as_attachment=False
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@file_bp.route('/api/assets/<int:asset_id>/files', methods=['GET'])
def get_asset_files(asset_id):
    """Get all files for an asset."""
    try:
        files = AssetFileModel.get_by_asset_id(asset_id)
        # Add URL to each file record
        for file_record in files:
            file_record['url'] = f'/api/files/{file_record["id"]}'
        return jsonify(files), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

