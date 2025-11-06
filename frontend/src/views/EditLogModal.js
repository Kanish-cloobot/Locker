/**
 * Modal component for displaying asset edit history.
 */
import React from 'react';
import '../styles/Modal.css';

function EditLogModal({ isOpen, onClose, editLogs, assetName }) {
  if (!isOpen) return null;

  // Group logs by date (created_at timestamp)
  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  const formatFieldName = (fieldName) => {
    // Convert field names to readable format
    const fieldMap = {
      'name': 'Name',
      'asset_type': 'Asset Type',
      'worth_on_creation': 'Worth on Creation',
      'details': 'Details',
      'creation_date': 'Creation Date',
      'material_type': 'Material Type',
      'material_grade': 'Material Grade',
      'gifting_details': 'Gifting Details',
      'document_type': 'Document Type',
      'jewellery_material_type': 'Material Type',
      'jewellery_material_grade': 'Material Grade',
      'jewellery_gifting_details': 'Gifting Details'
    };
    return fieldMap[fieldName] || fieldName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Edit History - {assetName}</h2>
          <button className="modal-close-button" onClick={onClose}>×</button>
        </div>
        <div className="modal-body">
          {editLogs.length === 0 ? (
            <p>No edit history available for this asset.</p>
          ) : (
            <div className="edit-log-container">
              <table className="edit-log-table">
                <thead>
                  <tr>
                    <th>Date & Time</th>
                    <th>Field</th>
                    <th>Old Value</th>
                    <th>New Value</th>
                  </tr>
                </thead>
                <tbody>
                  {editLogs.map((log, index) => (
                    <tr key={index}>
                      <td>{formatDate(log.created_at)}</td>
                      <td>{formatFieldName(log.field_name)}</td>
                      <td className="old-value-cell">
                        {log.old_value || <span className="empty-value">(empty)</span>}
                      </td>
                      <td className="new-value-cell">
                        {log.new_value || <span className="empty-value">(empty)</span>}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
        <div className="modal-actions">
          <button type="button" onClick={onClose} className="cancel-button">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default EditLogModal;

