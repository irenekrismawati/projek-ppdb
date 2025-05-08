from flask import Blueprint, render_template, request, redirect, url_for
from .forms import RegistrationForm
from .models import Student

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def index():
    return render_template('index.html')

@app_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            email=form.email.data,
            # Add other fields as necessary
        )
        student.save()  # Assuming a save method exists in the Student model
        return redirect(url_for('app_routes.index'))
    return render_template('register.html', form=form)