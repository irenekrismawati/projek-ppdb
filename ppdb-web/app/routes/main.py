from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import db, User, Pendaftaran, PaymentRequest
from werkzeug.utils import secure_filename
import os

main_bp = Blueprint('main_bp', __name__)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@main_bp.route('/')
def index():
    """Route for the home page"""
    return render_template('index.html')

from sqlalchemy.exc import IntegrityError

@main_bp.route('/daftar', methods=['POST'])
@login_required
def daftar():
    nisn = request.form.get('nisn')
    
    # Check if NISN already exists
    existing_registration = Pendaftaran.query.filter_by(nisn=nisn).first()
    if existing_registration:
        flash('NISN sudah terdaftar dalam sistem. Mohon periksa kembali NISN Anda.', 'error')
        return redirect(url_for('main_bp.dashboard'))

    try:
        pendaftaran = Pendaftaran(
            nama=request.form.get('nama'),
            nisn=nisn,
            asal_sekolah=request.form.get('asal_sekolah'),
            alamat=request.form.get('alamat'),
            no_hp=request.form.get('no_hp'),
            pilihan_jurusan=request.form.get('pilihan_jurusan'),
            status='pending',
            user_id=current_user.id
        )
        db.session.add(pendaftaran)
        db.session.commit()
        flash('Pendaftaran berhasil dikirim!', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Error: NISN sudah terdaftar', 'error')
    
    return redirect(url_for('main_bp.dashboard'))
    return render_template('daftar.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    pendaftarans = Pendaftaran.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', 
        current_user=current_user,
        pendaftarans=pendaftarans
    )

@main_bp.route('/profile')
@login_required
def profile():
    pendaftaran = Pendaftaran.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', pendaftaran=pendaftaran)

@main_bp.route('/upload-documents', methods=['POST'])
@login_required
def upload_documents():
    if request.method == 'POST':
        # Create upload folder if it doesn't exist
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', str(current_user.id))
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        allowed_extensions = {'pdf', 'png', 'jpg', 'jpeg'}
        files_uploaded = []
        
        # Handle each file upload
        for file_type in ['ijazah', 'kartu_keluarga', 'akta_kelahiran', 'foto']:
            if file_type in request.files:
                file = request.files[file_type]
                if file and file.filename and allowed_file(file.filename, allowed_extensions):
                    filename = secure_filename(f"{file_type}_{file.filename}")
                    file_path = os.path.join(upload_folder, filename)
                    file.save(file_path)
                    files_uploaded.append(file_type)

        if files_uploaded:
            flash(f'Berhasil mengupload {", ".join(files_uploaded)}', 'success')
        else:
            flash('Tidak ada file yang diupload', 'warning')
            
        return redirect(url_for('main_bp.dashboard'))

    return redirect(url_for('main_bp.dashboard'))
