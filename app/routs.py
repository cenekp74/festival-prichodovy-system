from app import app, db, bcrypt
from flask import render_template, url_for, send_from_directory, request, redirect, flash, make_response, abort
from flask_login import login_required, login_user, logout_user, current_user
from app.db_classes import User, Student, Prichod
from app.forms import LoginForm
from app.utils import class_name_from_code, search
import json
from datetime import datetime

CLASSES = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VII', '1.A', '2.A', '3.A', '4.A', '1.B', '2.B', '3.B', '4.B']
VCASNY_PRICHOD_LIMIT = datetime(2000, 1, 1, 8, 35).time()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

#region edit
@app.route('/edit')
@login_required
def edit():
    return render_template('edit/edit.html', classes=CLASSES)

@app.route('/edit_class/<class_name>')
@app.route('/edit/class/<class_name>')
@login_required
def edit_class(class_name):
    students = [student for student in Student.query.all() if class_name_from_code(student.code) == class_name]
    return render_template('edit/edit_class.html', students=students, classes=CLASSES, class_name=class_name)

@app.route('/edit/student/<student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    if not student_id.isdigit(): abort(500)
    student = Student.query.get(student_id)
    if not student: abort(404)
    if request.method == 'POST':
        rfid = request.form["rfid"]
        student.rfid = rfid
        db.session.commit()
    # v templatu edit_student.html zobrazuju i tridu studenta, proto musim queryinout vsechny zaky z dane tridy
    class_name = class_name_from_code(student.code)
    class_students = [student_ for student_ in Student.query.all() if class_name_from_code(student_.code) == class_name] # vsichni zaci z tridy daneho zaka
    return render_template('edit/edit_student.html', student=student, class_name=class_name, classes=CLASSES, students=class_students)

@app.route('/edit/search')
@login_required
def edit_search(): # funkce na vyhledavani jsou ruzny pro editovani a pro prohlizeni, protoze ve vysledcich musi byt jiny link
    query = request.args.get('q')
    results = set()
    if len(query) > 2:
        results = search(query)
    return render_template('edit/search_results.html', results=results)

@app.route('/write', methods=['GET', 'POST'])
@login_required
def write(): # fce na zapisovani prichodu - na GET proste vrati template, na POST zapise prichod a vrati odpoved
    if request.method == 'GET':
        return render_template('write/write.html')
    rfid = request.form.get("rfid")
    if not rfid: abort(500) # pokud v POST requestu neni argument rfid, je neplatny
    student = Student.query.filter_by(rfid=rfid).first()
    if not student:
        return 'STUDENT NENALEZEN'
    for prichod in Prichod.query.filter_by(student_id=student.id):
        if prichod.dt.date() == datetime.today().date(): return f'{student.name} <br> DUPLICITNÍ PŘÍCHOD - IGNORUJI'
    prichod = Prichod(student_id=student.id)
    db.session.add(prichod)
    db.session.commit()
    stat = 'ok' # podle tohohle bude mit cas prichodu barvicku
    time = datetime.now().time()
    if time > VCASNY_PRICHOD_LIMIT: stat = 'late'
    return render_template('write/write_response.html', student=student, time=time.strftime("%H:%M"), stat=stat)
#endregion edit

#region view
#endregion view

@app.post('/add') # post request na pridani studenta, pro ucely migrace ze starsi databaze. POZOR - je potreba nezapomenout zabezpecit (@login_required) !!
@login_required
def add():
    request_json = json.loads(request.json)
    name = request_json["name"]
    code = request_json["code"]
    rfid = None
    if "rfid" in request_json: # rfid je optional, student se muze pridat bez kodu cipu
        rfid = request_json["rfid"]
    student = Student(name=name, code=code, rfid=rfid)
    db.session.add(student)
    db.session.commit()
    return '200'

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