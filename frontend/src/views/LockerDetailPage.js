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
import EditLogModal from './EditLogModal';
import FileService from '../presenters/fileService';
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
  const [showEditLogModal, setShowEditLogModal] = useState(false);
  const [selectedAssetForLogs, setSelectedAssetForLogs] = useState(null);

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
      const newAsset = await AssetService.createAsset(id, assetData);
      // Reload to get full asset data including files
      await loadData();
      // Open modal again with the new asset for file upload
      const updatedAssets = await AssetService.getAssetsByLocker(id);
      const createdAsset = updatedAssets.find(a => a.id === newAsset.id);
      if (createdAsset) {
        setEditingAsset(createdAsset);
        setShowAssetModal(true);
      } else {
        setShowAssetModal(false);
      }
    } catch (err) {
      alert('Failed to create asset: ' + err.message);
      setShowAssetModal(false);
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
                  <th>Preview</th>
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
                    <td>
                      {asset.thumbnail ? (
                        asset.thumbnail.file_type === 'PDF' ? (
                          <div 
                            className="asset-pdf-preview"
                            title={`PDF: ${asset.thumbnail.original_file_name || 'Document'}`}
                            onClick={() => window.open(FileService.getFileUrl(asset.thumbnail.id), '_blank')}
                          >
                            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="#e74c3c" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                              <path d="M14 2V8H20" stroke="#e74c3c" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                              <path d="M16 13H8" stroke="#e74c3c" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                              <path d="M16 17H8" stroke="#e74c3c" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                              <path d="M10 9H9H8" stroke="#e74c3c" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                            </svg>
                            <span>PDF</span>
                          </div>
                        ) : (
                          <>
                            <img 
                              src={
                                asset.thumbnail.thumbnail_path 
                                  ? FileService.getThumbnailUrl(asset.thumbnail.id)
                                  : FileService.getFileUrl(asset.thumbnail.id)
                              }
                              alt={asset.name}
                              className="asset-thumbnail"
                              onError={(e) => {
                                // Hide image and show placeholder
                                e.target.style.display = 'none';
                                const placeholder = e.target.parentElement.querySelector('.asset-thumbnail-placeholder');
                                if (placeholder) {
                                  placeholder.style.display = 'flex';
                                }
                              }}
                            />
                            <div 
                              className="asset-thumbnail-placeholder" 
                              style={{ display: 'none' }}
                            >
                              No Image
                            </div>
                          </>
                        )
                      ) : (
                        <div 
                          className="asset-thumbnail-placeholder" 
                          style={{ display: 'flex' }}
                        >
                          No Image
                        </div>
                      )}
                    </td>
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
                        <button 
                          className="history-button"
                          onClick={() => {
                            setSelectedAssetForLogs(asset);
                            setShowEditLogModal(true);
                          }}
                          title="View Edit History"
                        >
                          History
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

      {showEditLogModal && selectedAssetForLogs && (
        <EditLogModal
          isOpen={showEditLogModal}
          onClose={() => {
            setShowEditLogModal(false);
            setSelectedAssetForLogs(null);
          }}
          editLogs={selectedAssetForLogs.edit_logs || []}
          assetName={selectedAssetForLogs.name}
        />
      )}
    </div>
  );
}

export default LockerDetailPage;

