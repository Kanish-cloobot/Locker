"""
Dashboard service for statistics and aggregations.
"""
from backend.database.db_setup import get_connection
from backend.models.transaction import TransactionModel


class DashboardService:
    """Service class for dashboard statistics."""
    
    @staticmethod
    def get_dashboard_stats(locker_id=None):
        """Get dashboard statistics for a specific locker or all lockers if locker_id is None."""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            if locker_id:
                # Total assets deposited (including withdrawn) for this locker
                cursor.execute('''
                    SELECT COUNT(DISTINCT t.asset_id) as total_deposited
                    FROM "Transaction" t
                    JOIN Asset a ON t.asset_id = a.id
                    WHERE t.transaction_type = 'DEPOSIT' 
                    AND t.status = 'active'
                    AND a.locker_id = ?
                ''', (locker_id,))
                result = cursor.fetchone()
                total_deposited = result['total_deposited'] if result and result['total_deposited'] else 0
                
                # Assets currently in locker - assets that have been deposited 
                # and the last transaction is not WITHDRAW or PERMANENT_REMOVE
                cursor.execute('''
                    SELECT COUNT(DISTINCT a.id) as current_in_locker
                    FROM Asset a
                    WHERE a.status = 'active' AND a.locker_id = ?
                    AND EXISTS (
                        SELECT 1 FROM "Transaction" t1
                        WHERE t1.asset_id = a.id 
                        AND t1.transaction_type = 'DEPOSIT' 
                        AND t1.status = 'active'
                    )
                    AND NOT EXISTS (
                        SELECT 1 FROM "Transaction" t2
                        WHERE t2.asset_id = a.id
                        AND t2.transaction_type IN ('WITHDRAW', 'PERMANENT_REMOVE')
                        AND t2.status = 'active'
                        AND t2.created_at > (
                            SELECT COALESCE(MAX(t3.created_at), '1900-01-01')
                            FROM "Transaction" t3
                            WHERE t3.asset_id = a.id
                            AND t3.transaction_type = 'DEPOSIT'
                            AND t3.status = 'active'
                        )
                    )
                ''', (locker_id,))
                result = cursor.fetchone()
                current_in_locker = result['current_in_locker'] if result and result['current_in_locker'] else 0
                
                # Assets withdrawn as on date for this locker
                cursor.execute('''
                    SELECT COUNT(DISTINCT t.asset_id) as withdrawn
                    FROM "Transaction" t
                    JOIN Asset a ON t.asset_id = a.id
                    WHERE t.transaction_type = 'WITHDRAW' 
                    AND t.status = 'active'
                    AND a.locker_id = ?
                ''', (locker_id,))
                result = cursor.fetchone()
                withdrawn = result['withdrawn'] if result and result['withdrawn'] else 0
                
                # Last 10 transactions for this locker
                recent_transactions = TransactionModel.get_recent(limit=10, locker_id=locker_id)
            else:
                # Total assets deposited (including withdrawn) - global
                cursor.execute('''
                    SELECT COUNT(DISTINCT asset_id) as total_deposited
                    FROM "Transaction"
                    WHERE transaction_type = 'DEPOSIT' AND status = 'active'
                ''')
                result = cursor.fetchone()
                total_deposited = result['total_deposited'] if result and result['total_deposited'] else 0
                
                # Assets currently in locker - assets that have been deposited 
                # and the last transaction is not WITHDRAW or PERMANENT_REMOVE
                cursor.execute('''
                    SELECT COUNT(DISTINCT a.id) as current_in_locker
                    FROM Asset a
                    WHERE a.status = 'active'
                    AND EXISTS (
                        SELECT 1 FROM "Transaction" t1
                        WHERE t1.asset_id = a.id 
                        AND t1.transaction_type = 'DEPOSIT' 
                        AND t1.status = 'active'
                    )
                    AND NOT EXISTS (
                        SELECT 1 FROM "Transaction" t2
                        WHERE t2.asset_id = a.id
                        AND t2.transaction_type IN ('WITHDRAW', 'PERMANENT_REMOVE')
                        AND t2.status = 'active'
                        AND t2.created_at > (
                            SELECT COALESCE(MAX(t3.created_at), '1900-01-01')
                            FROM "Transaction" t3
                            WHERE t3.asset_id = a.id
                            AND t3.transaction_type = 'DEPOSIT'
                            AND t3.status = 'active'
                        )
                    )
                ''')
                result = cursor.fetchone()
                current_in_locker = result['current_in_locker'] if result and result['current_in_locker'] else 0
                
                # Assets withdrawn as on date
                cursor.execute('''
                    SELECT COUNT(DISTINCT asset_id) as withdrawn
                    FROM "Transaction"
                    WHERE transaction_type = 'WITHDRAW' AND status = 'active'
                ''')
                result = cursor.fetchone()
                withdrawn = result['withdrawn'] if result and result['withdrawn'] else 0
                
                # Last 10 transactions
                recent_transactions = TransactionModel.get_recent(limit=10)
            
            return {
                'total_deposited': total_deposited,
                'current_in_locker': current_in_locker,
                'withdrawn': withdrawn,
                'recent_transactions': recent_transactions
            }
        except Exception as e:
            # Log the error for debugging
            import traceback
            error_trace = traceback.format_exc()
            print(f"Dashboard stats error: {str(e)}")
            print(f"Traceback: {error_trace}")
            # Return default values on error
            return {
                'total_deposited': 0,
                'current_in_locker': 0,
                'withdrawn': 0,
                'recent_transactions': []
            }
        finally:
            conn.close()
    
    @staticmethod
    def get_locker_stats(locker_id):
        """Get statistics for a specific locker."""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Total assets in this locker (including withdrawn)
            cursor.execute('''
                SELECT COUNT(DISTINCT a.id) as total_assets
                FROM Asset a
                WHERE a.locker_id = ? AND a.status = 'active'
            ''', (locker_id,))
            result = cursor.fetchone()
            total_assets = result['total_assets'] if result and result['total_assets'] else 0
            
            # Assets withdrawn from this locker
            cursor.execute('''
                SELECT COUNT(DISTINCT t.asset_id) as withdrawn_assets
                FROM "Transaction" t
                JOIN Asset a ON t.asset_id = a.id
                WHERE a.locker_id = ? 
                AND t.transaction_type = 'WITHDRAW' 
                AND t.status = 'active'
                AND a.status = 'active'
            ''', (locker_id,))
            result = cursor.fetchone()
            withdrawn_assets = result['withdrawn_assets'] if result and result['withdrawn_assets'] else 0
            
            return {
                'total_assets': total_assets,
                'withdrawn_assets': withdrawn_assets
            }
        except Exception as e:
            # Return default values on error
            import traceback
            print(f"Error getting locker stats for locker {locker_id}: {str(e)}")
            print(traceback.format_exc())
            return {
                'total_assets': 0,
                'withdrawn_assets': 0
            }
        finally:
            conn.close()

