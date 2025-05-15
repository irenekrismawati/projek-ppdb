import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from app.models import User
from app import db

auth_bp = Blueprint('auth_bp', __name__)

# -------- LOGIN --------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main_bp.index'))
        else:
            flash('Login gagal. Cek username dan password.', 'danger')

    return render_template('login.html')

# -------- REGISTER --------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            name = request.form.get('name')

            # Cek email sudah terdaftar atau belum
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email sudah terdaftar! Silakan gunakan email lain.', 'error')
                return render_template('register.html')

            # Cek username sudah digunakan atau belum    
            existing_username = User.query.filter_by(username=username).first()
            if existing_username:
                flash('Username sudah digunakan! Silakan pilih username lain.', 'error')
                return render_template('register.html')

            # Buat user baru
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password),
                name=name
            )

            db.session.add(new_user)
            db.session.commit()
            
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('auth_bp.login'))

        except Exception as e:
            db.session.rollback()
            print(f"Error saat registrasi: {str(e)}")
            flash('Terjadi kesalahan saat registrasi.', 'error')
            
    return render_template('register.html')

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# -------- LOGOUT --------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))
