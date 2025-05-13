import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inisialisasi objek db dan login_manager
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Konfigurasi dasar aplikasi
    app.config['SECRET_KEY'] = 'mysecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppdb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Konfigurasi folder upload
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/profile_pics')
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inisialisasi ekstensi
    db.init_app(app)
    login_manager.init_app(app)

    # Tentukan halaman login untuk flask-login
    login_manager.login_view = 'auth_bp.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    # Daftarkan blueprint untuk aplikasi
    from app.routes import register_blueprints
    register_blueprints(app)

    # Menggunakan app_context untuk memastikan models dimuat
    with app.app_context():
        from app import models  # Memastikan models diimpor
        db.create_all()  # Hanya buat tabel jika belum ada

    return app
