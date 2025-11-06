/**
 * PDF Preview Modal component.
 */
import React from 'react';
import FileService from '../presenters/fileService';
import '../styles/PDFPreviewModal.css';

function PDFPreviewModal({ file, onClose }) {
  if (!file) return null;

  const pdfUrl = file.id ? FileService.getFileUrl(file.id) : (file.url || file);

  return (
    <div className="pdf-preview-overlay" onClick={onClose}>
      <div className="pdf-preview-content" onClick={(e) => e.stopPropagation()}>
        <div className="pdf-preview-header">
          <h3>{file.file_name || file.name || 'PDF Preview'}</h3>
          <button className="pdf-preview-close-button" onClick={onClose}>×</button>
        </div>
        <div className="pdf-preview-body">
          <iframe
            src={pdfUrl}
            title={file.file_name || file.name || 'PDF Preview'}
            className="pdf-preview-iframe"
          />
        </div>
      </div>
    </div>
  );
}

export default PDFPreviewModal;

