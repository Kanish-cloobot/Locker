"""
Main Flask application entry point.
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from backend.database.db_setup import init_database
from backend.views.locker_routes import locker_bp
from backend.views.asset_routes import asset_bp
from backend.views.transaction_routes import transaction_bp
from backend.views.file_routes import file_bp
from backend.views.dashboard_routes import dashboard_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Register blueprints
app.register_blueprint(locker_bp)
app.register_blueprint(asset_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(file_bp)
app.register_blueprint(dashboard_bp)


@app.route('/')
def index():
    """Root endpoint."""
    from flask import jsonify
    return jsonify({'message': 'Family Locker Organizer API', 'status': 'running'})


if __name__ == '__main__':
    # Initialize database on startup
    init_database()
    # Run the Flask app
    app.run(debug=True, port=5000)

