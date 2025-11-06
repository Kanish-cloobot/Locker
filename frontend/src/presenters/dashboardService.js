/**
 * Dashboard service for API calls.
 */
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class DashboardService {
  /**
   * Get dashboard statistics.
   */
  static async getDashboardStats() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/dashboard`);
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

