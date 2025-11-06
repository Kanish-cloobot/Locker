/**
 * Transaction ledger page - displays all transactions for a locker.
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import TransactionService from '../presenters/transactionService';
import AssetService from '../presenters/assetService';
import TransactionModal from './TransactionModal';
import ConfirmationModal from './ConfirmationModal';
import '../styles/TransactionLedgerPage.css';

function TransactionLedgerPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [transactions, setTransactions] = useState([]);
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showTransactionModal, setShowTransactionModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [editingTransaction, setEditingTransaction] = useState(null);
  const [transactionToDelete, setTransactionToDelete] = useState(null);
  const [filterAssetId, setFilterAssetId] = useState('');
  const [filterAssetType, setFilterAssetType] = useState('');

  useEffect(() => {
    loadData();
  }, [id]);

  useEffect(() => {
    applyFilters();
  }, [filterAssetId, filterAssetType]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [transactionsData, assetsData] = await Promise.all([
        TransactionService.getTransactionsByLocker(id),
        AssetService.getAssetsByLocker(id)
      ]);
      setTransactions(transactionsData);
      setAssets(assetsData);
      setError(null);
    } catch (err) {
      setError('Failed to load transaction data. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = async () => {
    try {
      let filteredTransactions;
      if (filterAssetId) {
        filteredTransactions = await TransactionService.filterTransactions(id, filterAssetId, null);
      } else if (filterAssetType) {
        filteredTransactions = await TransactionService.filterTransactions(id, null, filterAssetType);
      } else {
        filteredTransactions = await TransactionService.getTransactionsByLocker(id);
      }
      setTransactions(filteredTransactions);
    } catch (err) {
      console.error('Error filtering transactions:', err);
    }
  };

  const handleCreateTransaction = async (transactionData) => {
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

  const handleEditTransaction = (transaction) => {
    setEditingTransaction(transaction);
    setShowTransactionModal(true);
  };

  const handleDeleteTransaction = (transactionId) => {
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

  const handleCloseTransactionModal = () => {
    setShowTransactionModal(false);
    setEditingTransaction(null);
  };

  const clearFilters = () => {
    setFilterAssetId('');
    setFilterAssetType('');
  };

  const getTransactionTypeLabel = (type) => {
    const labels = {
      'DEPOSIT': 'Deposit',
      'WITHDRAW': 'Withdraw',
      'PERMANENTLY_REMOVE': 'Permanently Remove'
    };
    return labels[type] || type;
  };

  if (loading) {
    return <div className="loading-container">Loading transactions...</div>;
  }

  return (
    <div className="transaction-ledger-page">
      <div className="transaction-ledger-header">
        <button className="back-button" onClick={() => navigate(`/locker/${id}`)}>
          ← Back
        </button>
        <h1>Transaction Ledger</h1>
        <button 
          className="create-transaction-button"
          onClick={() => setShowTransactionModal(true)}
        >
          + Add Transaction
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="filters-section">
        <div className="filter-group">
          <label htmlFor="filter-asset">Filter by Asset:</label>
          <select
            id="filter-asset"
            value={filterAssetId}
            onChange={(e) => {
              setFilterAssetId(e.target.value);
              setFilterAssetType('');
            }}
          >
            <option value="">All Assets</option>
            {assets.map(asset => (
              <option key={asset.id} value={asset.id}>
                {asset.name}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label htmlFor="filter-asset-type">Filter by Asset Type:</label>
          <select
            id="filter-asset-type"
            value={filterAssetType}
            onChange={(e) => {
              setFilterAssetType(e.target.value);
              setFilterAssetId('');
            }}
          >
            <option value="">All Types</option>
            <option value="JEWELLERY">Jewellery</option>
            <option value="DOCUMENT">Document</option>
            <option value="MISC">Miscellaneous</option>
          </select>
        </div>

        {(filterAssetId || filterAssetType) && (
          <button className="clear-filters-button" onClick={clearFilters}>
            Clear Filters
          </button>
        )}
      </div>

      <div className="transactions-table-container">
        {transactions.length === 0 ? (
          <div className="empty-state">
            <p>No transactions found. Add your first transaction!</p>
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
                  <td>{transaction.transaction_date ? transaction.transaction_date.split(' ')[0] : '-'}</td>
                  <td>{transaction.asset_name || '-'}</td>
                  <td>
                    <span className={`asset-type-badge ${transaction.asset_type ? transaction.asset_type.toLowerCase() : ''}`}>
                      {transaction.asset_type || '-'}
                    </span>
                  </td>
                  <td>{getTransactionTypeLabel(transaction.transaction_type)}</td>
                  <td>{transaction.reason || '-'}</td>
                  <td>{transaction.responsible_person || '-'}</td>
                  <td>
                    <div className="action-buttons">
                      <button 
                        className="edit-button"
                        onClick={() => handleEditTransaction(transaction)}
                      >
                        Edit
                      </button>
                      <button 
                        className="delete-button"
                        onClick={() => handleDeleteTransaction(transaction.id)}
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
          onClose={handleCloseTransactionModal}
          onSave={handleCreateTransaction}
          transaction={editingTransaction}
          assets={assets}
          lockerId={parseInt(id)}
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

export default TransactionLedgerPage;

