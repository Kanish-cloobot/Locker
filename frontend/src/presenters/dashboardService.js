/**
 * Dashboard service for API calls.
 */
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class DashboardService {
  /**
   * Get dashboard statistics for a specific locker.
   * @param {number} lockerId - The locker ID (required)
   */
  static async getDashboardStats(lockerId) {
    if (!lockerId) {
      throw new Error('Locker ID is required');
    }
    try {
      const url = `${API_BASE_URL}/api/lockers/${lockerId}/dashboard`;
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Failed to fetch dashboard stats');
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      throw error;
    }
  }
}

export default DashboardService;

