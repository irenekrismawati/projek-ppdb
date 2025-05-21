from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Ensure instance folder exists
    if not os.path.exists('instance'):
        os.makedirs('instance')
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'

    # Add user loader function
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    with app.app_context():
        # Import models
        from app.models import User, Pendaftaran
        
        # Create tables
        db.create_all()

        # Register blueprints
        from app.routes.main import main_bp
        from app.routes.auth import auth_bp
        from app.routes.admin import admin_bp
        
        # Register blueprints - main_bp first to handle root URL
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp)

    return app