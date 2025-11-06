# Quick Setup Guide

## Step 1: Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the Flask server:
```bash
python app.py
```

The backend will:
- Create `backend/locker.db` automatically on first run
- Start on `http://localhost:5000`

## Step 2: Frontend Setup

1. Open a new terminal and navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will:
- Start on `http://localhost:3000`
- Automatically open in your browser
- Proxy API requests to `http://localhost:5000`

## Verification

1. Backend is running if you see: "Running on http://127.0.0.1:5000"
2. Frontend is running if browser opens to `http://localhost:3000`
3. Test by creating a locker on the home page

## Troubleshooting

- **Port 5000 already in use**: Change port in `app.py` (line 28)
- **Port 3000 already in use**: React will prompt to use a different port
- **Module not found errors**: Ensure you're running commands from the project root (for backend) and frontend directory (for frontend)
- **Database errors**: Delete `backend/locker.db` and restart the Flask app to recreate it

