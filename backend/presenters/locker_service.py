"""
Locker service/presenter for business logic.
"""
from backend.models.locker import LockerModel
from backend.presenters.dashboard_service import DashboardService


class LockerService:
    """Service class for locker business logic."""
    
    @staticmethod
    def get_all_lockers():
        """Get all lockers with asset counts."""
        lockers = LockerModel.get_all()
        
        # Add asset counts for each locker
        for locker in lockers:
            try:
                stats = DashboardService.get_locker_stats(locker['id'])
                locker['total_assets'] = stats.get('total_assets', 0)
                locker['withdrawn_assets'] = stats.get('withdrawn_assets', 0)
            except Exception as e:
                # If stats fail, set defaults but still return the locker
                print(f"Error getting stats for locker {locker['id']}: {str(e)}")
                locker['total_assets'] = 0
                locker['withdrawn_assets'] = 0
        
        return lockers
    
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

