from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Pendaftaran, Sekolah
from sqlalchemy.exc import IntegrityError

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
