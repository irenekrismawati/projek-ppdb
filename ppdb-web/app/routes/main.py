from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import db, User, Pendaftaran, PaymentRequest
from werkzeug.utils import secure_filename
import os
from datetime import datetime

main_bp = Blueprint('main_bp', __name__)

UPLOAD_FOLDER = 'app/static/uploads/payments'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/')
def index():
    """Route for the home page"""
    return render_template('index.html')

from sqlalchemy.exc import IntegrityError

@main_bp.route('/daftar', methods=['POST'])
@login_required
def daftar():
    if request.method == 'POST':
        try:
            pendaftaran = Pendaftaran(
                user_id=current_user.id,
                nama=request.form['nama'],
                nisn=request.form['nisn'],
                tempat_lahir=request.form['tempat_lahir'],
                tanggal_lahir=datetime.strptime(request.form['tanggal_lahir'], '%Y-%m-%d'),
                jenis_kelamin=request.form['jenis_kelamin'],
                agama=request.form['agama'],
                alamat=request.form['alamat'],  # Pastikan field ini ada
                rt_rw=request.form['rt_rw'],
                no_hp=request.form['no_hp'],
                email=request.form['email'],
                nama_ayah=request.form['nama_ayah'],
                agama_ayah=request.form['agama_ayah'],
                pekerjaan_ayah=request.form['pekerjaan_ayah'],
                nama_ibu=request.form['nama_ibu'],
                agama_ibu=request.form['agama_ibu'],
                pekerjaan_ibu=request.form['pekerjaan_ibu'],
                asal_sekolah=request.form['asal_sekolah'],
                npsn_sekolah=request.form['npsn_sekolah'],
                pilihan_jurusan=request.form['pilihan_jurusan']
            )
            
            db.session.add(pendaftaran)
            db.session.commit()
            
            flash('Pendaftaran berhasil!', 'success')
            return redirect(url_for('main_bp.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
            return redirect(url_for('main_bp.daftar'))

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

@main_bp.route('/submit-payment', methods=['POST'])
@login_required
def submit_payment():
    if 'payment_proof' not in request.files:
        flash('Tidak ada file yang dipilih', 'error')
        return redirect(url_for('main_bp.dashboard'))
        
    file = request.files['payment_proof']
    
    if file.filename == '':
        flash('Tidak ada file yang dipilih', 'error')
        return redirect(url_for('main_bp.dashboard'))
        
    if file and allowed_file(file.filename):
        try:
            # Create upload directory if it doesn't exist
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            # Generate secure filename with timestamp
            filename = secure_filename(f"payment_{current_user.id}_{int(datetime.now().timestamp())}{os.path.splitext(file.filename)[1]}")
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            
            # Save file
            file.save(file_path)
            
            # Update payment status
            pendaftaran = Pendaftaran.query.filter_by(user_id=current_user.id).first()
            pendaftaran.payment_status = 'pending'
            pendaftaran.payment_proof = filename
            pendaftaran.payment_date = datetime.now()
            
            db.session.commit()
            
            flash('Bukti pembayaran berhasil diunggah. Mohon tunggu verifikasi admin.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
            
        return redirect(url_for('main_bp.dashboard'))
    
    flash('Format file tidak didukung', 'error')
    return redirect(url_for('main_bp.dashboard'))
