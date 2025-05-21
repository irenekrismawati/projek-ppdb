from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin 
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    pendaftarans = db.relationship('Pendaftaran', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_admin(self):
        return self.role == 'admin'

class Pendaftaran(db.Model):
    __tablename__ = 'pendaftaran'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    nisn = db.Column(db.String(20), unique=True, nullable=False)
    asal_sekolah = db.Column(db.String(100))
    pilihan_jurusan = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')
    tanggal_daftar = db.Column(db.DateTime, default=datetime.utcnow)

class Sekolah(db.Model):
    __tablename__ = 'sekolah'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    akreditasi = db.Column(db.String(1))
    kepala_sekolah = db.Column(db.String(100))
    email = db.Column(db.String(120))
    telepon = db.Column(db.String(20))

class PaymentRequest(db.Model):
    __tablename__ = 'payment_requests'
    id = db.Column(db.Integer, primary_key=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'))