from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Konfigurasi dasar (ganti sesuai kebutuhanmu)
    app.config['SECRET_KEY'] = 'ini-rahasia'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ppdb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inisialisasi ekstensi
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'

    # Import dan register blueprint hanya sekali!
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # User loader
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
