from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .. import db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Debug print
        print(f"Login attempt - Username: {username}")
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                print(f"Login successful for user: {username}")
                flash('Login berhasil!', 'success')
                return redirect(url_for('main_bp.dashboard'))
            else:
                print(f"Invalid password for user: {username}")
                flash('Password salah!', 'error')
        else:
            print(f"User not found: {username}")
            flash('Username tidak ditemukan!', 'error')
    
    return render_template('login.html')