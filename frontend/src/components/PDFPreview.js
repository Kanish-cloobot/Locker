/**
 * PDF Preview component for displaying PDFs inline.
 */
import React, { useState } from 'react';
import FileService from '../presenters/fileService';
import '../styles/PDFPreview.css';

function PDFPreview({ file }) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const pdfUrl = FileService.getFileUrl(file.id);

  const fileName = file.original_file_name || file.file_name || 'PDF Document';
  
  return (
    <div className="pdf-preview-container">
      <div className="pdf-preview-header">
        <span className="pdf-icon">📄</span>
        <span className="pdf-filename">{fileName}</span>
      </div>
      {error ? (
        <div className="pdf-preview-error">
          <p>Unable to load PDF preview</p>
          <a 
            href={pdfUrl} 
            target="_blank" 
            rel="noopener noreferrer"
            className="pdf-download-link"
          >
            Download PDF
          </a>
        </div>
      ) : (
        <div className="pdf-preview-wrapper">
          {loading && (
            <div className="pdf-loading">
              <p>Loading PDF...</p>
            </div>
          )}
          <iframe
            src={`${pdfUrl}#toolbar=0`}
            className="pdf-iframe"
            title={`PDF Preview: ${fileName}`}
            onLoad={() => setLoading(false)}
            onError={() => {
              setLoading(false);
              setError(true);
            }}
            style={{ display: loading ? 'none' : 'block' }}
          />
        </div>
      )}
    </div>
  );
}

export default PDFPreview;

