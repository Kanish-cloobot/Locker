"""
Transaction API routes/views.
"""
from flask import Blueprint, request, jsonify
from backend.presenters.transaction_service import TransactionService

transaction_bp = Blueprint('transaction', __name__)


@transaction_bp.route('/api/transactions', methods=['GET'])
def get_all_transactions():
    """Get all transactions with optional filters."""
    try:
        asset_id = request.args.get('asset_id', type=int)
        asset_type = request.args.get('asset_type')
        
        if asset_id or asset_type:
            transactions = TransactionService.get_filtered_transactions(
                asset_id=asset_id,
                asset_type=asset_type
            )
        else:
            transactions = TransactionService.get_all_transactions()
        
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transaction_bp.route('/api/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction_by_id(transaction_id):
    """Get a transaction by ID."""
    try:
        transaction = TransactionService.get_transaction_by_id(transaction_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        return jsonify(transaction), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transaction_bp.route('/api/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction."""
    try:
        data = request.get_json()
        transaction = TransactionService.create_transaction(data)
        return jsonify(transaction), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transaction_bp.route('/api/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    """Update an existing transaction."""
    try:
        data = request.get_json()
        transaction = TransactionService.update_transaction(transaction_id, data)
        return jsonify(transaction), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transaction_bp.route('/api/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    """Delete a transaction."""
    try:
        TransactionService.delete_transaction(transaction_id)
        return jsonify({'message': 'Transaction deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transaction_bp.route('/api/transactions/recent', methods=['GET'])
def get_recent_transactions():
    """Get recent transactions."""
    try:
        limit = request.args.get('limit', 10, type=int)
        transactions = TransactionService.get_recent_transactions(limit=limit)
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

