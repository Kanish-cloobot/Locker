"""
File upload API routes/views.
"""
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from backend.models.asset_file import AssetFileModel
from backend.models.locker_file_storage import LockerFileStorageModel
import os
import uuid
from PIL import Image

file_bp = Blueprint('file', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_type(filename):
    """Determine if file is IMAGE or PDF."""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    if ext == 'pdf':
        return 'PDF'
    elif ext in ['png', 'jpg', 'jpeg', 'gif']:
        return 'IMAGE'
    return None


@file_bp.route('/api/assets/<int:asset_id>/files', methods=['POST'])
def upload_file(asset_id):
    """Upload a file for an asset."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Allowed types: PNG, JPG, JPEG, GIF, PDF'}), 400
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        
        # Get upload folder from app config
        from flask import current_app
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        
        # Create asset-specific folder
        asset_folder = os.path.join(upload_folder, str(asset_id))
        if not os.path.exists(asset_folder):
            os.makedirs(asset_folder)
        
        file_path = os.path.join(asset_folder, unique_filename)
        file.save(file_path)
        
        # Store relative path for database
        relative_path = f"uploads/{asset_id}/{unique_filename}"
        
        # Create file record in new LockerFileStorage table
        file_type = get_file_type(filename)
        file_size = os.path.getsize(file_path)
        mime_type = file.content_type
        
        # Generate thumbnail for images
        thumbnail_path = None
        is_thumbnail = False
        if file_type == 'IMAGE':
            try:
                # Create thumbnail
                img = Image.open(file_path)
                img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                thumbnail_filename = f"thumb_{unique_filename}"
                thumbnail_path_full = os.path.join(asset_folder, thumbnail_filename)
                img.save(thumbnail_path_full)
                thumbnail_path = f"uploads/{asset_id}/{thumbnail_filename}"
                
                # Check if this is the first image for this asset (make it thumbnail)
                existing_images = LockerFileStorageModel.get_images_by_asset_id(asset_id)
                if len(existing_images) == 0:
                    is_thumbnail = True
            except Exception as e:
                print(f"Error creating thumbnail: {str(e)}")
        
        # Store in LockerFileStorage table
        file_id = LockerFileStorageModel.create(
            asset_id=asset_id,
            original_file_name=filename,
            stored_file_name=unique_filename,
            file_path=relative_path,
            file_type=file_type,
            file_size=file_size,
            mime_type=mime_type,
            thumbnail_path=thumbnail_path,
            is_thumbnail=is_thumbnail
        )
        
        # Also store in AssetFile for backward compatibility
        AssetFileModel.create(
            asset_id=asset_id,
            file_name=filename,
            file_path=relative_path,
            file_type=file_type
        )
        
        file_record = LockerFileStorageModel.get_by_id(file_id)
        return jsonify(file_record), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@file_bp.route('/api/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Delete a file."""
    try:
        # Delete from LockerFileStorage
        LockerFileStorageModel.delete(file_id)
        # Also delete from AssetFile if exists
        try:
            AssetFileModel.delete(file_id)
        except:
            pass  # Ignore if not in AssetFile
        return jsonify({'message': 'File deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@file_bp.route('/api/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    """Get file information."""
    try:
        # Try LockerFileStorage first
        file_record = LockerFileStorageModel.get_by_id(file_id)
        if not file_record:
            # Fallback to AssetFile for backward compatibility
            file_record = AssetFileModel.get_by_id(file_id)
        if not file_record:
            return jsonify({'error': 'File not found'}), 404
        return jsonify(file_record), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@file_bp.route('/api/files/<int:file_id>/download', methods=['GET'])
def download_file(file_id):
    """Download a file."""
    try:
        # Try LockerFileStorage first
        file_record = LockerFileStorageModel.get_by_id(file_id)
        is_locker_storage = True
        if not file_record:
            # Fallback to AssetFile
            file_record = AssetFileModel.get_by_id(file_id)
            is_locker_storage = False
        
        if not file_record:
            return jsonify({'error': 'File not found'}), 404
        
        # Get file path - LockerFileStorage uses 'file_path', AssetFile also uses 'file_path'
        file_path = file_record.get('file_path')
        if not file_path:
            return jsonify({'error': 'File path not found'}), 404
        
        # Convert relative path to absolute using Flask app config
        from flask import current_app
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        
        # If file_path is already absolute, use it; otherwise join with upload_folder
        if os.path.isabs(file_path):
            absolute_path = file_path
        else:
            # Remove 'uploads/' prefix if present since upload_folder already points to uploads directory
            if file_path.startswith('uploads/'):
                file_path = file_path.replace('uploads/', '', 1)
            absolute_path = os.path.join(upload_folder, file_path)
        
        # Debug logging
        print(f"Downloading file {file_id}:")
        print(f"  File path from DB: {file_record.get('file_path')}")
        print(f"  Upload folder: {upload_folder}")
        print(f"  Absolute path: {absolute_path}")
        print(f"  Path exists: {os.path.exists(absolute_path)}")
        
        if not os.path.exists(absolute_path):
            return jsonify({
                'error': f'File not found on server',
                'details': {
                    'file_id': file_id,
                    'file_path': file_record.get('file_path'),
                    'absolute_path': absolute_path,
                    'upload_folder': upload_folder,
                    'storage_type': 'LockerFileStorage' if is_locker_storage else 'AssetFile'
                }
            }), 404
        
        directory = os.path.dirname(absolute_path)
        filename = os.path.basename(absolute_path)
        
        # Determine content type based on file extension
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        mimetype = None
        if file_ext in ['jpg', 'jpeg']:
            mimetype = 'image/jpeg'
        elif file_ext == 'png':
            mimetype = 'image/png'
        elif file_ext == 'gif':
            mimetype = 'image/gif'
        elif file_ext == 'pdf':
            mimetype = 'application/pdf'
        
        response = send_from_directory(directory, filename, mimetype=mimetype)
        
        # Add CORS headers
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        
        return response
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error downloading file {file_id}: {str(e)}")
        print(f"Traceback: {error_trace}")
        return jsonify({'error': str(e), 'traceback': error_trace}), 500


@file_bp.route('/api/files/<int:file_id>/thumbnail', methods=['GET'])
def get_thumbnail(file_id):
    """Get thumbnail for a file."""
    try:
        file_record = LockerFileStorageModel.get_by_id(file_id)
        if not file_record:
            return jsonify({'error': 'File not found'}), 404
        
        # If it's an image and has thumbnail path
        if file_record.get('file_type') == 'IMAGE' and file_record.get('thumbnail_path'):
            thumbnail_path = file_record['thumbnail_path']
            from flask import current_app
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            
            # Remove 'uploads/' prefix if present
            if thumbnail_path.startswith('uploads/'):
                thumbnail_path = thumbnail_path.replace('uploads/', '', 1)
            absolute_path = os.path.join(upload_folder, thumbnail_path)
            
            if os.path.exists(absolute_path):
                directory = os.path.dirname(absolute_path)
                filename = os.path.basename(absolute_path)
                
                # Determine content type for thumbnail (should be image)
                file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                mimetype = None
                if file_ext in ['jpg', 'jpeg']:
                    mimetype = 'image/jpeg'
                elif file_ext == 'png':
                    mimetype = 'image/png'
                elif file_ext == 'gif':
                    mimetype = 'image/gif'
                
                response = send_from_directory(directory, filename, mimetype=mimetype)
                
                # Add CORS headers
                response.headers.add('Access-Control-Allow-Origin', '*')
                response.headers.add('Access-Control-Allow-Methods', 'GET')
                response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
                
                return response
        
        # Fallback to original file
        return download_file(file_id)
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error getting thumbnail for file {file_id}: {str(e)}")
        print(f"Traceback: {error_trace}")
        return jsonify({'error': str(e), 'traceback': error_trace}), 500


@file_bp.route('/api/files/<int:file_id>/set-thumbnail', methods=['POST'])
def set_thumbnail(file_id):
    """Set a file as thumbnail for its asset."""
    try:
        success = LockerFileStorageModel.set_as_thumbnail(file_id)
        if success:
            file_record = LockerFileStorageModel.get_by_id(file_id)
            return jsonify(file_record), 200
        return jsonify({'error': 'Failed to set thumbnail'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@file_bp.route('/api/assets/<int:asset_id>/files', methods=['GET'])
def get_asset_files(asset_id):
    """Get all files for an asset."""
    try:
        # Get from LockerFileStorage first
        files = LockerFileStorageModel.get_by_asset_id(asset_id)
        if not files:
            # Fallback to AssetFile
            files = AssetFileModel.get_by_asset_id(asset_id)
        return jsonify(files), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

