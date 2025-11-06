/**
 * Asset data model.
 */
class Asset {
  constructor(data = {}) {
    this.id = data.id || null;
    this.locker_id = data.locker_id || null;
    this.org_id = data.org_id || 1;
    this.user_id = data.user_id || 1;
    this.name = data.name || '';
    this.asset_type = data.asset_type || 'MISC';
    this.worth_on_creation = data.worth_on_creation || null;
    this.details = data.details || '';
    this.creation_date = data.creation_date || '';
    this.created_at = data.created_at || '';
    this.updated_at = data.updated_at || '';
    
    // Detail fields
    this.jewellery_details = data.jewellery_details || null;
    this.document_details = data.document_details || null;
  }

  toJSON() {
    const json = {
      name: this.name,
      asset_type: this.asset_type,
      worth_on_creation: this.worth_on_creation || null,
      details: this.details || null,
      creation_date: this.creation_date || null
    };

    if (this.asset_type === 'JEWELLERY') {
      json.material_type = this.jewellery_details?.material_type || null;
      json.material_grade = this.jewellery_details?.material_grade || null;
      json.gifting_details = this.jewellery_details?.gifting_details || null;
    } else if (this.asset_type === 'DOCUMENT') {
      json.document_type = this.document_details?.document_type || null;
    }

    return json;
  }
}

export default Asset;

