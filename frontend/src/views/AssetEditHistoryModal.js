/**
 * Modal component for displaying asset edit history.
 */
import React, { useState, useEffect } from 'react';
import AssetService from '../presenters/assetService';
import '../styles/Modal.css';
import '../styles/AssetEditHistoryModal.css';

function AssetEditHistoryModal({ asset, onClose }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, [asset.id]);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const historyData = await AssetService.getEditHistory(asset.id);
      setHistory(historyData);
    } catch (err) {
      console.error('Error loading edit history:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatFieldName = (fieldName) => {
    return fieldName
      .replace(/_/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content large-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Edit History - {asset.name}</h2>
          <button className="modal-close-button" onClick={onClose}>×</button>
        </div>
        <div className="edit-history-content">
          {loading ? (
            <div className="loading-message">Loading edit history...</div>
          ) : history.length === 0 ? (
            <div className="empty-history">
              <p>No edit history found for this asset.</p>
            </div>
          ) : (
            <div className="history-list">
              {history.map((entry, index) => (
                <div key={entry.id} className="history-entry">
                  <div className="history-header">
                    <span className="history-date">{entry.edited_at}</span>
                    <span className="history-editor">by {entry.edited_by}</span>
                  </div>
                  <div className="history-changes">
                    <h4>Fields Edited:</h4>
                    <ul>
                      {entry.edited_fields.map((field, fieldIndex) => (
                        <li key={fieldIndex} className="change-item">
                          <strong>{formatFieldName(field)}:</strong>
                          <div className="change-values">
                            <span className="old-value">
                              {entry.old_values[field] !== null && entry.old_values[field] !== undefined
                                ? String(entry.old_values[field])
                                : '(empty)'}
                            </span>
                            <span className="arrow">→</span>
                            <span className="new-value">
                              {entry.new_values[field] !== null && entry.new_values[field] !== undefined
                                ? String(entry.new_values[field])
                                : '(empty)'}
                            </span>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
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

export default AssetEditHistoryModal;

