from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, Pendaftaran, Sekolah

main_bp = Blueprint('main_bp', __name__)

# -------- Halaman Utama - Daftar Pendaftaran User --------
@main_bp.route("/")
@login_required
def index():
    # Ambil daftar pendaftaran yang terkait dengan user yang sedang login
    pendaftarans = Pendaftaran.query.filter_by(user_id=current_user.id).all()
    
    return render_template("index.html", pendaftarans=pendaftarans)

# -------- Halaman Detail Pendaftaran --------
@main_bp.route('/pendaftaran/<int:pendaftaran_id>')
@login_required
def view_pendaftaran(pendaftaran_id):
    # Ambil data pendaftaran tertentu berdasarkan ID
    pendaftaran = Pendaftaran.query.get_or_404(pendaftaran_id)
    
    # Ambil data sekolah terkait pendaftaran
    sekolah = Sekolah.query.get(pendaftaran.sekolah_id)
    
    return render_template("detail_pendaftaran.html", pendaftaran=pendaftaran, sekolah=sekolah)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', current_user=current_user)