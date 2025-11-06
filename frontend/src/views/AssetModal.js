/**
 * Modal component for creating/editing assets.
 */
import React, { useState, useEffect } from 'react';
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

