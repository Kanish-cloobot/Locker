# Family Locker Organizer

A full-stack web application for tracking family assets stored in lockers. Built with ReactJS (frontend), Python/Flask (backend), and SQLite (database).

## Project Structure (MVP Architecture)

```
Locker/
├── backend/
│   ├── models/          # Data layer - database models
│   │   ├── locker.py
│   │   ├── asset.py
│   │   └── asset_detail.py
│   ├── views/           # Presentation layer - API routes
│   │   ├── locker_routes.py
│   │   └── asset_routes.py
│   ├── presenters/      # Business logic layer - services
│   │   ├── locker_service.py
│   │   └── asset_service.py
│   └── database/        # Database setup
│       └── db_setup.py
├── frontend/
│   ├── src/
│   │   ├── models/      # Data models
│   │   │   ├── Locker.js
│   │   │   └── Asset.js
│   │   ├── views/       # UI components
│   │   │   ├── HomePage.js
│   │   │   ├── LockerDetailPage.js
│   │   │   ├── CreateLockerModal.js
│   │   │   ├── EditLockerModal.js
│   │   │   └── AssetModal.js
│   │   ├── presenters/  # Business logic - API services
│   │   │   ├── lockerService.js
│   │   │   └── assetService.js
│   │   ├── styles/      # External CSS files
│   │   │   ├── App.css
│   │   │   ├── HomePage.css
│   │   │   ├── LockerDetailPage.css
│   │   │   └── Modal.css
│   │   ├── App.js
│   │   └── index.js
│   └── public/
├── app.py               # Flask application entry point
├── requirements.txt     # Python dependencies
└── README.md
```

## Features

- **Locker Management**: Create, view, update, and delete lockers
- **Asset Management**: Track assets (Jewellery, Documents, Miscellaneous) within lockers
- **Dynamic Forms**: Asset creation form adapts based on asset type
- **Cascade Deletion**: Deleting a locker automatically removes associated assets
- **Clean Architecture**: MVP (Model-View-Presenter) pattern for maintainability

## Database Schema

### Tables

1. **Locker**: Stores locker information (name, location, address)
2. **Asset**: Stores asset information (name, type, worth, details)
3. **AssetDetail_Jewellery**: Stores jewellery-specific details (material, grade, gifting info)
4. **AssetDetail_Document**: Stores document-specific details (document type)

All tables include `org_id` and `user_id` fields (defaulting to 1) and timestamps.

## Setup Instructions

### Prerequisites

- Python 3.7+
- Node.js 16.x (v16.20.2 recommended)
- npm 8.x (8.19.4 recommended)

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

The backend will start on `http://localhost:5000` and automatically create the SQLite database (`backend/locker.db`) on first run.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will start on `http://localhost:3000` and automatically open in your browser.

## API Endpoints

### Lockers

- `GET /api/lockers` - Get all lockers
- `POST /api/lockers` - Create a new locker
- `PUT /api/lockers/<id>` - Update a locker
- `DELETE /api/lockers/<id>` - Delete a locker

### Assets

- `GET /api/lockers/<locker_id>/assets` - Get all assets for a locker
- `POST /api/lockers/<locker_id>/assets` - Create a new asset
- `PUT /api/assets/<asset_id>` - Update an asset
- `DELETE /api/assets/<asset_id>` - Delete an asset

## Usage

1. **Create a Locker**: Click "Create New Locker" on the home page
2. **View Locker Details**: Click on any locker card to see its assets
3. **Add Assets**: Click "Add Asset" on the locker detail page
4. **Edit/Delete**: Use the Edit and Delete buttons on lockers and assets

## Asset Types

- **JEWELLERY**: Requires material type, grade, and gifting details
- **DOCUMENT**: Requires document type
- **MISC**: General assets with optional details

## Development Notes

- All CSS is external (no inline styles)
- Uses pixel values (no rem units)
- Human-readable naming conventions throughout
- Error handling and validation on both frontend and backend
- CORS enabled for development

## Testing

Test the application by:
1. Creating multiple lockers
2. Adding different types of assets to lockers
3. Editing and deleting lockers and assets
4. Verifying cascade deletion (deleting a locker removes its assets)

