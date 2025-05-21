import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from app.models import User
from app import db

auth_bp = Blueprint('auth_bp', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

# -------- LOGIN --------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.profile'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            
            # Redirect to profile with success message
            flash('Login berhasil! Selamat datang kembali.', 'success')
            return redirect(next_page or url_for('main_bp.profile'))
        else:
            # Store error message in session instead of flash
            session['login_error'] = 'Login gagal. Cek username dan password.'
            return redirect(url_for('auth_bp.login'))
            
    # Clear any stored error message
    error_msg = session.pop('login_error', None)
    return render_template('login.html', error=error_msg)
# -------- REGISTER --------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            name = request.form.get('name')

            # Check existing email/username
            if User.query.filter_by(email=email).first():
                flash('Email sudah terdaftar!', 'error')
                return render_template('register.html')
            
            if User.query.filter_by(username=username).first():
                flash('Username sudah digunakan!', 'error')
                return render_template('register.html')

            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password),
                name=name,
                role='user'  # Default role is user
            )

            db.session.add(new_user)
            db.session.commit()
            
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('auth_bp.login'))

        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan saat registrasi.', 'error')
            
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

