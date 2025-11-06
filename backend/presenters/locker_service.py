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

