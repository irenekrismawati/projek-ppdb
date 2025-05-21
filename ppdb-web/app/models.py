from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin 
from app import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100))
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pendaftarans = db.relationship('Pendaftaran', backref='user', lazy=True)

    def is_admin(self):
        return self.role == 'admin'

class Pendaftaran(db.Model):
    __tablename__ = 'pendaftaran'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    nisn = db.Column(db.String(20), nullable=False, unique=True)
    tempat_lahir = db.Column(db.String(100), nullable=False)
    tanggal_lahir = db.Column(db.Date, nullable=False)
    jenis_kelamin = db.Column(db.String(1), nullable=False)
    asal_sekolah = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    no_hp = db.Column(db.String(20), nullable=False)
    pilihan_jurusan = db.Column(db.String(50), nullable=False)
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pendaftaran_id = db.Column(db.Integer, db.ForeignKey('pendaftaran.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=500000)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, paid
    payment_method = db.Column(db.String(50), nullable=False)
    payment_proof = db.Column(db.String(200))
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    paid_at = db.Column(db.DateTime)
    admin_notes = db.Column(db.Text)