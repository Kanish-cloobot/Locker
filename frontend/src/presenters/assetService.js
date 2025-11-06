/**
 * Asset service for API calls.
 */
import Asset from '../models/Asset';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class AssetService {
  /**
   * Get all assets for a locker.
   */
  static async getAssetsByLocker(lockerId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/lockers/${lockerId}/assets`);
      if (!response.ok) {
        throw new Error('Failed to fetch assets');
      }
      const data = await response.json();
      return data.map(asset => new Asset(asset));
    } catch (error) {
      console.error('Error fetching assets:', error);
      throw error;
    }
  }

  /**
   * Create a new asset.
   */
  static async createAsset(lockerId, assetData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/lockers/${lockerId}/assets`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(assetData),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to create asset');
      }
      const data = await response.json();
      return new Asset(data);
    } catch (error) {
      console.error('Error creating asset:', error);
      throw error;
    }
  }

  /**
   * Update an existing asset.
   */
  static async updateAsset(assetId, assetData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/assets/${assetId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(assetData),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to update asset');
      }
      const data = await response.json();
      return new Asset(data);
    } catch (error) {
      console.error('Error updating asset:', error);
      throw error;
    }
  }

  /**
   * Delete an asset.
   */
  static async deleteAsset(assetId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/assets/${assetId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to delete asset');
      }
      return true;
    } catch (error) {
      console.error('Error deleting asset:', error);
      throw error;
    }
  }

  /**
   * Get edit history for an asset.
   */
  static async getEditHistory(assetId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/assets/${assetId}/edit-history`);
      if (!response.ok) {
        throw new Error('Failed to fetch edit history');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching edit history:', error);
      throw error;
    }
  }

  /**
   * Get files for an asset.
   */
  static async getAssetFiles(assetId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/assets/${assetId}/files`);
      if (!response.ok) {
        throw new Error('Failed to fetch asset files');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching asset files:', error);
      throw error;
    }
  }
}

export default AssetService;

