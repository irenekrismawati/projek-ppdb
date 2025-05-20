from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Pendaftaran, Payment
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

main_bp = Blueprint('main_bp', __name__)

# -------- Halaman Utama (Publik) --------
@main_bp.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

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
    if 'ijazah' not in request.files and \
       'kartu_keluarga' not in request.files and \
       'akta_kelahiran' not in request.files and \
       'foto' not in request.files:
        flash('Tidak ada file yang dipilih', 'error')
        return redirect(url_for('main_bp.dashboard'))

    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    uploaded_files = []
    
    for field in ['ijazah', 'kartu_keluarga', 'akta_kelahiran', 'foto']:
        file = request.files.get(field)
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(f"{current_user.id}_{field}_{file.filename}")
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            uploaded_files.append(field)

    if uploaded_files:
        flash(f'Berhasil mengupload {", ".join(uploaded_files)}', 'success')
    else:
        flash('Gagal mengupload dokumen', 'error')

    return redirect(url_for('main_bp.dashboard'))

@main_bp.route('/upload-payment', methods=['POST'])
@login_required
def upload_payment():
    if 'payment_proof' not in request.files:
        flash('Tidak ada file yang dipilih', 'error')
        return redirect(url_for('main_bp.dashboard'))

    file = request.files['payment_proof']
    if file.filename == '':
        flash('Tidak ada file yang dipilih', 'error')
        return redirect(url_for('main_bp.dashboard'))

    if file and allowed_file(file.filename):
        pendaftaran = Pendaftaran.query.filter_by(user_id=current_user.id).first()
        if not pendaftaran:
            flash('Data pendaftaran tidak ditemukan', 'error')
            return redirect(url_for('main_bp.dashboard'))

        filename = secure_filename(f"payment_{pendaftaran.id}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        payment = Payment(
            pendaftaran_id=pendaftaran.id,
            amount=500000,
            payment_method=request.form.get('payment_method'),
            payment_proof=filename,
            status='pending'
        )
        
        try:
            db.session.add(payment)
            db.session.commit()
            flash('Bukti pembayaran berhasil dikirim dan sedang diverifikasi', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Terjadi kesalahan saat mengirim bukti pembayaran', 'error')

    return redirect(url_for('main_bp.dashboard'))