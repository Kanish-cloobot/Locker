/**
 * File upload component for images and PDFs.
 */
import React, { useState } from 'react';
import FileService from '../presenters/fileService';
import PDFPreviewModal from './PDFPreviewModal';
import '../styles/FileUpload.css';

function FileUpload({ assetId, files = [], onFilesChange }) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [previewFile, setPreviewFile] = useState(null);

  const handleFileSelect = async (e) => {
    const selectedFiles = Array.from(e.target.files);
    if (selectedFiles.length === 0) return;

    setError(null);
    setUploading(true);

    try {
      const uploadPromises = selectedFiles.map(file => FileService.uploadFile(assetId, file));
      const uploadedFiles = await Promise.all(uploadPromises);
      onFilesChange([...files, ...uploadedFiles]);
    } catch (err) {
      setError(err.message || 'Failed to upload files');
    } finally {
      setUploading(false);
      e.target.value = ''; // Reset input
    }
  };

  const handleDeleteFile = async (fileId) => {
    try {
      await FileService.deleteFile(fileId);
      onFilesChange(files.filter(file => file.id !== fileId));
    } catch (err) {
      alert('Failed to delete file: ' + err.message);
    }
  };

  const handleFileClick = (file) => {
    if (file.file_type === 'PDF') {
      setPreviewFile(file);
    }
  };

  const getFilePreview = (file) => {
    if (file.file_type === 'IMAGE') {
      return (
        <img
          src={FileService.getFileUrl(file.id)}
          alt={file.file_name}
          className="file-preview-image"
        />
      );
    } else {
      return (
        <div 
          className="file-preview-pdf clickable-pdf"
          onClick={() => handleFileClick(file)}
          title="Click to preview PDF"
        >
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M14 2V8H20" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span>{file.file_name}</span>
        </div>
      );
    }
  };

  return (
    <div className="file-upload-container">
      <div className="file-upload-header">
        <label htmlFor="file-upload-input" className="file-upload-button">
          {uploading ? 'Uploading...' : '+ Upload Files (Images/PDF)'}
        </label>
        <input
          id="file-upload-input"
          type="file"
          multiple
          accept="image/*,.pdf"
          onChange={handleFileSelect}
          disabled={uploading || !assetId}
          style={{ display: 'none' }}
        />
      </div>

      {error && <div className="file-upload-error">{error}</div>}

      {files.length > 0 && (
        <div className="file-preview-grid">
          {files.map(file => (
            <div key={file.id} className="file-preview-item">
              <div className="file-preview-content">
                {getFilePreview(file)}
              </div>
              <div className="file-preview-info">
                <span className="file-name">{file.file_name}</span>
                <button
                  className="file-delete-button"
                  onClick={() => handleDeleteFile(file.id)}
                  title="Delete file"
                >
                  ×
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {previewFile && (
        <PDFPreviewModal
          file={previewFile}
          onClose={() => setPreviewFile(null)}
        />
      )}
    </div>
  );
}

export default FileUpload;

