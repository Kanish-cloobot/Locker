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
      const data = await LockerService.getAllLockers();
      setLockers(data);
      setError(null);
    } catch (err) {
      setError('Failed to load lockers. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

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
        <div className="header-actions">
          <button 
            className="nav-button"
            onClick={() => navigate('/dashboard')}
          >
            Dashboard
          </button>
          <button 
            className="nav-button"
            onClick={() => navigate('/transactions')}
          >
            Transactions
          </button>
          <button 
            className="create-locker-button"
            onClick={() => setShowCreateModal(true)}
          >
            + Create New Locker
          </button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {lockers.length === 0 ? (
        <div className="empty-state">
          <p>No lockers found. Create your first locker to get started!</p>
        </div>
      ) : (
        <>
          {lockers.filter(l => (l.withdrawn_assets || 0) > 0).length > 0 && (
            <div className="lockers-section">
              <h2 className="section-title">Lockers with Withdrawn Assets</h2>
              <div className="lockers-grid">
                {lockers
                  .filter(locker => (locker.withdrawn_assets || 0) > 0)
                  .map(locker => (
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
                        <div className="asset-counts">
                          <span className="asset-count-text">
                            Assets: {locker.withdrawn_assets || 0} withdrawn / {locker.total_assets || 0} total
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          )}

          {lockers.filter(l => (l.withdrawn_assets || 0) === 0).length > 0 && (
            <div className="lockers-section">
              <h2 className="section-title">Lockers with All Assets Intact</h2>
              <div className="lockers-grid">
                {lockers
                  .filter(locker => (locker.withdrawn_assets || 0) === 0)
                  .map(locker => (
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
                        <div className="asset-counts">
                          <span className="asset-count-text">
                            Assets: {locker.withdrawn_assets || 0} withdrawn / {locker.total_assets || 0} total
                          </span>
                        </div>
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

