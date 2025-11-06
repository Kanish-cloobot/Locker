"""
Transaction service/presenter for business logic.
"""
from backend.models.transaction import TransactionModel
from backend.models.asset import AssetModel


class TransactionService:
    """Service class for transaction business logic."""
    
    @staticmethod
    def create_transaction(asset_id, locker_id, transaction_type, reason=None,
                          responsible_person=None, transaction_date=None):
        """Create a new transaction and update asset status."""
        if transaction_type not in ['DEPOSIT', 'WITHDRAW', 'PERMANENTLY_REMOVE']:
            raise ValueError("transaction_type must be DEPOSIT, WITHDRAW, or PERMANENTLY_REMOVE")
        
        # Verify asset exists and belongs to locker
        asset = AssetModel.get_by_id(asset_id)
        if not asset:
            raise ValueError("Asset not found")
        if asset['locker_id'] != locker_id:
            raise ValueError("Asset does not belong to this locker")
        
        # Create transaction
        transaction_id = TransactionModel.create(
            asset_id=asset_id,
            locker_id=locker_id,
            transaction_type=transaction_type,
            reason=reason,
            responsible_person=responsible_person,
            transaction_date=transaction_date
        )
        
        # Update asset current_status based on transaction type
        if transaction_type == 'DEPOSIT':
            new_status = 'IN_LOCKER'
        elif transaction_type == 'WITHDRAW':
            new_status = 'WITHDRAWN'
        elif transaction_type == 'PERMANENTLY_REMOVE':
            new_status = 'PERMANENTLY_REMOVED'
        
        AssetModel.update(
            asset_id, 
            asset['name'], 
            asset['asset_type'], 
            current_status=new_status
        )
        
        return TransactionModel.get_by_id(transaction_id)
    
    @staticmethod
    def get_transactions_by_locker(locker_id):
        """Get all transactions for a locker."""
        return TransactionModel.get_by_locker_id(locker_id)
    
    @staticmethod
    def get_transactions_by_asset(asset_id):
        """Get all transactions for an asset."""
        return TransactionModel.get_by_asset_id(asset_id)
    
    @staticmethod
    def get_dashboard_stats(locker_id):
        """Get dashboard statistics for a locker."""
        from backend.database.db_setup import get_connection
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Total deposited (count of DEPOSIT transactions)
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM "Transaction"
            WHERE locker_id = ? AND transaction_type = 'DEPOSIT' AND status = 'active'
        ''', (locker_id,))
        total_deposited = cursor.fetchone()['count']
        
        # Withdrawn count (assets with current_status = 'WITHDRAWN')
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM Asset
            WHERE locker_id = ? AND current_status = 'WITHDRAWN' AND status = 'active'
        ''', (locker_id,))
        withdrawn_count = cursor.fetchone()['count']
        
        # Currently in locker (assets with current_status = 'IN_LOCKER')
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM Asset
            WHERE locker_id = ? AND current_status = 'IN_LOCKER' AND status = 'active'
        ''', (locker_id,))
        currently_in_locker = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            'total_deposited': total_deposited,
            'withdrawn_count': withdrawn_count,
            'currently_in_locker': currently_in_locker
        }
    
    @staticmethod
    def get_recent_transactions(locker_id, limit=10):
        """Get recent transactions for a locker."""
        transactions = TransactionModel.get_by_locker_id(locker_id)
        return transactions[:limit]
    
    @staticmethod
    def update_transaction(transaction_id, transaction_type=None, reason=None,
                          responsible_person=None, transaction_date=None):
        """Update a transaction."""
        transaction = TransactionModel.get_by_id(transaction_id)
        if not transaction:
            raise ValueError("Transaction not found")
        
        # If transaction type is being updated, update asset status
        if transaction_type and transaction_type != transaction['transaction_type']:
            asset_id = transaction['asset_id']
            asset = AssetModel.get_by_id(asset_id)
            if not asset:
                raise ValueError("Asset not found")
            if transaction_type == 'DEPOSIT':
                new_status = 'IN_LOCKER'
            elif transaction_type == 'WITHDRAW':
                new_status = 'WITHDRAWN'
            elif transaction_type == 'PERMANENTLY_REMOVE':
                new_status = 'PERMANENTLY_REMOVED'
            AssetModel.update(
                asset_id, 
                asset['name'], 
                asset['asset_type'], 
                current_status=new_status
            )
        
        TransactionModel.update(
            transaction_id=transaction_id,
            transaction_type=transaction_type,
            reason=reason,
            responsible_person=responsible_person,
            transaction_date=transaction_date
        )
        
        return TransactionModel.get_by_id(transaction_id)
    
    @staticmethod
    def delete_transaction(transaction_id):
        """Delete a transaction."""
        transaction = TransactionModel.get_by_id(transaction_id)
        if not transaction:
            raise ValueError("Transaction not found")
        
        return TransactionModel.delete(transaction_id)
    
    @staticmethod
    def filter_transactions(locker_id, asset_id=None, asset_type=None):
        """Filter transactions by asset or asset type."""
        if asset_id:
            return TransactionModel.filter_by_asset(locker_id, asset_id)
        elif asset_type:
            return TransactionModel.filter_by_asset_type(locker_id, asset_type)
        else:
            return TransactionModel.get_by_locker_id(locker_id)

