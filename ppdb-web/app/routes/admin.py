from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, User, Pendaftaran
from app.routes.auth import admin_required
from functools import wraps

# Define blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Add dashboard route
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    pendaftarans = Pendaftaran.query.all()
    return render_template('dashboard_admin.html', 
        pendaftarans=pendaftarans,
        current_user=current_user
    )

@admin_bp.route('/approve/<int:id>')
@login_required
@admin_required
def approve_pendaftaran(id):
    pendaftaran = Pendaftaran.query.get_or_404(id)
    pendaftaran.status = 'approved'
    db.session.commit()
    flash('Pendaftaran berhasil disetujui!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/reject/<int:id>')
@login_required
@admin_required
def reject_pendaftaran(id):
    pendaftaran = Pendaftaran.query.get_or_404(id)
    pendaftaran.status = 'rejected'
    db.session.commit()
    flash('Pendaftaran ditolak!', 'error')
    return redirect(url_for('admin.dashboard'))