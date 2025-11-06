/**
 * Locker Dashboard page - displays statistics and recent transactions.
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DashboardService from '../presenters/dashboardService';
import '../styles/LockerDashboardPage.css';

function LockerDashboardPage() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const data = await DashboardService.getDashboardStats();
      setStats(data);
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
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
    return <div className="loading-container">Loading dashboard...</div>;
  }

  if (error || !stats) {
    return (
      <div className="error-container">
        <p>{error || 'Failed to load dashboard'}</p>
        <button onClick={() => navigate('/')}>Back to Home</button>
      </div>
    );
  }

  return (
    <div className="locker-dashboard-page">
      <div className="dashboard-header">
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back
        </button>
        <h1>Locker Dashboard</h1>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Total Assets Deposited</div>
          <div className="stat-value">{stats.total_deposited || 0}</div>
          <div className="stat-description">Including withdrawn assets</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Assets Currently in Locker</div>
          <div className="stat-value">{stats.current_in_locker || 0}</div>
          <div className="stat-description">Not withdrawn or removed</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Assets Withdrawn</div>
          <div className="stat-value">{stats.withdrawn || 0}</div>
          <div className="stat-description">As on date</div>
        </div>
      </div>

      <div className="recent-transactions-section">
        <h2>Last 10 Transactions</h2>
        {stats.recent_transactions && stats.recent_transactions.length > 0 ? (
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
                {stats.recent_transactions.map(transaction => (
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
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <p>No transactions found.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default LockerDashboardPage;

