import os
from flask import Config, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate 

migrate = Migrate()

# Inisialisasi ekstensi
db = SQLAlchemy()

login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    # Konfigurasi aplikasi
    migrate.init_app(app, db)   
    # Add upload folder configuration
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/profile_pics')
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    app.config['SECRET_KEY'] = 'mysecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inisialisasi ekstensi
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    
# Tambahkan filter template untuk format tanggal
    
   # Daftarkan Blueprint
    from .routes import register_blueprints
    register_blueprints(app)
    
    with app.app_context():
        from app import models
       

    return app