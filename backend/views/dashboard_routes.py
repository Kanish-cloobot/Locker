"""
Dashboard API routes/views.
"""
from flask import Blueprint, jsonify
from backend.presenters.dashboard_service import DashboardService

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    """Get dashboard statistics."""
    try:
        stats = DashboardService.get_dashboard_stats()
        return jsonify(stats), 200
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Dashboard error: {str(e)}")
        print(f"Traceback: {error_trace}")
        return jsonify({'error': str(e), 'traceback': error_trace}), 500

