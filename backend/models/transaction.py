"""
Transaction model for database operations.
"""
from backend.database.db_setup import get_connection, get_timestamp


class TransactionModel:
    """Model class for Transaction table operations."""
    
    @staticmethod
    def create(asset_id, locker_id, transaction_type, reason=None, 
               responsible_person=None, transaction_date=None):
        """Create a new transaction."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        if transaction_date is None:
            transaction_date = timestamp
        cursor.execute('''
            INSERT INTO "Transaction" (asset_id, locker_id, transaction_type, 
                                   reason, responsible_person, transaction_date,
                                   status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
        ''', (asset_id, locker_id, transaction_type, reason, 
              responsible_person, transaction_date, timestamp, timestamp))
        transaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return transaction_id
    
    @staticmethod
    def get_by_locker_id(locker_id):
        """Get all active transactions for a specific locker."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.*, a.name as asset_name, a.asset_type
            FROM "Transaction" t
            JOIN Asset a ON t.asset_id = a.id
            WHERE t.locker_id = ? AND t.status = 'active'
            ORDER BY t.transaction_date DESC, t.created_at DESC
        ''', (locker_id,))
        transactions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return transactions
    
    @staticmethod
    def get_by_asset_id(asset_id):
        """Get all active transactions for a specific asset."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM "Transaction" 
            WHERE asset_id = ? AND status = 'active'
            ORDER BY transaction_date DESC, created_at DESC
        ''', (asset_id,))
        transactions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return transactions
    
    @staticmethod
    def get_by_id(transaction_id):
        """Get a transaction by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.*, a.name as asset_name, a.asset_type
            FROM "Transaction" t
            JOIN Asset a ON t.asset_id = a.id
            WHERE t.id = ? AND t.status = 'active'
        ''', (transaction_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def update(transaction_id, transaction_type=None, reason=None, 
               responsible_person=None, transaction_date=None):
        """Update an existing transaction."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        
        # Build dynamic update query
        updates = []
        params = []
        
        if transaction_type is not None:
            updates.append("transaction_type = ?")
            params.append(transaction_type)
        if reason is not None:
            updates.append("reason = ?")
            params.append(reason)
        if responsible_person is not None:
            updates.append("responsible_person = ?")
            params.append(responsible_person)
        if transaction_date is not None:
            updates.append("transaction_date = ?")
            params.append(transaction_date)
        
        if not updates:
            conn.close()
            return False
        
        updates.append("updated_at = ?")
        params.append(timestamp)
        params.append(transaction_id)
        
        query = f'UPDATE "Transaction" SET {", ".join(updates)} WHERE id = ? AND status = \'active\''
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @staticmethod
    def delete(transaction_id):
        """Soft delete a transaction."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            UPDATE "Transaction" 
            SET status = 'deleted', updated_at = ?
            WHERE id = ? AND status = 'active'
        ''', (timestamp, transaction_id))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @staticmethod
    def filter_by_asset(locker_id, asset_id):
        """Filter transactions by asset for a locker."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.*, a.name as asset_name, a.asset_type
            FROM "Transaction" t
            JOIN Asset a ON t.asset_id = a.id
            WHERE t.locker_id = ? AND t.asset_id = ? AND t.status = 'active'
            ORDER BY t.transaction_date DESC, t.created_at DESC
        ''', (locker_id, asset_id))
        transactions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return transactions
    
    @staticmethod
    def filter_by_asset_type(locker_id, asset_type):
        """Filter transactions by asset type for a locker."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.*, a.name as asset_name, a.asset_type
            FROM "Transaction" t
            JOIN Asset a ON t.asset_id = a.id
            WHERE t.locker_id = ? AND a.asset_type = ? AND t.status = 'active'
            ORDER BY t.transaction_date DESC, t.created_at DESC
        ''', (locker_id, asset_type))
        transactions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return transactions

