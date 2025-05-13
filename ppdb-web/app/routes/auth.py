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
        username = request.form.get('username')
        email = request.form.get('email')  # <- Pastikan ini tidak None
        password = request.form.get('password')
        name = request.form.get('name')

        # Tambahkan validasi
        if not email or not username or not password:
            flash("Semua field wajib diisi!", "danger")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            name=name
        )
        db.session.add(user)
        db.session.commit()
        flash("Pendaftaran berhasil", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# -------- LOGOUT --------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))
