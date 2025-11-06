/**
 * Asset card component with thumbnail/preview support.
 */
import React, { useState, useEffect } from 'react';
import FileService from '../presenters/fileService';
import AssetService from '../presenters/assetService';
import '../styles/AssetCard.css';

function AssetCard({ asset, onEdit, onDelete, onViewHistory }) {
  const [thumbnail, setThumbnail] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadThumbnail();
  }, [asset.id]);

  const loadThumbnail = async () => {
    try {
      setLoading(true);
      const files = await AssetService.getAssetFiles(asset.id);
      // Find first image file for thumbnail
      const imageFile = files.find(file => file.file_type === 'IMAGE');
      if (imageFile) {
        const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
        setThumbnail(`${API_BASE_URL}/api/files/${imageFile.id}`);
      } else {
        // Check for PDF
        const pdfFile = files.find(file => file.file_type === 'PDF');
        if (pdfFile) {
          setThumbnail('PDF');
        } else {
          setThumbnail(null);
        }
      }
    } catch (err) {
      console.error('Error loading thumbnail:', err);
      setThumbnail(null);
    } finally {
      setLoading(false);
    }
  };

  const getAssetTypeLabel = (type) => {
    const labels = {
      'JEWELLERY': 'Jewellery',
      'DOCUMENT': 'Document',
      'MISC': 'Miscellaneous'
    };
    return labels[type] || type;
  };

  return (
    <div className="asset-card">
      <div className="asset-card-thumbnail">
        {loading ? (
          <div className="thumbnail-loading">Loading...</div>
        ) : thumbnail ? (
          thumbnail === 'PDF' ? (
            <div className="thumbnail-pdf">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M14 2V8H20" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
          ) : (
            <img 
              src={thumbnail} 
              alt={asset.name}
              onError={(e) => {
                console.error('Error loading thumbnail image:', thumbnail);
                e.target.style.display = 'none';
                setThumbnail(null);
              }}
            />
          )
        ) : (
          <div className="thumbnail-placeholder">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 16L8.586 11.414C9.367 10.633 10.633 10.633 11.414 11.414L16 16M14 14L15.586 12.414C16.367 11.633 17.633 11.633 18.414 12.414L20 14M14 8H14.01M6 20H18C19.1046 20 20 19.1046 20 18V6C20 4.89543 19.1046 4 18 4H6C4.89543 4 4 4.89543 4 6V18C4 19.1046 4.89543 20 6 20Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
        )}
      </div>
      <div className="asset-card-content">
        <div className="asset-card-header">
          <h3>{asset.name}</h3>
          <span className={`asset-type-badge ${asset.asset_type.toLowerCase()}`}>
            {getAssetTypeLabel(asset.asset_type)}
          </span>
        </div>
        <div className="asset-card-details">
          {asset.worth_on_creation && (
            <div className="asset-detail-item">
              <strong>Worth:</strong> ${parseFloat(asset.worth_on_creation).toFixed(2)}
            </div>
          )}
          {asset.creation_date && (
            <div className="asset-detail-item">
              <strong>Created:</strong> {asset.creation_date}
            </div>
          )}
          {asset.asset_type === 'JEWELLERY' && asset.jewellery_details && (
            <div className="asset-detail-item">
              <strong>Material:</strong> {asset.jewellery_details.material_type || 'N/A'}
            </div>
          )}
          {asset.asset_type === 'DOCUMENT' && asset.document_details && (
            <div className="asset-detail-item">
              <strong>Type:</strong> {asset.document_details.document_type || 'N/A'}
            </div>
          )}
          {asset.details && (
            <div className="asset-detail-item asset-notes">
              {asset.details}
            </div>
          )}
        </div>
        <div className="asset-card-actions">
          <button className="action-button edit-button" onClick={() => onEdit(asset)}>
            Edit
          </button>
          <button className="action-button history-button" onClick={() => onViewHistory(asset)}>
            History
          </button>
          <button className="action-button delete-button" onClick={() => onDelete(asset.id)}>
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}

export default AssetCard;

