/**
 * Modal component for creating/editing assets.
 */
import React, { useState, useEffect } from 'react';
import FileUpload from '../components/FileUpload';
import AssetService from '../presenters/assetService';
import '../styles/Modal.css';

function AssetModal({ onClose, onSave, asset }) {
  const isEditing = !!asset;
  const [formData, setFormData] = useState({
    name: '',
    asset_type: 'MISC',
    worth_on_creation: '',
    details: '',
    creation_date: '',
    material_type: '',
    material_grade: '',
    gifting_details: '',
    document_type: ''
  });
  const [errors, setErrors] = useState({});
  const [files, setFiles] = useState([]);
  const [pendingFiles, setPendingFiles] = useState([]);

  useEffect(() => {
    if (asset) {
      setFormData({
        name: asset.name || '',
        asset_type: asset.asset_type || 'MISC',
        worth_on_creation: asset.worth_on_creation || '',
        details: asset.details || '',
        creation_date: asset.creation_date || '',
        material_type: asset.jewellery_details?.material_type || '',
        material_grade: asset.jewellery_details?.material_grade || '',
        gifting_details: asset.jewellery_details?.gifting_details || '',
        document_type: asset.document_details?.document_type || ''
      });
      loadAssetFiles(asset.id);
    } else {
      setFiles([]);
    }
  }, [asset]);

  const loadAssetFiles = async (assetId) => {
    try {
      const assetFiles = await AssetService.getAssetFiles(assetId);
      // Add URL to each file
      const filesWithUrl = assetFiles.map(file => ({
        ...file,
        url: `http://localhost:5000/api/files/${file.id}`
      }));
      setFiles(filesWithUrl);
    } catch (err) {
      console.error('Error loading asset files:', err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    if (!formData.asset_type) {
      newErrors.asset_type = 'Asset type is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validate()) {
      const submitData = {
        name: formData.name,
        asset_type: formData.asset_type,
        worth_on_creation: formData.worth_on_creation ? parseFloat(formData.worth_on_creation) : null,
        details: formData.details || null,
        creation_date: formData.creation_date || null
      };

      if (formData.asset_type === 'JEWELLERY') {
        submitData.material_type = formData.material_type || null;
        submitData.material_grade = formData.material_grade || null;
        submitData.gifting_details = formData.gifting_details || null;
      } else if (formData.asset_type === 'DOCUMENT') {
        submitData.document_type = formData.document_type || null;
      }

      // For new assets, pass pending files to be uploaded after creation
      if (!isEditing && pendingFiles.length > 0) {
        submitData.pendingFiles = pendingFiles;
      }

      onSave(submitData);
    }
  };

  const handlePendingFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    if (selectedFiles.length === 0) return;
    setPendingFiles([...pendingFiles, ...selectedFiles]);
    e.target.value = ''; // Reset input
  };

  const handleRemovePendingFile = (index) => {
    setPendingFiles(pendingFiles.filter((_, i) => i !== index));
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content large-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{isEditing ? 'Edit Asset' : 'Create New Asset'}</h2>
          <button className="modal-close-button" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label htmlFor="name">Asset Name *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className={errors.name ? 'error' : ''}
            />
            {errors.name && <span className="error-message">{errors.name}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="asset_type">Asset Type *</label>
            <select
              id="asset_type"
              name="asset_type"
              value={formData.asset_type}
              onChange={handleChange}
              className={errors.asset_type ? 'error' : ''}
            >
              <option value="MISC">Miscellaneous</option>
              <option value="JEWELLERY">Jewellery</option>
              <option value="DOCUMENT">Document</option>
            </select>
            {errors.asset_type && <span className="error-message">{errors.asset_type}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="worth_on_creation">Worth on Creation</label>
            <input
              type="number"
              id="worth_on_creation"
              name="worth_on_creation"
              value={formData.worth_on_creation}
              onChange={handleChange}
              step="0.01"
              min="0"
            />
          </div>

          <div className="form-group">
            <label htmlFor="creation_date">Creation Date</label>
            <input
              type="date"
              id="creation_date"
              name="creation_date"
              value={formData.creation_date}
              onChange={handleChange}
            />
          </div>

          {formData.asset_type === 'JEWELLERY' && (
            <>
              <div className="form-group">
                <label htmlFor="material_type">Material Type</label>
                <input
                  type="text"
                  id="material_type"
                  name="material_type"
                  value={formData.material_type}
                  onChange={handleChange}
                  placeholder="e.g., Gold, Diamond"
                />
              </div>

              <div className="form-group">
                <label htmlFor="material_grade">Material Grade</label>
                <input
                  type="text"
                  id="material_grade"
                  name="material_grade"
                  value={formData.material_grade}
                  onChange={handleChange}
                  placeholder="e.g., 22k, VS1 Clarity"
                />
              </div>

              <div className="form-group">
                <label htmlFor="gifting_details">Gifting Details</label>
                <textarea
                  id="gifting_details"
                  name="gifting_details"
                  value={formData.gifting_details}
                  onChange={handleChange}
                  rows="3"
                  placeholder="Who gifted, when given, why purchased, etc."
                />
              </div>
            </>
          )}

          {formData.asset_type === 'DOCUMENT' && (
            <div className="form-group">
              <label htmlFor="document_type">Document Type</label>
              <input
                type="text"
                id="document_type"
                name="document_type"
                value={formData.document_type}
                onChange={handleChange}
                placeholder="e.g., Title Deed, Birth Certificate"
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="details">Details / Notes</label>
            <textarea
              id="details"
              name="details"
              value={formData.details}
              onChange={handleChange}
              rows="3"
              placeholder="Additional notes about this asset"
            />
          </div>

          <div className="form-group">
            <label>Files (Images/PDFs)</label>
            {isEditing && asset ? (
              <FileUpload
                assetId={asset.id}
                files={files}
                onFilesChange={setFiles}
              />
            ) : (
              <div className="file-upload-container">
                <div className="file-upload-header">
                  <label htmlFor="pending-file-upload-input" className="file-upload-button">
                    + Select Files (Images/PDF)
                  </label>
                  <input
                    id="pending-file-upload-input"
                    type="file"
                    multiple
                    accept="image/*,.pdf"
                    onChange={handlePendingFileSelect}
                    style={{ display: 'none' }}
                  />
                </div>
                {pendingFiles.length > 0 && (
                  <div className="file-preview-grid">
                    {pendingFiles.map((file, index) => (
                      <div key={index} className="file-preview-item">
                        <div className="file-preview-content">
                          {file.type.startsWith('image/') ? (
                            <img
                              src={URL.createObjectURL(file)}
                              alt={file.name}
                              className="file-preview-image"
                            />
                          ) : (
                            <div className="file-preview-pdf">
                              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                                <path d="M14 2V8H20" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                              </svg>
                              <span>{file.name}</span>
                            </div>
                          )}
                        </div>
                        <div className="file-preview-info">
                          <span className="file-name">{file.name}</span>
                          <button
                            className="file-delete-button"
                            onClick={() => handleRemovePendingFile(index)}
                            title="Remove file"
                          >
                            ×
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                <p className="file-upload-hint">Files will be uploaded after the asset is created.</p>
              </div>
            )}
          </div>

          <div className="modal-actions">
            <button type="button" onClick={onClose} className="cancel-button">
              Cancel
            </button>
            <button type="submit" className="save-button">
              {isEditing ? 'Update Asset' : 'Create Asset'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AssetModal;

