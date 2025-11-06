/**
 * Locker dashboard page - displays statistics and recent transactions.
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import TransactionService from '../presenters/transactionService';
import '../styles/LockerDashboardPage.css';

function LockerDashboardPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, [id]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const data = await TransactionService.getDashboardData(id);
      setDashboardData(data);
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard data. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
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
    return <div className="loading-container">Loading dashboard...</div>;
  }

  if (error || !dashboardData) {
    return (
      <div className="error-container">
        <p>{error || 'Dashboard data not found'}</p>
        <button onClick={() => navigate(`/locker/${id}`)}>Back to Locker</button>
      </div>
    );
  }

  const { stats, recent_transactions } = dashboardData;

  return (
    <div className="locker-dashboard-page">
      <div className="dashboard-header">
        <button className="back-button" onClick={() => navigate(`/locker/${id}`)}>
          ← Back
        </button>
        <h1>Locker Dashboard</h1>
        <button 
          className="view-transactions-button"
          onClick={() => navigate(`/locker/${id}/transactions`)}
        >
          View All Transactions
        </button>
      </div>

      <div className="stats-section">
        <div className="stat-card">
          <div className="stat-icon deposit">📦</div>
          <div className="stat-content">
            <h3>Total Deposited</h3>
            <p className="stat-value">{stats.total_deposited}</p>
            <p className="stat-label">Assets deposited (incl. withdrawn)</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon withdrawn">📤</div>
          <div className="stat-content">
            <h3>Withdrawn</h3>
            <p className="stat-value">{stats.withdrawn_count}</p>
            <p className="stat-label">Assets withdrawn as on date</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon in-locker">🔒</div>
          <div className="stat-content">
            <h3>Currently in Locker</h3>
            <p className="stat-value">{stats.currently_in_locker}</p>
            <p className="stat-label">Assets currently in locker</p>
          </div>
        </div>
      </div>

      <div className="recent-transactions-section">
        <h2>Last 10 Transactions</h2>
        {recent_transactions.length === 0 ? (
          <div className="empty-state">
            <p>No transactions found.</p>
          </div>
        ) : (
          <div className="transactions-table-container">
            <table className="transactions-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Asset Name</th>
                  <th>Asset Type</th>
                  <th>Transaction Type</th>
                  <th>Reason</th>
                </tr>
              </thead>
              <tbody>
                {recent_transactions.map(transaction => (
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
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default LockerDashboardPage;

