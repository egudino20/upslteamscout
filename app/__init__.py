from flask import Flask
import os
import datetime
from config import SECRET_KEY, DEBUG

def create_app():
    # Check if we're running in production (Render)
    if 'GOOGLE_APPLICATION_CREDENTIALS_JSON' in os.environ:
        # Create a temporary file with the credentials
        credentials_content = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        credentials_path = 'credentials/google-credentials-temp.json'
        
        # Ensure the credentials directory exists
        os.makedirs('credentials', exist_ok=True)
        
        with open(credentials_path, 'w') as f:
            f.write(credentials_content)
            
        # Set environment variable to point to this file
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    else:
        # Local development using the file directly
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials/upsl-video-api-c5071e2d09bf.json'

    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DEBUG'] = DEBUG

    # Add context processor to make the current year available to all templates
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.datetime.now().year}

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.clubs import clubs_bp
    from app.routes.conferences import conferences_bp
    from app.routes.videos import videos_bp
    from app.routes.annotations import annotations_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(clubs_bp)
    app.register_blueprint(conferences_bp)
    app.register_blueprint(videos_bp)
    app.register_blueprint(annotations_bp)
    app.register_blueprint(api_bp)

    # Create required folders if they don't exist
    os.makedirs(os.path.join(app.static_folder, 'annotations'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'clips'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'images'), exist_ok=True)

    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return "Page not found", 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return "Internal server error", 500

    return app

