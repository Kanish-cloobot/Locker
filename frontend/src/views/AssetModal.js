/**
 * Modal component for creating/editing assets.
 */
import React, { useState, useEffect } from 'react';
import FileService from '../presenters/fileService';
import PDFPreview from '../components/PDFPreview';
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
  const [uploading, setUploading] = useState(false);

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
      setFiles(asset.files || []);
    }
  }, [asset]);

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

  const handleSubmit = (e) => {
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

      onSave(submitData);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    if (!asset || !asset.id) {
      alert('Please save the asset first before uploading files');
      return;
    }

    setUploading(true);
    try {
      const uploadedFile = await FileService.uploadFile(asset.id, file);
      setFiles(prev => [...prev, uploadedFile]);
    } catch (err) {
      alert('Failed to upload file: ' + err.message);
    } finally {
      setUploading(false);
      e.target.value = ''; // Reset input
    }
  };

  const getFileType = (file) => {
    if (file.file_type) {
      return file.file_type;
    }
    const fileName = file.original_file_name || file.file_name || '';
    const ext = fileName.split('.').pop()?.toLowerCase();
    if (ext === 'pdf') return 'PDF';
    if (['png', 'jpg', 'jpeg', 'gif'].includes(ext)) return 'IMAGE';
    return 'UNKNOWN';
  };

  const handleFileDelete = async (fileId) => {
    if (!window.confirm('Are you sure you want to delete this file?')) return;
    
    try {
      await FileService.deleteFile(fileId);
      setFiles(prev => prev.filter(f => f.id !== fileId));
    } catch (err) {
      alert('Failed to delete file: ' + err.message);
    }
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

          {isEditing && (
            <div className="form-group">
              <label>Files (Images/PDFs)</label>
              <input
                type="file"
                accept="image/*,.pdf"
                onChange={handleFileUpload}
                disabled={uploading}
                className="file-input"
              />
              {uploading && <p className="uploading-message">Uploading...</p>}
              {files.length > 0 && (
                <div className="files-preview-container">
                  {files.map(file => {
                    const fileType = getFileType(file);
                    return (
                      <div key={file.id} className="file-preview-item">
                        <div className="file-preview-header">
                          <span className="file-name">
                            {file.original_file_name || file.file_name}
                          </span>
                          <button
                            type="button"
                            onClick={() => handleFileDelete(file.id)}
                            className="delete-file-button"
                            title="Delete file"
                          >
                            ×
                          </button>
                        </div>
                        {fileType === 'PDF' ? (
                          <PDFPreview file={file} />
                        ) : fileType === 'IMAGE' ? (
                          <div className="image-preview-container">
                            <img
                              src={file.thumbnail_path ? FileService.getThumbnailUrl(file.id) : FileService.getFileUrl(file.id)}
                              alt={file.original_file_name || file.file_name}
                              className="image-preview"
                              onError={(e) => {
                                e.target.src = FileService.getFileUrl(file.id);
                              }}
                            />
                            <a
                              href={FileService.getFileUrl(file.id)}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="view-full-image-link"
                            >
                              View Full Size
                            </a>
                          </div>
                        ) : (
                          <div className="file-link-container">
                            <a 
                              href={FileService.getFileUrl(file.id)} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="file-download-link"
                            >
                              Download {file.original_file_name || file.file_name}
                            </a>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}

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

