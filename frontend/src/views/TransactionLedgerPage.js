/**
 * Transaction Ledger page - displays all transactions with filters.
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import TransactionService from '../presenters/transactionService';
import AssetService from '../presenters/assetService';
import ConfirmationModal from './ConfirmationModal';
import '../styles/TransactionLedgerPage.css';

function TransactionLedgerPage() {
  const navigate = useNavigate();
  const [transactions, setTransactions] = useState([]);
  const [allAssets, setAllAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    asset_id: '',
    asset_type: ''
  });
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [transactionToDelete, setTransactionToDelete] = useState(null);
  const [editingTransaction, setEditingTransaction] = useState(null);
  const [showTransactionModal, setShowTransactionModal] = useState(false);

  useEffect(() => {
    loadData();
  }, [filters]);

  const loadAllAssets = async () => {
    try {
      // Get all lockers first, then get assets from each
      const lockersResponse = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:5000'}/api/lockers`);
      const lockers = await lockersResponse.json();
      const allAssetsList = [];
      
      for (const locker of lockers) {
        try {
          const assets = await AssetService.getAssetsByLocker(locker.id);
          allAssetsList.push(...assets);
        } catch (err) {
          console.error(`Failed to load assets for locker ${locker.id}:`, err);
        }
      }
      
      setAllAssets(allAssetsList);
    } catch (err) {
      console.error('Error loading all assets:', err);
    }
  };

  const loadData = async () => {
    try {
      setLoading(true);
      const transactionsData = await TransactionService.getAllTransactions(filters);
      setTransactions(transactionsData);
      setError(null);
    } catch (err) {
      setError('Failed to load transactions. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllAssets();
  }, []);

  useEffect(() => {
    loadData();
  }, [filters]);

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleDeleteClick = (transactionId) => {
    setTransactionToDelete(transactionId);
    setShowDeleteModal(true);
  };

  const handleConfirmDelete = async () => {
    if (transactionToDelete) {
      try {
        await TransactionService.deleteTransaction(transactionToDelete);
        setShowDeleteModal(false);
        setTransactionToDelete(null);
        loadData();
      } catch (err) {
        alert('Failed to delete transaction: ' + err.message);
        setShowDeleteModal(false);
        setTransactionToDelete(null);
      }
    }
  };

  const handleCancelDelete = () => {
    setShowDeleteModal(false);
    setTransactionToDelete(null);
  };

  const handleEditClick = (transaction) => {
    setEditingTransaction(transaction);
    setShowTransactionModal(true);
  };

  const handleSaveTransaction = async (transactionData) => {
    try {
      if (editingTransaction) {
        await TransactionService.updateTransaction(editingTransaction.id, transactionData);
      } else {
        await TransactionService.createTransaction(transactionData);
      }
      setShowTransactionModal(false);
      setEditingTransaction(null);
      loadData();
    } catch (err) {
      alert('Failed to save transaction: ' + err.message);
    }
  };

  const getTransactionTypeLabel = (type) => {
    const labels = {
      'DEPOSIT': 'Deposited',
      'WITHDRAW': 'Withdrawn',
      'PERMANENT_REMOVE': 'Permanently Removed'
    };
    return labels[type] || type;
  };

  if (loading) {
    return <div className="loading-container">Loading transactions...</div>;
  }

  return (
    <div className="transaction-ledger-page">
      <div className="transaction-ledger-header">
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back
        </button>
        <h1>Transaction Ledger</h1>
        <button 
          className="create-transaction-button"
          onClick={() => {
            setEditingTransaction(null);
            setShowTransactionModal(true);
          }}
        >
          + Add Transaction
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="filters-section">
        <div className="filter-group">
          <label>Filter by Asset:</label>
          <select 
            value={filters.asset_id} 
            onChange={(e) => handleFilterChange('asset_id', e.target.value)}
          >
            <option value="">All Assets</option>
            {allAssets.map(asset => (
              <option key={asset.id} value={asset.id}>{asset.name}</option>
            ))}
          </select>
        </div>
        <div className="filter-group">
          <label>Filter by Asset Type:</label>
          <select 
            value={filters.asset_type} 
            onChange={(e) => handleFilterChange('asset_type', e.target.value)}
          >
            <option value="">All Types</option>
            <option value="JEWELLERY">Jewellery</option>
            <option value="DOCUMENT">Document</option>
            <option value="MISC">Miscellaneous</option>
          </select>
        </div>
      </div>

      <div className="transactions-table-container">
        {transactions.length === 0 ? (
          <div className="empty-state">
            <p>No transactions found.</p>
          </div>
        ) : (
          <table className="transactions-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Asset Name</th>
                <th>Asset Type</th>
                <th>Transaction Type</th>
                <th>Reason</th>
                <th>Responsible Person</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map(transaction => (
                <tr key={transaction.id}>
                  <td>{new Date(transaction.created_at).toLocaleString()}</td>
                  <td>{transaction.asset_name || 'N/A'}</td>
                  <td>
                    <span className={`asset-type-badge ${(transaction.asset_type || '').toLowerCase()}`}>
                      {transaction.asset_type || 'N/A'}
                    </span>
                  </td>
                  <td>
                    <span className={`transaction-type-badge ${transaction.transaction_type.toLowerCase()}`}>
                      {getTransactionTypeLabel(transaction.transaction_type)}
                    </span>
                  </td>
                  <td>{transaction.reason || '-'}</td>
                  <td>{transaction.responsible_person || '-'}</td>
                  <td>
                    <div className="action-buttons">
                      <button 
                        className="edit-button"
                        onClick={() => handleEditClick(transaction)}
                      >
                        Edit
                      </button>
                      <button 
                        className="delete-button"
                        onClick={() => handleDeleteClick(transaction.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {showTransactionModal && (
        <TransactionModal
          transaction={editingTransaction}
          assets={allAssets}
          onClose={() => {
            setShowTransactionModal(false);
            setEditingTransaction(null);
          }}
          onSave={handleSaveTransaction}
        />
      )}

      <ConfirmationModal
        isOpen={showDeleteModal}
        onClose={handleCancelDelete}
        onConfirm={handleConfirmDelete}
        title="Delete Transaction"
        message="Are you sure you want to delete this transaction? This action cannot be undone."
        confirmText="Delete"
        cancelText="Cancel"
      />
    </div>
  );
}

function TransactionModal({ transaction, assets, onClose, onSave }) {
  const [formData, setFormData] = useState({
    asset_id: transaction?.asset_id || '',
    transaction_type: transaction?.transaction_type || 'DEPOSIT',
    reason: transaction?.reason || '',
    responsible_person: transaction?.responsible_person || ''
  });

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.asset_id || !formData.transaction_type) {
      alert('Please fill in all required fields');
      return;
    }
    onSave(formData);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{transaction ? 'Edit Transaction' : 'Create Transaction'}</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit} className="transaction-form">
          <div className="form-group">
            <label>Linked Asset *</label>
            <select 
              value={formData.asset_id} 
              onChange={(e) => handleChange('asset_id', e.target.value)}
              required
            >
              <option value="">Select Asset</option>
              {assets.map(asset => (
                <option key={asset.id} value={asset.id}>
                  {asset.name} ({asset.asset_type})
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Transaction Type *</label>
            <select 
              value={formData.transaction_type} 
              onChange={(e) => handleChange('transaction_type', e.target.value)}
              required
            >
              <option value="DEPOSIT">Depositing in Locker</option>
              <option value="WITHDRAW">Withdrawing from Locker</option>
              <option value="PERMANENT_REMOVE">Permanently Remove</option>
            </select>
          </div>
          <div className="form-group">
            <label>Reason</label>
            <textarea 
              value={formData.reason} 
              onChange={(e) => handleChange('reason', e.target.value)}
              rows="3"
            />
          </div>
          <div className="form-group">
            <label>Responsible Person</label>
            <input 
              type="text"
              value={formData.responsible_person} 
              onChange={(e) => handleChange('responsible_person', e.target.value)}
            />
          </div>
          <div className="modal-actions">
            <button type="button" onClick={onClose}>Cancel</button>
            <button type="submit">Save</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default TransactionLedgerPage;

