from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.models import db, User, Pendaftaran
from app.routes.auth import admin_required

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    print("Accessing admin dashboard...")  # Debug print
    pendaftarans = Pendaftaran.query.all()
    users = User.query.filter_by(role='user').all()
    print(f"Found {len(pendaftarans)} pendaftarans")  # Debug print
    return render_template('dashboard_admin.html',
        pendaftarans=pendaftarans,
        users=users
    )

@admin_bp.route('/approve/<int:id>')
@login_required
@admin_required
def approve_pendaftaran(id):
    pendaftaran = Pendaftaran.query.get_or_404(id)
    pendaftaran.status = 'approved'
    db.session.commit()
    flash('Pendaftaran berhasil disetujui!', 'success')
    return redirect(url_for('admin_bp.admin_dashboard'))

@admin_bp.route('/reject/<int:id>')
@login_required
@admin_required
def reject_pendaftaran(id):
    pendaftaran = Pendaftaran.query.get_or_404(id)
    pendaftaran.status = 'rejected'
    db.session.commit()
    flash('Pendaftaran ditolak!', 'error')
    return redirect(url_for('admin_bp.admin_dashboard'))
