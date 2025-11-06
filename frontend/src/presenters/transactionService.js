/**
 * Transaction service for API calls.
 */
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class TransactionService {
  /**
   * Get all transactions with optional filters.
   */
  static async getAllTransactions(filters = {}) {
    try {
      const params = new URLSearchParams();
      if (filters.asset_id) params.append('asset_id', filters.asset_id);
      if (filters.asset_type) params.append('asset_type', filters.asset_type);
      
      const url = `${API_BASE_URL}/api/transactions${params.toString() ? '?' + params.toString() : ''}`;
      const response = await fetch(url);
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
   * Get a transaction by ID.
   */
  static async getTransactionById(transactionId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/transactions/${transactionId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch transaction');
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching transaction:', error);
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
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error creating transaction:', error);
      throw error;
    }
  }

  /**
   * Update an existing transaction.
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
      const data = await response.json();
      return data;
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
      return true;
    } catch (error) {
      console.error('Error deleting transaction:', error);
      throw error;
    }
  }

  /**
   * Get recent transactions.
   */
  static async getRecentTransactions(limit = 10) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/transactions/recent?limit=${limit}`);
      if (!response.ok) {
        throw new Error('Failed to fetch recent transactions');
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching recent transactions:', error);
      throw error;
    }
  }
}

export default TransactionService;

