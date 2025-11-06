"""
Transaction service/presenter for business logic.
"""
from backend.models.transaction import TransactionModel


class TransactionService:
    """Service class for transaction business logic."""
    
    @staticmethod
    def get_all_transactions():
        """Get all transactions with asset information."""
        return TransactionModel.get_all()
    
    @staticmethod
    def get_transaction_by_id(transaction_id):
        """Get a transaction by ID with asset information."""
        return TransactionModel.get_by_id(transaction_id)
    
    @staticmethod
    def get_transactions_by_asset(asset_id):
        """Get all transactions for a specific asset."""
        return TransactionModel.get_by_asset_id(asset_id)
    
    @staticmethod
    def create_transaction(data):
        """Create a new transaction."""
        asset_id = data.get('asset_id')
        transaction_type = data.get('transaction_type')
        
        if not asset_id or not transaction_type:
            raise ValueError("asset_id and transaction_type are required")
        
        if transaction_type not in ['DEPOSIT', 'WITHDRAW', 'PERMANENT_REMOVE']:
            raise ValueError("transaction_type must be DEPOSIT, WITHDRAW, or PERMANENT_REMOVE")
        
        transaction_id = TransactionModel.create(
            asset_id=asset_id,
            transaction_type=transaction_type,
            reason=data.get('reason'),
            responsible_person=data.get('responsible_person')
        )
        
        return TransactionService.get_transaction_by_id(transaction_id)
    
    @staticmethod
    def update_transaction(transaction_id, data):
        """Update an existing transaction."""
        transaction = TransactionModel.get_by_id(transaction_id)
        if not transaction:
            raise ValueError("Transaction not found")
        
        TransactionModel.update(
            transaction_id=transaction_id,
            transaction_type=data.get('transaction_type'),
            reason=data.get('reason'),
            responsible_person=data.get('responsible_person')
        )
        
        return TransactionService.get_transaction_by_id(transaction_id)
    
    @staticmethod
    def delete_transaction(transaction_id):
        """Delete a transaction."""
        transaction = TransactionModel.get_by_id(transaction_id)
        if not transaction:
            raise ValueError("Transaction not found")
        
        return TransactionModel.delete(transaction_id)
    
    @staticmethod
    def get_filtered_transactions(asset_id=None, asset_type=None):
        """Get filtered transactions."""
        return TransactionModel.get_filtered(asset_id=asset_id, asset_type=asset_type)
    
    @staticmethod
    def get_recent_transactions(limit=10):
        """Get recent transactions."""
        return TransactionModel.get_recent(limit=limit)

