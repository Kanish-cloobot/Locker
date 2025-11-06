/**
 * Transaction service for API calls.
 */
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class TransactionService {
  /**
   * Get all transactions for a locker.
   */
  static async getTransactionsByLocker(lockerId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/lockers/${lockerId}/transactions`);
      if (!response.ok) {
        throw new Error('Failed to fetch transactions');
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching transactions:', error);
      throw error;
    }
  }

  /**
   * Create a new transaction.
   */
  static async createTransaction(transactionData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/transactions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(transactionData),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to create transaction');
      }
      return await response.json();
    } catch (error) {
      console.error('Error creating transaction:', error);
      throw error;
    }
  }

  /**
   * Update a transaction.
   */
  static async updateTransaction(transactionId, transactionData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/transactions/${transactionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(transactionData),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to update transaction');
      }
      return await response.json();
    } catch (error) {
      console.error('Error updating transaction:', error);
      throw error;
    }
  }

  /**
   * Delete a transaction.
   */
  static async deleteTransaction(transactionId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/transactions/${transactionId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to delete transaction');
      }
      return await response.json();
    } catch (error) {
      console.error('Error deleting transaction:', error);
      throw error;
    }
  }

  /**
   * Filter transactions.
   */
  static async filterTransactions(lockerId, assetId = null, assetType = null) {
    try {
      let url = `${API_BASE_URL}/api/lockers/${lockerId}/transactions/filter?`;
      if (assetId) {
        url += `asset_id=${assetId}`;
      } else if (assetType) {
        url += `asset_type=${assetType}`;
      }
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Failed to filter transactions');
      }
      return await response.json();
    } catch (error) {
      console.error('Error filtering transactions:', error);
      throw error;
    }
  }

  /**
   * Get dashboard data.
   */
  static async getDashboardData(lockerId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/lockers/${lockerId}/dashboard`);
      if (!response.ok) {
        throw new Error('Failed to fetch dashboard data');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      throw error;
    }
  }
}

export default TransactionService;

