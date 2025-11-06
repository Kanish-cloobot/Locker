"""
Transaction model for database operations.
"""
from backend.database.db_setup import get_connection, get_timestamp


class TransactionModel:
    """Model class for Transaction table operations."""
    
    @staticmethod
    def get_all():
        """Get all active transactions ordered by created_at DESC."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.*, a.name as asset_name, a.asset_type 
            FROM "Transaction" t
            JOIN Asset a ON t.asset_id = a.id
            WHERE t.status = 'active'
            ORDER BY t.created_at DESC
        ''')
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
            ORDER BY created_at DESC
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
    def create(asset_id, transaction_type, reason=None, responsible_person=None, org_id=1, user_id=1):
        """Create a new transaction."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        cursor.execute('''
            INSERT INTO "Transaction" (asset_id, transaction_type, reason, responsible_person, 
                                  org_id, user_id, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
        ''', (asset_id, transaction_type, reason, responsible_person, org_id, user_id, timestamp, timestamp))
        transaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return transaction_id
    
    @staticmethod
    def update(transaction_id, transaction_type=None, reason=None, responsible_person=None):
        """Update an existing transaction."""
        conn = get_connection()
        cursor = conn.cursor()
        timestamp = get_timestamp()
        
        # Get current values
        cursor.execute("SELECT * FROM \"Transaction\" WHERE id = ? AND status = 'active'", (transaction_id,))
        current = cursor.fetchone()
        if not current:
            conn.close()
            return False
        
        current = dict(current)
        
        cursor.execute('''
            UPDATE "Transaction" 
            SET transaction_type = ?, reason = ?, responsible_person = ?, updated_at = ?
            WHERE id = ? AND status = 'active'
        ''', (
            transaction_type if transaction_type else current['transaction_type'],
            reason if reason is not None else current['reason'],
            responsible_person if responsible_person is not None else current['responsible_person'],
            timestamp,
            transaction_id
        ))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    @staticmethod
    def delete(transaction_id):
        """Soft delete a transaction by setting status to 'deleted'."""
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
    def get_filtered(asset_id=None, asset_type=None):
        """Get filtered transactions."""
        conn = get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT t.*, a.name as asset_name, a.asset_type 
            FROM "Transaction" t
            JOIN Asset a ON t.asset_id = a.id
            WHERE t.status = 'active'
        '''
        params = []
        
        if asset_id:
            query += ' AND t.asset_id = ?'
            params.append(asset_id)
        
        if asset_type:
            query += ' AND a.asset_type = ?'
            params.append(asset_type)
        
        query += ' ORDER BY t.created_at DESC'
        
        cursor.execute(query, params)
        transactions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return transactions
    
    @staticmethod
    def get_recent(limit=10, locker_id=None):
        """Get recent transactions with asset info, optionally filtered by locker_id."""
        conn = get_connection()
        cursor = conn.cursor()
        
        if locker_id:
            cursor.execute('''
                SELECT t.*, a.name as asset_name, a.asset_type 
                FROM "Transaction" t
                JOIN Asset a ON t.asset_id = a.id
                WHERE t.status = 'active' AND a.locker_id = ?
                ORDER BY t.created_at DESC
                LIMIT ?
            ''', (locker_id, limit))
        else:
            cursor.execute('''
                SELECT t.*, a.name as asset_name, a.asset_type 
                FROM "Transaction" t
                JOIN Asset a ON t.asset_id = a.id
                WHERE t.status = 'active'
                ORDER BY t.created_at DESC
                LIMIT ?
            ''', (limit,))
        
        transactions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return transactions

