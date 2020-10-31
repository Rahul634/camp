from newmyproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user_stud(user_id):
    return student.query.get(user_id)


@login_manager.user_loader
def load_user_comp(user_id):
    return company.query.get(user_id)


class student(db.Model, UserMixin):
    __tablename__ = 'STUDENT'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password_stud(self, password):
        return check_password_hash(self.password_hash, password)


class company(db.Model, UserMixin):
    __tablename__ = 'COMPANY'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password_comp(self, password):
        return check_password_hash(self.password_hash, password)


class companyApprovedonly(db.Model, UserMixin):
    __tablename__ = 'APPRCOMPANY'
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(64), unique=True, index=True)
    companyinfo = db.Column(db.String(64))

    def __init__(self, companyname, companyinfo):
        self.companyname = companyname
        self.companyinfo = companyinfo


db.create_all()