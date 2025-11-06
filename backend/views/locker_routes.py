"""
Locker API routes/views.
"""
from flask import Blueprint, request, jsonify
from backend.presenters.locker_service import LockerService

locker_bp = Blueprint('locker', __name__)


@locker_bp.route('/api/lockers', methods=['GET'])
def get_all_lockers():
    """Get all lockers."""
    try:
        lockers = LockerService.get_all_lockers()
        return jsonify(lockers), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@locker_bp.route('/api/lockers/<int:locker_id>', methods=['GET'])
def get_locker_by_id(locker_id):
    """Get a locker by ID."""
    try:
        locker = LockerService.get_locker_by_id(locker_id)
        if not locker:
            return jsonify({'error': 'Locker not found'}), 404
        return jsonify(locker), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@locker_bp.route('/api/lockers', methods=['POST'])
def create_locker():
    """Create a new locker."""
    try:
        data = request.get_json()
        locker = LockerService.create_locker(data)
        return jsonify(locker), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@locker_bp.route('/api/lockers/<int:locker_id>', methods=['PUT'])
def update_locker(locker_id):
    """Update an existing locker."""
    try:
        data = request.get_json()
        locker = LockerService.update_locker(locker_id, data)
        return jsonify(locker), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@locker_bp.route('/api/lockers/<int:locker_id>', methods=['DELETE'])
def delete_locker(locker_id):
    """Delete a locker."""
    try:
        LockerService.delete_locker(locker_id)
        return jsonify({'message': 'Locker deleted successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

