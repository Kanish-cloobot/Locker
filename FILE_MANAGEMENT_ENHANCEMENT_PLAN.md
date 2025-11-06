# File Management Enhancement - Implementation Plan

## Overview
This document outlines the comprehensive file management enhancement that was implemented to improve file storage, thumbnail generation, and file preview capabilities in the Locker application.

---

## Enhancement Goals

1. **Improved File Storage System**: Create a new comprehensive file storage table with better metadata tracking
2. **Automatic Thumbnail Generation**: Generate thumbnails for images automatically
3. **PDF Preview Support**: Enable inline PDF preview in the frontend
4. **Thumbnail Management**: Allow users to set/change asset thumbnails
5. **Backward Compatibility**: Maintain compatibility with existing AssetFile table

---

## Implementation Plan

### Phase 1: Database Schema Enhancement

#### 1.1 Create New LockerFileStorage Table
**Location**: `backend/database/db_setup.py` (lines 138-158)

**Purpose**: Replace the basic AssetFile table with a more comprehensive storage solution.

**Key Features**:
- Stores original filename and stored filename (UUID-based)
- Tracks file type (IMAGE or PDF)
- Stores file size and MIME type
- Supports thumbnail path storage
- Includes `is_thumbnail` flag for marking primary thumbnails
- Implements soft delete with `status` field (active/deleted)
- Tracks creation and update timestamps

**Schema**:
```sql
CREATE TABLE LockerFileStorage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    original_file_name TEXT NOT NULL,
    stored_file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT NOT NULL CHECK(file_type IN ('IMAGE', 'PDF')),
    file_size INTEGER,
    mime_type TEXT,
    thumbnail_path TEXT,
    is_thumbnail BOOLEAN DEFAULT 0,
    org_id INTEGER NOT NULL DEFAULT 1,
    user_id INTEGER NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (asset_id) REFERENCES Asset(id)
)
```

---

### Phase 2: Backend Model Implementation

#### 2.1 Create LockerFileStorageModel
**Location**: `backend/models/locker_file_storage.py`

**Key Methods Implemented**:

1. **`get_by_asset_id(asset_id)`**: Get all active files for an asset
2. **`get_images_by_asset_id(asset_id)`**: Get only image files for an asset
3. **`get_thumbnail_by_asset_id(asset_id)`**: Get thumbnail with fallback logic:
   - First: Get marked thumbnail image
   - Second: Get first image if no thumbnail marked
   - Third: Get first PDF if no images exist
4. **`get_by_id(file_id)`**: Get single file by ID
5. **`create(...)`**: Create new file record with all metadata
6. **`set_as_thumbnail(file_id)`**: Set a file as thumbnail (unsets others for same asset)
7. **`delete(file_id)`**: Soft delete file (sets status to 'deleted')

---

### Phase 3: Backend API Routes Enhancement

#### 3.1 File Upload Endpoint
**Location**: `backend/views/file_routes.py` (lines 32-116)

**Route**: `POST /api/assets/<asset_id>/files`

**Enhancement Features**:
1. **File Validation**: 
   - Checks file extension (PNG, JPG, JPEG, GIF, PDF)
   - Validates file presence

2. **Unique Filename Generation**:
   - Uses UUID to generate unique filenames
   - Prevents filename conflicts

3. **Asset-Specific Folders**:
   - Creates folder structure: `uploads/{asset_id}/`
   - Organizes files by asset

4. **Automatic Thumbnail Generation** (for images):
   - Uses PIL (Pillow) to create 200x200 thumbnails
   - Saves thumbnails with `thumb_` prefix
   - Stores thumbnail path in database

5. **Automatic Thumbnail Assignment**:
   - First image uploaded becomes the default thumbnail
   - Sets `is_thumbnail = True` automatically

6. **Dual Storage**:
   - Stores in new LockerFileStorage table
   - Also stores in AssetFile table for backward compatibility

#### 3.2 File Download Endpoint
**Location**: `backend/views/file_routes.py` (lines 151-232)

**Route**: `GET /api/files/<file_id>/download`

**Features**:
- Supports both LockerFileStorage and AssetFile (backward compatibility)
- Handles relative and absolute paths
- Sets proper MIME types for different file types
- Includes CORS headers for frontend access
- Comprehensive error handling with debug logging

#### 3.3 Thumbnail Endpoint
**Location**: `backend/views/file_routes.py` (lines 235-285)

**Route**: `GET /api/files/<file_id>/thumbnail`

**Features**:
- Returns thumbnail if available
- Falls back to original file if no thumbnail
- Proper MIME type handling
- CORS support

#### 3.4 Set Thumbnail Endpoint
**Location**: `backend/views/file_routes.py` (lines 288-298)

**Route**: `POST /api/files/<file_id>/set-thumbnail`

**Features**:
- Allows users to change which image is the thumbnail
- Automatically unsets other thumbnails for the same asset
- Updates database accordingly

#### 3.5 Get Asset Files Endpoint
**Location**: `backend/views/file_routes.py` (lines 301-312)

**Route**: `GET /api/assets/<asset_id>/files`

**Features**:
- Returns all files for an asset
- Prioritizes LockerFileStorage, falls back to AssetFile

---

### Phase 4: Frontend Service Layer

#### 4.1 FileService Enhancement
**Location**: `frontend/src/presenters/fileService.js`

**New Methods Added**:

