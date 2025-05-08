from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db

main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/")
@login_required
def index():
    # Contoh: Menampilkan data siswa (Student) jika model Student ada
    from app.models import Student  # Lazy import
    students = Student.query.all()
    return render_template("index.html", students=students)

@main_bp.route('/add_student', methods=['POST'])
@login_required
def add_student():
    from app.models import Student  # Lazy import
    
    # Validasi input
    name = request.json.get('name')
    email = request.json.get('email')
    if not name or not email:
        return jsonify(success=False, error="Name and Email are required"), 400
    
    new_student = Student(
        name=name,
        email=email
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify(success=True)

@main_bp.route('/update_student/<int:student_id>', methods=['POST'])
@login_required
def update_student(student_id):
    from app.models import Student  # Lazy import
    student = Student.query.get_or_404(student_id)
    
    student.name = request.json.get('name', student.name)
    student.email = request.json.get('email', student.email)
    db.session.commit()
    return jsonify(success=True)

@main_bp.route('/delete_student/<int:student_id>', methods=['DELETE'])
@login_required
def delete_student(student_id):
    from app.models import Student  # Lazy import
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify(success=True)

@main_bp.route('/student/<int:student_id>')
@login_required
def get_student(student_id):
    from app.models import Student  # Lazy import
    student = Student.query.get_or_404(student_id)
    return jsonify({
        'id': student.id,
        'name': student.name,
        'email': student.email
    })