from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.validators import ValidationError

class registrationForm(FlaskForm):

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired(), EqualTo('pass_confirm', message='Password did not match!!')])
    pass_confirm = PasswordField('confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_username_stud(self, field):
        if student.query.filter_by(username=field.data).first():
            raise ValidationError("Password already there !!!")

    def check_username_rec(self, field):
        if recruiter.query.filter_by(username=field.data).first():
            raise ValidationError("Password already there !!!")

    def check_username_comp(self, field):
        if company.query.filter_by(username=field.data).first():
            raise ValidationError("Password already there !!!")


class loginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('LogIn')

class companyappr(FlaskForm):
    companyname = StringField('Company Name :',validators=[DataRequired()])
    companyinfo = TextAreaField('Type The Company Info :',validators=[DataRequired()])
    submit =SubmitField('requst approval')

class companylisthere(FlaskForm):
    compName = StringField('companyname',validators=[DataRequired()])
    compinfo = StringField( 'company info',validators=[DataRequired()])

class predicform(FlaskForm):
    label1 = StringField('10TH', validators=[DataRequired()])
    label2 = StringField('12TH', validators=[DataRequired()])
    label3 = StringField('DEGREE%', validators=[DataRequired()])
    label4 = StringField('Etest%', validators=[DataRequired()])
    label5 = StringField('MBA%', validators=[DataRequired()])
    label6 = StringField('GENDER', validators=[DataRequired()])
    label7 = StringField('ARTS', validators=[DataRequired()])
    label8 = StringField('COMMERCE', validators=[DataRequired()])
    label9 = StringField('SCIENCE', validators=[DataRequired()])
    label10 = StringField('work_xp', validators=[DataRequired()])
    label11 = StringField('mba_spl', validators=[DataRequired()])
    submit = SubmitField("PREDICT")
