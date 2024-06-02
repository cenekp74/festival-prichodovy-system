from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.Integer, unique=True, nullable=False)
    rfid = db.Column(db.String(10), unique=True)

class Prichod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.DateTime, default=datetime.now())
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))