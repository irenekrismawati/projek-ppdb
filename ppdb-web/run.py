from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    
    # Buat admin default jika belum ada
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            name='Administrator',
            role='admin',
            password=generate_password_hash('admin123')  # Password default: admin123
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin default berhasil dibuat:')
        print('Username: admin')
        print('Password: admin123')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)