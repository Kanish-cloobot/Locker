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

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Register blueprints
app.register_blueprint(locker_bp)
app.register_blueprint(asset_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(file_bp)


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

