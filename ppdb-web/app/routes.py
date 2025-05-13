from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .models import Student, User
from . import db

# Buat blueprint terpisah
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

def my_function():
    print("Hello")
    print("World")  # Indentasi konsisten
    
# Route utama
@main_bp.route('/')
def index():
    return render_template('index.html')

# Route registrasi siswa

# Route registrasi user/akun
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        try:
            # Validasi input
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            name = request.form.get('name')
            
            # Cek username dan email yang sudah ada
            if User.query.filter_by(username=username).first():
                flash('Username sudah digunakan!', 'error')
                return render_template('register.html')
                
            if User.query.filter_by(email=email).first():
                flash('Email sudah terdaftar!', 'error')
                return render_template('register.html')
            
            # Buat user baru
            user = User(
                email=email,
                username=username,
                password=generate_password_hash(password),
                name=name
            )
            
            db.session.add(user)
            db.session.commit()
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Registrasi gagal!', 'error')
            print(f"Error: {str(e)}")
            
    return render_template('register.html')