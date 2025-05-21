from app import create_app, db
from app.models import User, Pendaftaran
from werkzeug.security import generate_password_hash
import os

app = create_app()

def init_db():
    with app.app_context():
        try:
            # Delete existing database file
            if os.path.exists('instance/database.db'):
                os.remove('instance/database.db')
            
            # Create tables
            db.create_all()
            
            # Create default admin if not exists
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    name='Administrator',
                    role='admin',
                    password=generate_password_hash('admin123')
                )
                db.session.add(admin)
                db.session.commit()
                print('Admin default berhasil dibuat:')
                print('Username: admin')
                print('Password: admin123')
                
        except Exception as e:
            print(f"Error: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=3000, debug=True)