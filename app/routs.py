from app import app, db, bcrypt
from flask import render_template, url_for, send_from_directory, request, redirect, flash, make_response, abort
from flask_login import login_required, login_user, logout_user, current_user
from app.db_classes import User, Student
from app.forms import LoginForm
from app.utils import class_name_from_code

CLASSES = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VII', '1.A', '2.A', '3.A', '4.A', '1.B', '2.B', '3.B', '4.B']

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/edit')
def edit():
    return render_template('edit.html', classes=CLASSES)

@app.route('/edit_class/<class_name>')
@app.route('/edit/class/<class_name>')
def edit_class(class_name):
    students = [student for student in Student.query.all() if class_name_from_code(student.code) == class_name]
    return render_template('edit_class.html', students=students)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('/')
        flash('Přihlášení se nezdařilo - zkontrolujte jméno a heslo', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))