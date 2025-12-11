from flask import Flask, jsonify
from app.routes_tasks import tasks_bp
from app.routes_notes import notes_bp
from app.routes_agents import agents_bp
from flask_cors import CORS
from app.db.chroma_manager import get_chroma_manager
from app.utils.seed import seed_data
from app.api import api_bp
import os

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")

    # Configure CORS - allow all origins for development
    CORS(app, 
         resources={r"/*": {"origins": "*"}},
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
         supports_credentials=False)

    # Initialize ChromaDB manager
    manager = get_chroma_manager()

    # Seed if empty
    if not manager.get_all_tasks():
        print("No data found. Seeding database...")
        seed_data()

    app.register_blueprint(tasks_bp, url_prefix="/tasks")
    app.register_blueprint(notes_bp, url_prefix="/notes")
    app.register_blueprint(agents_bp, url_prefix="/agents")
    app.register_blueprint(api_bp, url_prefix="/api")
    
    @app.route("/")
    def index():
        return jsonify({"message": "Flask API is running", "status": "ok"})
    
    @app.route("/health")
    def health_check():
        return jsonify({"status": "healthy", "api": "tasks-notes-crud"})

    return app