import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, 'ppdb-web'))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

def buat_admin():
    with app.app_context():
        try:
            # Cek apakah admin sudah ada
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    password=generate_password_hash('admin123'),
                    name='Administrator',
                    role='admin',
                    is_active=True
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin berhasil dibuat!")
                print("Username: admin")
                print("Password: admin123")
            else:
                print("⚠️ Admin sudah ada!")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    buat_admin()