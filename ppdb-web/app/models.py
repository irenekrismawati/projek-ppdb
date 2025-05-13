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
    pendaftarans = db.relationship('Pendaftaran', backref='user', lazy=True)

class Sekolah(db.Model):
    __tablename__ = 'sekolah'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.String(200), nullable=True)
    pendaftarans = db.relationship('Pendaftaran', backref='sekolah', lazy=True)

class Pendaftaran(db.Model):
    __tablename__ = 'pendaftaran'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    sekolah_id = db.Column(db.Integer, db.ForeignKey('sekolah.id'), nullable=False)
    nilai = db.Column(db.Float, nullable=True)