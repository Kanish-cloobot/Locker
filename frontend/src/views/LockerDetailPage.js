/**
 * Locker detail page - displays locker info and assets.
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import LockerService from '../presenters/lockerService';
import AssetService from '../presenters/assetService';
import AssetModal from './AssetModal';
import EditLockerModal from './EditLockerModal';
import ConfirmationModal from './ConfirmationModal';
import '../styles/LockerDetailPage.css';

function LockerDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [locker, setLocker] = useState(null);
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAssetModal, setShowAssetModal] = useState(false);
  const [showEditLockerModal, setShowEditLockerModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [assetToDelete, setAssetToDelete] = useState(null);
  const [editingAsset, setEditingAsset] = useState(null);

  useEffect(() => {
    loadData();
  }, [id]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [lockerData, assetsData] = await Promise.all([
        LockerService.getLockerById(id),
        AssetService.getAssetsByLocker(id)
      ]);
      setLocker(lockerData);
      setAssets(assetsData);
      setError(null);
    } catch (err) {
      setError('Failed to load locker data. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAsset = async (assetData) => {
    try {
      await AssetService.createAsset(id, assetData);
      setShowAssetModal(false);
      loadData();
    } catch (err) {
      alert('Failed to create asset: ' + err.message);
    }
  };

  const handleUpdateAsset = async (assetId, assetData) => {
    try {
      await AssetService.updateAsset(assetId, assetData);
      setShowAssetModal(false);
      setEditingAsset(null);
      loadData();
    } catch (err) {
      alert('Failed to update asset: ' + err.message);
    }
  };

  const handleDeleteAsset = (assetId) => {
    setAssetToDelete(assetId);
    setShowDeleteModal(true);
  };

  const handleConfirmDelete = async () => {
    if (assetToDelete) {
      try {
        await AssetService.deleteAsset(assetToDelete);
        setShowDeleteModal(false);
        setAssetToDelete(null);
        loadData();
      } catch (err) {
        alert('Failed to delete asset: ' + err.message);
        setShowDeleteModal(false);
        setAssetToDelete(null);
      }
    }
  };

  const handleCancelDelete = () => {
    setShowDeleteModal(false);
    setAssetToDelete(null);
  };

  const handleEditAsset = (asset) => {
    setEditingAsset(asset);
    setShowAssetModal(true);
  };

  const handleUpdateLocker = async (lockerData) => {
    try {
      await LockerService.updateLocker(id, lockerData);
      setShowEditLockerModal(false);
      loadData();
    } catch (err) {
      alert('Failed to update locker: ' + err.message);
    }
  };

  const handleCloseAssetModal = () => {
    setShowAssetModal(false);
    setEditingAsset(null);
  };

  if (loading) {
    return <div className="loading-container">Loading locker details...</div>;
  }

  if (error || !locker) {
    return (
      <div className="error-container">
        <p>{error || 'Locker not found'}</p>
        <button onClick={() => navigate('/')}>Back to Home</button>
      </div>
    );
  }

  return (
    <div className="locker-detail-page">
      <div className="locker-detail-header">
        <button className="back-button" onClick={() => navigate('/')}>
          ← Back
        </button>
        <div className="locker-info">
          <h1>{locker.name}</h1>
          <p className="location-name">{locker.location_name}</p>
          <p className="address">{locker.address}</p>
        </div>
        <button 
          className="edit-locker-button"
          onClick={() => setShowEditLockerModal(true)}
        >
          Edit Locker
        </button>
      </div>

      <div className="assets-section">
        <div className="assets-header">
          <h2>Assets ({assets.length})</h2>
          <button 
            className="create-asset-button"
            onClick={() => setShowAssetModal(true)}
          >
            + Add Asset
          </button>
        </div>

        {assets.length === 0 ? (
          <div className="empty-state">
            <p>No assets in this locker. Add your first asset!</p>
          </div>
        ) : (
          <div className="assets-table-container">
            <table className="assets-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Type</th>
                  <th>Worth</th>
                  <th>Creation Date</th>
                  <th>Details</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {assets.map(asset => (
                  <tr key={asset.id}>
                    <td>{asset.name}</td>
                    <td>
                      <span className={`asset-type-badge ${asset.asset_type.toLowerCase()}`}>
                        {asset.asset_type}
                      </span>
                    </td>
                    <td>
                      {asset.worth_on_creation 
                        ? `$${parseFloat(asset.worth_on_creation).toFixed(2)}` 
                        : '-'}
                    </td>
                    <td>{asset.creation_date || '-'}</td>
                    <td className="asset-details-cell">
                      {asset.asset_type === 'JEWELLERY' && asset.jewellery_details && (
                        <div>
                          <strong>Material:</strong> {asset.jewellery_details.material_type || 'N/A'}
                          {asset.jewellery_details.material_grade && (
                            <span> ({asset.jewellery_details.material_grade})</span>
                          )}
                        </div>
                      )}
                      {asset.asset_type === 'DOCUMENT' && asset.document_details && (
                        <div>
                          <strong>Type:</strong> {asset.document_details.document_type || 'N/A'}
                        </div>
                      )}
                      {asset.details && (
                        <div className="asset-notes">{asset.details}</div>
                      )}
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button 
                          className="edit-button"
                          onClick={() => handleEditAsset(asset)}
                        >
                          Edit
                        </button>
                        <button 
                          className="delete-button"
                          onClick={() => handleDeleteAsset(asset.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {showAssetModal && (
        <AssetModal
          onClose={handleCloseAssetModal}
          onSave={editingAsset 
            ? (data) => handleUpdateAsset(editingAsset.id, data)
            : handleCreateAsset}
          asset={editingAsset}
        />
      )}

      {showEditLockerModal && (
        <EditLockerModal
          locker={locker}
          onClose={() => setShowEditLockerModal(false)}
          onSave={handleUpdateLocker}
        />
      )}

      <ConfirmationModal
        isOpen={showDeleteModal}
        onClose={handleCancelDelete}
        onConfirm={handleConfirmDelete}
        title="Delete Asset"
        message="Are you sure you want to delete this asset? This action cannot be undone."
        confirmText="Delete"
        cancelText="Cancel"
      />
    </div>
  );
}

export default LockerDetailPage;

