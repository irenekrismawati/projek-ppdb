from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100))
    role = db.Column(db.String(20), default='user')  # 'admin' or 'user'
    is_active = db.Column(db.Boolean, default=True)
    pendaftarans = db.relationship('Pendaftaran', backref='user', lazy=True)

    def is_admin(self):
        return self.role == 'admin'

class Pendaftaran(db.Model):
    __tablename__ = 'pendaftaran'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    nisn = db.Column(db.String(20), nullable=False, unique=True)
    asal_sekolah = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    no_hp = db.Column(db.String(20), nullable=False)
    pilihan_jurusan = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tanggal_daftar = db.Column(db.DateTime, default=db.func.current_timestamp())

class Sekolah(db.Model):
    __tablename__ = 'sekolah'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    akreditasi = db.Column(db.String(1))
    kepala_sekolah = db.Column(db.String(100))
    email = db.Column(db.String(120))
    telepon = db.Column(db.String(20))

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pendaftaran_id = db.Column(db.Integer, db.ForeignKey('pendaftaran.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_proof = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # pending, verified, rejected
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)
    
    pendaftaran = db.relationship('Pendaftaran', backref='payments')