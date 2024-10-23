from app import app, db, bcrypt
from flask import render_template, url_for, send_from_directory, request, redirect, flash, make_response, abort, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from app.db_classes import User, Student, Prichod
from app.forms import LoginForm
from app.utils import class_name_from_code, search, get_students_by_class_name
import json
from datetime import datetime
from sqlalchemy import func

CLASSES = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', '1.A', '2.A', '3.A', '4.A', '3.B', '4.B'] # pro rok 23/24
VCASNY_PRICHOD_LIMIT = datetime(2000, 1, 1, 8, 35).time()
FESTIVAL_DNY = [datetime(2024, 12, 16).date(), datetime(2024, 12, 17).date(), datetime(2024, 12, 18).date()] # vyuzity ve view_student

# aby byla variable classes ve vsech templatech a nemusel jsem ji vzdycky jako blbecek pridavat
@app.context_processor
def inject_classes():
    return dict(classes=CLASSES)

# require login on all endpoints except login and static
@app.before_request
def require_login(): # POZOR - dela problemy pokud je v url double slash (coz se stava treba kdyz odkazuju na static a dam / na zacatku navic - napr. {{ url_for('static', filename='/css/main.css') }})
    if not current_user.is_authenticated and request.endpoint not in ['login', 'static']:
        return redirect(url_for('login'))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

#region edit
@app.route('/edit')
def edit():
    return render_template('edit/edit.html')

@app.route('/edit_class/<class_name>')
@app.route('/edit/class/<class_name>')
def edit_class(class_name):
    students = get_students_by_class_name(class_name)
    return render_template('edit/edit_class.html', students=students, class_name=class_name)

@app.route('/edit/student/<student_id>', methods=['GET', 'POST'])
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
    class_students = get_students_by_class_name(class_name)
    return render_template('edit/edit_student.html', student=student, class_name=class_name, students=class_students)

@app.route('/edit/search')
def edit_search(): # funkce na vyhledavani jsou ruzny pro editovani a pro prohlizeni, protoze ve vysledcich musi byt jiny link (fce vraci jiny template)
    query = request.args.get('q')
    results = set()
    if len(query) > 2:
        results = search(query)
    return render_template('edit/search_results.html', results=results)
#endregion edit

@app.route('/write', methods=['GET', 'POST'])
def write(): # fce na zapisovani prichodu - na GET proste vrati template, na POST zapise prichod a vrati odpoved
    if request.method == 'GET':
        return render_template('write/write.html', secondary_server=app.config["SECONDARY_SERVER"])
    rfid = request.form.get("rfid")
    if not rfid: abort(500) # pokud v POST requestu neni argument rfid, je neplatny
    student = Student.query.filter_by(rfid=rfid).first()
    if not student:
        return 'STUDENT NENALEZEN'
    if Prichod.query.filter_by(student_id=student.id).filter(func.date(Prichod.dt) == datetime.today().date()).first(): # func.date vytahle z datetime objektu date
        return f'{student.name} <br> DUPLICITNÍ PŘÍCHOD - IGNORUJI'
    prichod = Prichod(student_id=student.id)
    db.session.add(prichod)
    db.session.commit()
    stat = 'ok' # podle tohohle bude mit cas prichodu barvicku
    time = datetime.now().time()
    if time > VCASNY_PRICHOD_LIMIT: stat = 'late'
    return render_template('write/write_response.html', student=student, time=time.strftime("%H:%M"), stat=stat)

#region view
@app.route('/view')
def view():
    return render_template('view/view.html')

@app.route('/view/class')
def view_class():
    class_name = request.args.get("class")
    date = request.args.get("date")
    if not date or not class_name:
        flash('Vyberte prosím třídu a datum')
        return redirect(url_for('view'))
    students = get_students_by_class_name(class_name)
    prichody = {} # prichody studentu ve formatu {student_id: {"time":cas_prichodu, "stat":absence/pozndni/vcasny), "color":barvicka}}
    for student in students:
        prichod = Prichod.query.filter_by(student_id=student.id).filter(
            func.date(Prichod.dt) == date
        ).first() # tohle vytahne z databaze prichod studenta v dany den pokud existuje
        if not prichod:
            prichody[student.id] = {"time":"---", "stat":"absence", "color":"red"}
            continue
        stat = 'včasný' if prichod.dt.time() <= VCASNY_PRICHOD_LIMIT else 'pozdní'
        color = 'green' if stat == 'včasný' else 'yellow'
        prichody[student.id] = {"time":prichod.dt.time().strftime("%H:%M"), "stat": stat, "color":color}
    return render_template('view/view_class.html', students=students, prichody=prichody, date=datetime.strptime(date, "%Y-%m-%d").strftime("%d.%m.%Y"), class_name=class_name)

@app.route('/view/student/<student_id>')
def view_student(student_id):
    if not student_id.isdigit(): abort(500)
    student = Student.query.get(student_id)
    if not student: abort(404)
    prichody = [] # prichody studenta ve formatu [{"date":den, "time":cas_prichodu, "stat":absence/pozdni/vcasny, "color":barvicka}]
    for date in FESTIVAL_DNY:
        prichod = Prichod.query.filter_by(student_id=student.id).filter(
            func.date(Prichod.dt) == date
        ).first()
        if not prichod:
            prichody.append({"date":date, "time":"---", "stat":"absence", "color":"red"})
            continue
        stat = 'včasný' if prichod.dt.time() <= VCASNY_PRICHOD_LIMIT else 'pozdní'
        color = 'green' if stat == 'včasný' else 'yellow'
        prichody.append({"date":date, "time":prichod.dt.time().strftime("%H:%M"), "stat":stat, "color":color})
    return render_template('view/view_student.html', student=student, prichody=prichody)

@app.route('/view/search')
def view_search(): # funkce na vyhledavani jsou ruzny pro editovani a pro prohlizeni, protoze ve vysledcich musi byt jiny link (fce vraci jiny template)
    query = request.args.get('q')
    results = set()
    if len(query) > 2:
        results = search(query)
    return render_template('view/search_results.html', results=results)

@app.route('/view/json') # vrati vsechny prichody v databazi jako json - pro ucely zalohovani viz readme
def prichody_to_json():
    prichody_dict = [prichod.to_dict() for prichod in Prichod.query.all()]
    return jsonify(prichody_dict)
#endregion view

@app.post('/add') # post request na pridani studenta, hlavne pro ucely migrace ze starsi databaze
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
        #flash('Přihlášení se nezdařilo - zkontrolujte jméno a heslo', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))