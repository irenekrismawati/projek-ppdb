from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, Pendaftaran, Sekolah

main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/")
@login_required
def index():
    # Tampilkan daftar pendaftaran milik user yang sedang login
    pendaftarans = Pendaftaran.query.filter_by(user_id=current_user.id).all()
    return render_template("index.html", pendaftarans=pendaftarans)

@main_bp.route('/pendaftaran/<int:pendaftaran_id>')
@login_required
def view_pendaftaran(pendaftaran_id):
    # Tampilkan detail pendaftaran tertentu
    pendaftaran = Pendaftaran.query.get_or_404(pendaftaran_id)
    sekolah = Sekolah.query.get(pendaftaran.sekolah_id)
    return render_template("detail_pendaftaran.html", pendaftaran=pendaftaran, sekolah=sekolah)
