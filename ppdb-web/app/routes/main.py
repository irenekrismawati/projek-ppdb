from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Pendaftaran, Sekolah

main_bp = Blueprint('main_bp', __name__)

# -------- Halaman Utama (Publik) --------
@main_bp.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@main_bp.route('/daftar', methods=['GET', 'POST'])
def daftar():
    if request.method == 'POST':
        nama = request.form.get('nama')
        asal_sekolah = request.form.get('asal_sekolah')
        no_hp = request.form.get('no_hp')
        pilihan_jurusan = request.form.get('pilihan_jurusan')
        # Tambahkan validasi jika perlu
        if nama and asal_sekolah and no_hp and pilihan_jurusan:
            pendaftaran = Pendaftaran(
                nama=nama,
                asal_sekolah=asal_sekolah,
                no_hp=no_hp,
                pilihan_jurusan=pilihan_jurusan
            )
            db.session.add(pendaftaran)
            db.session.commit()
            flash('Pendaftaran berhasil! Kami akan menghubungi Anda.', 'success')
        else:
            flash('Semua field harus diisi!', 'error')
        return redirect(url_for('main_bp.daftar'))
    return render_template('daftar.html')

# -------- Dashboard User (Harus Login) --------
@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Ambil daftar pendaftaran yang terkait dengan user yang sedang login
    pendaftarans = Pendaftaran.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", current_user=current_user, pendaftarans=pendaftarans)
