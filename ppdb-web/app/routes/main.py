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
        # Ambil semua field dari form
        nama = request.form.get('nama')
        nisn = request.form.get('nisn')           # Tambahkan ini
        asal_sekolah = request.form.get('asal_sekolah')
        alamat = request.form.get('alamat')       # Tambahkan ini
        no_hp = request.form.get('no_hp')
        pilihan_jurusan = request.form.get('pilihan_jurusan')

        # Cek jika user login, isi user_id, jika tidak, user_id=None
        user_id = current_user.id if current_user.is_authenticated else None

        # Validasi semua field required
        if all([nama, nisn, asal_sekolah, alamat, no_hp, pilihan_jurusan]):
            pendaftaran = Pendaftaran(
                nama=nama,
                nisn=nisn,              # Tambahkan ini
                asal_sekolah=asal_sekolah,
                alamat=alamat,          # Tambahkan ini
                no_hp=no_hp,
                pilihan_jurusan=pilihan_jurusan,
                user_id=user_id
            )
            db.session.add(pendaftaran)
            db.session.commit()
            flash('Pendaftaran berhasil! Kami akan menghubungi Anda.', 'success')
        else:
            flash('Semua field harus diisi!', 'error')
        return redirect(url_for('main_bp.daftar'))
    return render_template('daftar.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    pendaftarans = Pendaftaran.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', 
        current_user=current_user,
        pendaftarans=pendaftarans
    )
