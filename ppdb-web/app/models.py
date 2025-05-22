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
    nisn = db.Column(db.String(10), nullable=False, unique=True)
    tempat_lahir = db.Column(db.String(50), nullable=False) 
    tanggal_lahir = db.Column(db.Date, nullable=False)
    jenis_kelamin = db.Column(db.String(1), nullable=False)
    agama = db.Column(db.String(20), nullable=False)
    alamat = db.Column(db.Text, nullable=False)  # Tambahkan kolom alamat
    rt_rw = db.Column(db.String(10))
    no_hp = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120))
    nama_ayah = db.Column(db.String(100), nullable=False)
    agama_ayah = db.Column(db.String(20), nullable=False)
    pekerjaan_ayah = db.Column(db.String(50), nullable=False)
    nama_ibu = db.Column(db.String(100), nullable=False)
    agama_ibu = db.Column(db.String(20), nullable=False)
    pekerjaan_ibu = db.Column(db.String(50), nullable=False)
    asal_sekolah = db.Column(db.String(100), nullable=False)
    npsn_sekolah = db.Column(db.String(10))
    pilihan_jurusan = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')
    tanggal_daftar = db.Column(db.DateTime, default=datetime.utcnow)

    
class Sekolah(db.Model):
    __tablename__ = 'sekolah'
    
    id = db.Column(db.Integer, primary_key=True)  # Add primary key
    nama = db.Column(db.String(100), nullable=False)
    npsn = db.Column(db.String(10), unique=True)
    alamat = db.Column(db.Text)
    kota = db.Column(db.String(50))
    provinsi = db.Column(db.String(50))
    status = db.Column(db.String(20))  # negeri/swasta
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PaymentRequest(db.Model):
    __tablename__ = 'payment_requests'
    id = db.Column(db.Integer, primary_key=True)
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'))