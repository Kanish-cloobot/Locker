"""
Transaction API routes/views.
"""
from flask import Blueprint, request, jsonify
from backend.presenters.transaction_service import TransactionService

transaction_bp = Blueprint('transaction', __name__)


@transaction_bp.route('/api/lockers/<int:locker_id>/transactions', methods=['GET'])
def get_transactions_by_locker(locker_id):
    """Get all transactions for a specific locker."""
    try:
        transactions = TransactionService.get_transactions_by_locker(locker_id)
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transaction_bp.route('/api/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction."""
    try:
        data = request.get_json()
        asset_id = data.get('asset_id')
        locker_id = data.get('locker_id')
        transaction_type = data.get('transaction_type')
        
        if not asset_id or not locker_id or not transaction_type:
            return jsonify({'error': 'asset_id, locker_id, and transaction_type are required'}), 400
        
        transaction = TransactionService.create_transaction(
            asset_id=asset_id,
            locker_id=locker_id,
            transaction_type=transaction_type,
            reason=data.get('reason'),
            responsible_person=data.get('responsible_person'),
            transaction_date=data.get('transaction_date')
        )
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
        transaction = TransactionService.update_transaction(
            transaction_id=transaction_id,
            transaction_type=data.get('transaction_type'),
            reason=data.get('reason'),
            responsible_person=data.get('responsible_person'),
            transaction_date=data.get('transaction_date')
        )
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


@transaction_bp.route('/api/lockers/<int:locker_id>/transactions/filter', methods=['GET'])
def filter_transactions(locker_id):
    """Filter transactions by asset or asset type."""
    try:
        asset_id = request.args.get('asset_id', type=int)
        asset_type = request.args.get('asset_type')
        
        transactions = TransactionService.filter_transactions(
            locker_id=locker_id,
            asset_id=asset_id,
            asset_type=asset_type
        )
        return jsonify(transactions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@transaction_bp.route('/api/lockers/<int:locker_id>/dashboard', methods=['GET'])
def get_dashboard(locker_id):
    """Get dashboard data for a locker."""
    try:
        stats = TransactionService.get_dashboard_stats(locker_id)
        recent_transactions = TransactionService.get_recent_transactions(locker_id, limit=10)
        
        return jsonify({
            'stats': stats,
            'recent_transactions': recent_transactions
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

