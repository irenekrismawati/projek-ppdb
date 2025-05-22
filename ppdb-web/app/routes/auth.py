import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Pendaftaran
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
    # Clear any existing flash messages when accessing login page
    session.pop('_flashes', None)
    
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main_bp.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('main_bp.dashboard'))
        else:
            flash('Username atau password salah', 'error')
            
    return render_template('login.html')
# -------- REGISTER --------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Get form data
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            name = request.form.get('name')

            # Create user
            user = User(
                username=username,
                email=email,
                name=name,
                password=generate_password_hash(password),
                role='user'
            )
            db.session.add(user)
            db.session.commit()

            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('auth_bp.login'))

        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
            return redirect(url_for('auth_bp.register'))

    return render_template('register.html')
# -------- LOGOUT --------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah berhasil logout', 'success')
    return redirect(url_for('auth_bp.login'))