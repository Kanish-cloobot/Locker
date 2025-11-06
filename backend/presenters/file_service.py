"""
File service for handling file uploads and storage.
"""
import os
import uuid
from werkzeug.utils import secure_filename
from backend.database.db_setup import get_db_path
from backend.models.asset_file import AssetFileModel


class FileService:
    """Service class for file operations."""
    
    ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    ALLOWED_PDF_EXTENSIONS = {'pdf'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def get_upload_dir():
        """Get the upload directory path."""
        db_path = get_db_path()
        backend_dir = os.path.dirname(db_path)
        upload_dir = os.path.join(backend_dir, 'uploads', 'assets')
        return upload_dir
    
    @staticmethod
    def validate_file(file):
        """Validate uploaded file."""
        if not file or not file.filename:
            raise ValueError("No file provided")
        
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if ext not in FileService.ALLOWED_IMAGE_EXTENSIONS and ext not in FileService.ALLOWED_PDF_EXTENSIONS:
            raise ValueError(f"File type not allowed. Allowed: images ({', '.join(FileService.ALLOWED_IMAGE_EXTENSIONS)}), PDF")
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > FileService.MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds maximum allowed size of {FileService.MAX_FILE_SIZE / (1024*1024)}MB")
        
        return filename, ext
    
    @staticmethod
    def save_file(file, asset_id):
        """Save uploaded file and return file record."""
        filename, ext = FileService.validate_file(file)
        
        # Determine file type
        if ext in FileService.ALLOWED_IMAGE_EXTENSIONS:
            file_type = 'IMAGE'
        else:
            file_type = 'PDF'
        
        # Create upload directory for asset if it doesn't exist
        upload_dir = FileService.get_upload_dir()
        asset_dir = os.path.join(upload_dir, str(asset_id))
        os.makedirs(asset_dir, exist_ok=True)
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(asset_dir, unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Create database record
        file_id = AssetFileModel.create(
            asset_id=asset_id,
            file_name=filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size
        )
        
        return AssetFileModel.get_by_id(file_id)
    
    @staticmethod
    def delete_file(file_id):
        """Delete a file and its record."""
        file_record = AssetFileModel.get_by_id(file_id)
        if not file_record:
            raise ValueError("File not found")
        
        # Delete physical file
        file_path = file_record['file_path']
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass  # File might already be deleted
        
        # Delete database record
        return AssetFileModel.delete(file_id)
    
    @staticmethod
    def get_file_url(file_id):
        """Get URL path for a file."""
        file_record = AssetFileModel.get_by_id(file_id)
        if not file_record:
            return None
        
        # Return relative path from backend directory
        db_path = get_db_path()
        backend_dir = os.path.dirname(db_path)
        relative_path = os.path.relpath(file_record['file_path'], backend_dir)
        
        # Convert to URL-friendly path (use forward slashes)
        return relative_path.replace('\\', '/')

