/**
 * Home page component - displays all lockers as cards.
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import LockerService from '../presenters/lockerService';
import CreateLockerModal from './CreateLockerModal';
import '../styles/HomePage.css';

function HomePage() {
  const [lockers, setLockers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
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

  const handleDeleteLocker = async (lockerId, event) => {
    event.stopPropagation();
    if (window.confirm('Are you sure you want to delete this locker? All associated assets will also be deleted.')) {
      try {
        await LockerService.deleteLocker(lockerId);
        loadLockers();
      } catch (err) {
        alert('Failed to delete locker: ' + err.message);
      }
    }
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

      {error && <div className="error-message">{error}</div>}

      <div className="lockers-grid">
        {lockers.length === 0 ? (
          <div className="empty-state">
            <p>No lockers found. Create your first locker to get started!</p>
          </div>
        ) : (
          lockers.map(locker => (
            <div 
              key={locker.id} 
              className="locker-card"
              onClick={() => handleLockerClick(locker.id)}
            >
              <div className="locker-card-header">
                <h2>{locker.name}</h2>
                <button
                  className="delete-button"
                  onClick={(e) => handleDeleteLocker(locker.id, e)}
                  title="Delete locker"
                >
                  ×
                </button>
              </div>
              <div className="locker-card-body">
                <p className="location-name">{locker.location_name}</p>
                <p className="address">{locker.address}</p>
              </div>
            </div>
          ))
        )}
      </div>

      {showCreateModal && (
        <CreateLockerModal
          onClose={() => setShowCreateModal(false)}
          onSave={handleCreateLocker}
        />
      )}
    </div>
  );
}

export default HomePage;