1. **`uploadFile(assetId, file)`**: Upload file with FormData
2. **`deleteFile(fileId)`**: Delete a file
3. **`getFileUrl(fileId)`**: Get download URL for a file
4. **`getThumbnailUrl(fileId)`**: Get thumbnail URL for a file
5. **`setAsThumbnail(fileId)`**: Set a file as thumbnail

---

### Phase 5: Frontend Components

#### 5.1 PDF Preview Component
**Location**: `frontend/src/components/PDFPreview.js`

**Features**:
- Displays PDFs inline using iframe
- Shows loading state while PDF loads
- Error handling with fallback to download link
- Displays PDF filename
- Uses `#toolbar=0` to hide PDF toolbar

#### 5.2 Asset Modal Enhancement
**Location**: `frontend/src/views/AssetModal.js`

**File Management Features**:
- File upload input (only shown when editing existing asset)
- File preview section showing:
  - Images: Thumbnail preview with "View Full Size" link
  - PDFs: Inline PDF preview using PDFPreview component
  - Other files: Download link
- Delete file button for each file
- Upload progress indicator

**Key Implementation Details**:
- Files are only uploadable after asset is created
- Uses thumbnail URL if available, falls back to full image
- Handles both old (AssetFile) and new (LockerFileStorage) file formats

#### 5.3 Locker Detail Page Enhancement
**Location**: `frontend/src/views/LockerDetailPage.js`

**Thumbnail Display Features**:
- Shows thumbnail in assets table
- For images: Displays thumbnail with fallback to full image
- For PDFs: Shows PDF icon with clickable link
- Placeholder for assets without files
- Error handling for broken image links

---

### Phase 6: Service Layer Integration

#### 6.1 Asset Service Updates
**Location**: `backend/presenters/asset_service.py`

**Enhancements**:
- `get_assets_by_locker()`: Now includes thumbnail from LockerFileStorage
- `get_asset_by_id()`: Returns files and thumbnail from LockerFileStorage
- Fallback logic: If LockerFileStorage has no data, falls back to AssetFile
- Converts old AssetFile format to match new format expectations

---

## Technical Implementation Details

### File Storage Structure
```
uploads/
  └── {asset_id}/
      ├── {uuid}.{ext}          # Original file
      └── thumb_{uuid}.{ext}     # Thumbnail (images only)
```

### Thumbnail Generation Process
1. User uploads an image file
2. Backend saves original file with UUID filename
3. PIL opens the image and creates 200x200 thumbnail
4. Thumbnail saved with `thumb_` prefix
5. Both paths stored in database
6. If first image for asset, automatically set as thumbnail

### Backward Compatibility Strategy
- All new uploads go to both LockerFileStorage and AssetFile tables
- Read operations check LockerFileStorage first, then AssetFile
- Old file format is converted to new format when retrieved
- This ensures existing files continue to work

### File Type Detection
- Backend: Uses file extension to determine type (IMAGE or PDF)
- Frontend: Checks `file_type` field or infers from filename extension
- Supported types: PNG, JPG, JPEG, GIF (images), PDF (documents)

---

## API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/assets/<asset_id>/files` | Upload a file |
| GET | `/api/assets/<asset_id>/files` | Get all files for an asset |
| GET | `/api/files/<file_id>` | Get file information |
| GET | `/api/files/<file_id>/download` | Download a file |
| GET | `/api/files/<file_id>/thumbnail` | Get thumbnail for a file |
| POST | `/api/files/<file_id>/set-thumbnail` | Set a file as thumbnail |
| DELETE | `/api/files/<file_id>` | Delete a file |

---

## Dependencies Added

### Backend
- **Pillow (PIL)**: For image processing and thumbnail generation
  - Added to `requirements.txt`
  - Used in `file_routes.py` for thumbnail creation

### Frontend
- No new dependencies required
- Uses native browser PDF viewing via iframe

---

## Key Features Delivered

✅ **Comprehensive File Storage**: New LockerFileStorage table with rich metadata  
✅ **Automatic Thumbnails**: Images automatically get 200x200 thumbnails  
✅ **PDF Preview**: Inline PDF viewing in the frontend  
✅ **Thumbnail Management**: Users can set/change asset thumbnails  
✅ **Backward Compatibility**: Existing AssetFile records still work  
✅ **Organized Storage**: Files organized by asset in separate folders  
✅ **Soft Delete**: Files marked as deleted, not physically removed  
✅ **Error Handling**: Comprehensive error handling throughout  
✅ **CORS Support**: Proper CORS headers for file access  

---

## Testing Considerations

1. **File Upload**: Test with various image formats and PDFs
2. **Thumbnail Generation**: Verify thumbnails are created correctly
3. **PDF Preview**: Test PDF viewing in different browsers
4. **Thumbnail Setting**: Test changing thumbnails
5. **File Deletion**: Verify soft delete works correctly
6. **Backward Compatibility**: Ensure old files still display
7. **Error Cases**: Test with invalid files, missing files, etc.

---

## Future Enhancements (Potential)

- Image cropping/editing before upload
- Multiple file upload at once
- File compression for large images
- Video file support
- File versioning
- Cloud storage integration (S3, etc.)
- Image gallery view
- Drag-and-drop file upload

---

## Notes

- All file paths are stored as relative paths (`uploads/{asset_id}/{filename}`)
- Physical file deletion is optional (currently implemented in soft delete)
- Thumbnail generation only happens for images, not PDFs
- First image uploaded automatically becomes thumbnail
- Users can change thumbnail via the set-thumbnail endpoint

