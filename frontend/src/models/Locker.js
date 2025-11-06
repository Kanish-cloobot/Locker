/**
 * Locker data model.
 */
class Locker {
  constructor(data = {}) {
    this.id = data.id || null;
    this.org_id = data.org_id || 1;
    this.user_id = data.user_id || 1;
    this.name = data.name || '';
    this.location_name = data.location_name || '';
    this.address = data.address || '';
    this.created_at = data.created_at || '';
    this.updated_at = data.updated_at || '';
    this.total_assets = data.total_assets || 0;
    this.withdrawn_assets = data.withdrawn_assets || 0;
  }

  toJSON() {
    return {
      name: this.name,
      location_name: this.location_name,
      address: this.address
    };
  }
}

export default Locker;

