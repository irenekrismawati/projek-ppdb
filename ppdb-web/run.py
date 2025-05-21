from app import create_app, db
from app.models import User, Pendaftaran, Sekolah, PaymentRequest
from werkzeug.security import generate_password_hash
import os
import time
import psutil

app = create_app()

def init_db():
    with app.app_context():
        try:
            db_path = os.path.join('instance', 'database.db')
            
            print("Starting database initialization...")
            
            # Create instance directory if it doesn't exist
            if not os.path.exists('instance'):
                os.makedirs('instance')
            
            # Create database tables
            db.create_all()
            print("Database tables created successfully")

            # Create admin user if not exists
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
                print("Admin user created successfully")
            
            return True

        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            if 'db' in locals():
                db.session.rollback()
            return False

if __name__ == '__main__':
    print("Initializing application...")
    if init_db():
        print("Starting server at http://localhost:3000")
        app.run(host='0.0.0.0', port=3000, debug=True)
    else:
        print("Failed to initialize database. Check the error messages above.")