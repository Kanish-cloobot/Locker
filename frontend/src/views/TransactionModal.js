/**
 * Modal component for creating/editing transactions.
 */
import React, { useState, useEffect } from 'react';
import '../styles/Modal.css';

function TransactionModal({ onClose, onSave, transaction, assets, lockerId }) {
  const isEditing = !!transaction;
  const [formData, setFormData] = useState({
    asset_id: '',
    transaction_type: 'DEPOSIT',
    reason: '',
    responsible_person: '',
    transaction_date: new Date().toISOString().split('T')[0]
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (transaction) {
      setFormData({
        asset_id: transaction.asset_id || '',
        transaction_type: transaction.transaction_type || 'DEPOSIT',
        reason: transaction.reason || '',
        responsible_person: transaction.responsible_person || '',
        transaction_date: transaction.transaction_date ? transaction.transaction_date.split(' ')[0] : new Date().toISOString().split('T')[0]
      });
    }
  }, [transaction]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.asset_id) {
      newErrors.asset_id = 'Asset is required';
    }
    if (!formData.transaction_type) {
      newErrors.transaction_type = 'Transaction type is required';
    }
    if (!formData.transaction_date) {
      newErrors.transaction_date = 'Transaction date is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      const submitData = {
        ...formData,
        locker_id: lockerId,
        asset_id: parseInt(formData.asset_id)
      };
      onSave(submitData);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{isEditing ? 'Edit Transaction' : 'Create New Transaction'}</h2>
          <button className="modal-close-button" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label htmlFor="asset_id">Linked Asset *</label>
            <select
              id="asset_id"
              name="asset_id"
              value={formData.asset_id}
              onChange={handleChange}
              className={errors.asset_id ? 'error' : ''}
              disabled={isEditing}
            >
              <option value="">Select an asset</option>
              {assets.map(asset => (
                <option key={asset.id} value={asset.id}>
                  {asset.name} ({asset.asset_type})
                </option>
              ))}
            </select>
            {errors.asset_id && <span className="error-message">{errors.asset_id}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="transaction_type">Action Type *</label>
            <select
              id="transaction_type"
              name="transaction_type"
              value={formData.transaction_type}
              onChange={handleChange}
              className={errors.transaction_type ? 'error' : ''}
            >
              <option value="DEPOSIT">Depositing in locker</option>
              <option value="WITHDRAW">Withdrawing from locker</option>
              <option value="PERMANENTLY_REMOVE">Permanently remove</option>
            </select>
            {errors.transaction_type && <span className="error-message">{errors.transaction_type}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="reason">Reason</label>
            <textarea
              id="reason"
              name="reason"
              value={formData.reason}
              onChange={handleChange}
              rows="3"
              placeholder="Reason for this transaction"
            />
          </div>

          <div className="form-group">
            <label htmlFor="responsible_person">Who is Responsible</label>
            <input
              type="text"
              id="responsible_person"
              name="responsible_person"
              value={formData.responsible_person}
              onChange={handleChange}
              placeholder="Name of responsible person"
            />
          </div>

          <div className="form-group">
            <label htmlFor="transaction_date">Transaction Date *</label>
            <input
              type="date"
              id="transaction_date"
              name="transaction_date"
              value={formData.transaction_date}
              onChange={handleChange}
              className={errors.transaction_date ? 'error' : ''}
            />
            {errors.transaction_date && <span className="error-message">{errors.transaction_date}</span>}
          </div>

          <div className="modal-actions">
            <button type="button" onClick={onClose} className="cancel-button">
              Cancel
            </button>
            <button type="submit" className="save-button">
              {isEditing ? 'Update Transaction' : 'Create Transaction'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default TransactionModal;

