/**
 * Locker service for API calls.
 */
import Locker from '../models/Locker';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class LockerService {
  /**
   * Get all lockers.
   */
  static async getAllLockers() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/lockers`);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.error || `Server returned ${response.status}: ${response.statusText}`;
        throw new Error(errorMessage);
      }
      const data = await response.json();
      return data.map(locker => new Locker(locker));
    } catch (error) {
      console.error('Error fetching lockers:', error);
      // Provide more specific error messages
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Unable to connect to server. Please ensure the backend server is running on http://localhost:5000');
      }
      throw error;
    }
  }

  /**
   * Get a locker by ID.
   */
  static async getLockerById(lockerId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/lockers/${lockerId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch locker');
      }
      const data = await response.json();
      return new Locker(data);
    } catch (error) {
      console.error('Error fetching locker:', error);
      throw error;
    }
  }

  /**
   * Create a new locker.
   */
  static async createLocker(lockerData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/lockers`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(lockerData),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to create locker');
      }
      const data = await response.json();
      return new Locker(data);
    } catch (error) {
      console.error('Error creating locker:', error);
      throw error;
    }
  }

  /**
   * Update an existing locker.
   */
  static async updateLocker(lockerId, lockerData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/lockers/${lockerId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(lockerData),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to update locker');
      }
      const data = await response.json();
      return new Locker(data);
    } catch (error) {
      console.error('Error updating locker:', error);
      throw error;
    }
  }

  /**
   * Delete a locker.
   */
  static async deleteLocker(lockerId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/lockers/${lockerId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to delete locker');
      }
      return true;
    } catch (error) {
      console.error('Error deleting locker:', error);
      throw error;
    }
  }

  /**
   * Get locker statistics (asset counts).
   */
  static async getLockerStats(lockerId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/lockers/${lockerId}/stats`);
      if (!response.ok) {
        throw new Error('Failed to fetch locker stats');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching locker stats:', error);
      throw error;
    }
  }
}

export default LockerService;

