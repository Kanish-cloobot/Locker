/**
 * Home page component - displays all lockers as cards.
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import LockerService from '../presenters/lockerService';
import CreateLockerModal from './CreateLockerModal';
import ConfirmationModal from './ConfirmationModal';
import '../styles/HomePage.css';

function HomePage() {
  const [lockers, setLockers] = useState([]);
  const [lockersWithStats, setLockersWithStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [lockerToDelete, setLockerToDelete] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadLockers();
  }, []);

  const loadLockers = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await LockerService.getAllLockers();
      setLockers(data);
      
      // Fetch stats for each locker
      const lockersWithStatsData = await Promise.all(
        data.map(async (locker) => {
          try {
            const stats = await LockerService.getLockerStats(locker.id);
            return { ...locker, stats };
          } catch (err) {
            console.error(`Error loading stats for locker ${locker.id}:`, err);
            return { ...locker, stats: { total_assets: 0, withdrawn_count: 0 } };
          }
        })
      );
      setLockersWithStats(lockersWithStatsData);
    } catch (err) {
      const errorMessage = err.message || 'Failed to load lockers. Please try again.';
      setError(errorMessage);
      console.error('Error loading lockers:', err);
    } finally {
      setLoading(false);
    }
  };
  
  // Organize lockers into two sections
  const lockersWithWithdrawn = lockersWithStats.filter(locker => locker.stats && locker.stats.withdrawn_count > 0);
  const lockersIntact = lockersWithStats.filter(locker => !locker.stats || locker.stats.withdrawn_count === 0);

  const handleCreateLocker = async (lockerData) => {
    try {
      await LockerService.createLocker(lockerData);
      setShowCreateModal(false);
      loadLockers();
    } catch (err) {
      alert('Failed to create locker: ' + err.message);
    }
  };

  const handleDeleteClick = (lockerId, event) => {
    event.stopPropagation();
    setLockerToDelete(lockerId);
    setShowDeleteModal(true);
  };

  const handleConfirmDelete = async () => {
    if (lockerToDelete) {
      try {
        await LockerService.deleteLocker(lockerToDelete);
        setShowDeleteModal(false);
        setLockerToDelete(null);
        loadLockers();
      } catch (err) {
        alert('Failed to delete locker: ' + err.message);
        setShowDeleteModal(false);
        setLockerToDelete(null);
      }
    }
  };

  const handleCancelDelete = () => {
    setShowDeleteModal(false);
    setLockerToDelete(null);
  };

  const handleLockerClick = (lockerId) => {
    navigate(`/locker/${lockerId}`);
  };

  if (loading) {
    return <div className="loading-container">Loading lockers...</div>;
  }

  return (
    <div className="home-page">
      <div className="home-header">
        <h1>Family Locker Organizer</h1>
        <button 
          className="create-locker-button"
          onClick={() => setShowCreateModal(true)}
        >
          + Create New Locker
        </button>
      </div>

      {error && (
        <div className="error-container">
          <div className="error-message">{error}</div>
          <button 
            className="retry-button"
            onClick={loadLockers}
            disabled={loading}
          >
            {loading ? 'Retrying...' : 'Retry'}
          </button>
        </div>
      )}

      {lockers.length === 0 ? (
        <div className="empty-state">
          <p>No lockers found. Create your first locker to get started!</p>
        </div>
      ) : (
        <>
          {lockersWithWithdrawn.length > 0 && (
            <div className="lockers-section">
              <h2 className="section-title">Lockers with withdrawn assets</h2>
              <div className="lockers-grid">
                {lockersWithWithdrawn.map(locker => (
                  <div 
                    key={locker.id} 
                    className="locker-card"
                    onClick={() => handleLockerClick(locker.id)}
                  >
                    <div className="locker-card-header">
                      <h2>{locker.name}</h2>
                      <button
                        className="delete-button"
                        onClick={(e) => handleDeleteClick(locker.id, e)}
                        title="Delete locker"
                      >
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                      </button>
                    </div>
                    <div className="locker-card-body">
                      <p className="location-name">{locker.location_name}</p>
                      <p className="address">{locker.address}</p>
                      {locker.stats && (
                        <p className="asset-count">
                          {locker.stats.withdrawn_count} withdrawn / {locker.stats.total_assets} total
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {lockersIntact.length > 0 && (
            <div className="lockers-section">
              <h2 className="section-title">Lockers with all assets intact</h2>
              <div className="lockers-grid">
                {lockersIntact.map(locker => (
                  <div 
                    key={locker.id} 
                    className="locker-card"
                    onClick={() => handleLockerClick(locker.id)}
                  >
                    <div className="locker-card-header">
                      <h2>{locker.name}</h2>
                      <button
                        className="delete-button"
                        onClick={(e) => handleDeleteClick(locker.id, e)}
                        title="Delete locker"
                      >
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                      </button>
                    </div>
                    <div className="locker-card-body">
                      <p className="location-name">{locker.location_name}</p>
                      <p className="address">{locker.address}</p>
                      {locker.stats && (
                        <p className="asset-count">
                          {locker.stats.withdrawn_count} withdrawn / {locker.stats.total_assets} total
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {showCreateModal && (
        <CreateLockerModal
          onClose={() => setShowCreateModal(false)}
          onSave={handleCreateLocker}
        />
      )}

      <ConfirmationModal
        isOpen={showDeleteModal}
        onClose={handleCancelDelete}
        onConfirm={handleConfirmDelete}
        title="Delete Locker"
        message="Are you sure you want to delete this locker? All associated assets will also be permanently deleted. This action cannot be undone."
        confirmText="Delete"
        cancelText="Cancel"
      />
    </div>
  );
}

export default HomePage;

