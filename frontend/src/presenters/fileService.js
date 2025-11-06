/**
 * File service for API calls.
 */
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class FileService {
  /**
   * Upload a file for an asset.
   */
  static async uploadFile(assetId, file) {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_BASE_URL}/api/assets/${assetId}/files`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to upload file');
      }

      const fileData = await response.json();
      // Add URL to file data
      fileData.url = `${API_BASE_URL}/api/files/${fileData.id}`;
      return fileData;
    } catch (error) {
      console.error('Error uploading file:', error);
      throw error;
    }
  }

  /**
   * Delete a file.
   */
  static async deleteFile(fileId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/files/${fileId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to delete file');
      }

      return true;
    } catch (error) {
      console.error('Error deleting file:', error);
      throw error;
    }
  }

  /**
   * Get file URL.
   */
  static getFileUrl(fileId) {
    return `${API_BASE_URL}/api/files/${fileId}`;
  }
}

export default FileService;

