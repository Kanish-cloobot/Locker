"""
Locker service/presenter for business logic.
"""
from backend.models.locker import LockerModel


class LockerService:
    """Service class for locker business logic."""
    
    @staticmethod
    def get_all_lockers():
        """Get all lockers."""
        return LockerModel.get_all()
    
    @staticmethod
    def get_locker_by_id(locker_id):
        """Get a locker by ID."""
        return LockerModel.get_by_id(locker_id)
    
    @staticmethod
    def create_locker(data):
        """Create a new locker from request data."""
        name = data.get('name')
        location_name = data.get('location_name')
        address = data.get('address')
        
        if not name or not location_name or not address:
            raise ValueError("Name, location_name, and address are required")
        
        locker_id = LockerModel.create(name, location_name, address)
        return LockerModel.get_by_id(locker_id)
    
    @staticmethod
    def update_locker(locker_id, data):
        """Update an existing locker."""
        locker = LockerModel.get_by_id(locker_id)
        if not locker:
            raise ValueError("Locker not found")
        
        name = data.get('name', locker['name'])
        location_name = data.get('location_name', locker['location_name'])
        address = data.get('address', locker['address'])
        
        LockerModel.update(locker_id, name, location_name, address)
        return LockerModel.get_by_id(locker_id)
    
    @staticmethod
    def delete_locker(locker_id):
        """Delete a locker."""
        locker = LockerModel.get_by_id(locker_id)
        if not locker:
            raise ValueError("Locker not found")
        
        return LockerModel.delete(locker_id)
    
    @staticmethod
    def get_locker_stats(locker_id):
        """Get asset statistics for a locker."""
        from backend.database.db_setup import get_connection
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Total assets (including withdrawn)
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM Asset
            WHERE locker_id = ? AND status = 'active'
        ''', (locker_id,))
        total_assets = cursor.fetchone()['count']
        
        # Withdrawn assets count
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM Asset
            WHERE locker_id = ? AND current_status = 'WITHDRAWN' AND status = 'active'
        ''', (locker_id,))
        withdrawn_count = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            'total_assets': total_assets,
            'withdrawn_count': withdrawn_count
        }

