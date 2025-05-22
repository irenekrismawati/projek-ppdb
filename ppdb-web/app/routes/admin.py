from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.models import db, User, Pendaftaran
from app.routes.auth import admin_required
from functools import wraps
import os

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

@admin_bp.route('/documents/<int:pendaftaran_id>')
@login_required
@admin_required
def get_documents(pendaftaran_id):
    try:
        pendaftaran = Pendaftaran.query.get_or_404(pendaftaran_id)
        
        # Mendapatkan path upload folder dari konfigurasi
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # Membuat URL untuk setiap dokumen
        documents = {
            'ijazah': None,
            'kartu_keluarga': None,
            'akta_kelahiran': None
        }
        
        # Cek dan generate URL untuk setiap dokumen
        if pendaftaran.ijazah and os.path.exists(os.path.join(upload_folder, pendaftaran.ijazah)):
            documents['ijazah'] = url_for('static', filename=f'uploads/{pendaftaran.ijazah}')
            
        if pendaftaran.kartu_keluarga and os.path.exists(os.path.join(upload_folder, pendaftaran.kartu_keluarga)):
            documents['kartu_keluarga'] = url_for('static', filename=f'uploads/{pendaftaran.kartu_keluarga}')
            
        if pendaftaran.akta_kelahiran and os.path.exists(os.path.join(upload_folder, pendaftaran.akta_kelahiran)):
            documents['akta_kelahiran'] = url_for('static', filename=f'uploads/{pendaftaran.akta_kelahiran}')
        
        return jsonify(documents)
        
    except Exception as e:
        current_app.logger.error(f"Error fetching documents: {str(e)}")
        return jsonify({'error': 'Gagal memuat dokumen'}), 500