from newmyproject import db, app
from flask import render_template, request, url_for, flash, abort, redirect,Flask
from flask_login import login_user, login_required, logout_user
from newmyproject.models import student, company, companyApprovedonly
from newmyproject.forms import loginForm, registrationForm, companyappr, predicform, companylisthere
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import numpy as np
import matplotlib as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

place = pd.read_csv("place.csv")
place.isnull().sum()
place = place.fillna(0)
place.isnull().sum()
sex = pd.get_dummies(place["gender"], drop_first=True)
place = pd.concat([place.drop("gender", axis=1), sex], axis=1)
place.isnull().sum()
board = pd.get_dummies(place["ssc_b"], drop_first=True)
place = pd.concat([place.drop("ssc_b", axis=1), board], axis=1)
stream = pd.get_dummies(place["hsc_s"])
place = pd.concat([place.drop("hsc_s", axis=1), stream], axis=1)
exp = pd.get_dummies(place["workex"], drop_first=True)
place = pd.concat([place.drop("workex", axis=1), exp], axis=1)
place.drop("Others", axis=1)
place = place.drop("Others", axis=1)
place = place.drop("hsc_b", axis=1)
sa = pd.get_dummies(place["degree_t"], drop_first=True)
place = pd.concat([place.drop("degree_t", axis=1), sa], axis=1)
special = pd.get_dummies(place["specialisation"], drop_first=True)
place = pd.concat([place.drop("specialisation", axis=1), special], axis=1)
pla = pd.get_dummies(place["status"])
place = pd.concat([place.drop("status", axis=1), pla], axis=1)
place = place.drop("sl_no", axis=1)
place = place.drop("Not Placed", axis=1)
place = place.drop("salary", axis=1)
place = place.rename(
    columns={"ssc_p": "10th_p", "hsc_p": "12th_p", "Yes": "work_exp", "M": "gender", "Mkt&HR": "mba_spl"})
place = place.drop("Others", axis=1)
place = place.drop("Sci&Tech", axis=1)
X = place.drop("Placed", axis=1)
y = place["Placed"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)
logmodel = LogisticRegression(max_iter=5000)
logmodel.fit(X_train, y_train)
predictions = logmodel.predict(X_test)

import pickle

pickle.dump(logmodel, open('model101.pkl', 'wb'))
modelling = pickle.load(open('model101.pkl', 'rb'))


@app.route("/")
# this route is will (STUDENT,COMPANY,RECRUITER TABS IN PANEL)
def home():
    return render_template('home.html')


@app.route("/welcome/studant")
# welcome(name of user) and nav of selected field

def welcome_stud():
    return render_template('welcome_stud.html')


@app.route("/welcome/company")
# welcome(name of user) and nav of selected field
def welcome_comp():
    return render_template('welcome_comp.html')


@app.route("/logout")
# logout for all users
def logout():
    logout_user()
    flash("you are logged out !!")
    return redirect(url_for('home'))


@app.route("/login/student", methods=['POST', 'GET'])
# login for student username and password
def studlogin():
    form_new = loginForm()
    if form_new.validate_on_submit():
        stud = student.query.filter_by(username=form_new.username.data).first()
        if stud.check_password_stud(form_new.password.data):
            login_user(stud)
            flash("logged in succesfully!!!")
            return redirect(url_for('welcome_stud'))

    return render_template('login_stud.html', form_new=form_new)


@app.route("/login/company", methods=['GET', 'POST'])
# login for student username and password
def complogin():
    form = loginForm()
    if form.validate_on_submit():
        comp = company.query.filter_by(username=form.username.data).first()
        if comp.check_password_comp(form.password.data):
            login_user(comp)
            return redirect(url_for('welcome_comp'))

    return render_template('login_comp.html', form=form)


@app.route("/register/student", methods=['GET', 'POST'])
# register student
def register_stud():
    form = registrationForm()
    if form.validate_on_submit():
        stud = student(username=form.username.data, password=form.password.data)
        db.session.add(stud)
        db.session.commit()
        flash("thanks for registering")
        return redirect(url_for('studlogin'))

    return render_template('register_stud.html', form=form)


@app.route("/register/company", methods=['GET', 'POST'])
# register student
def register_comp():
    form = registrationForm()
    if form.validate_on_submit():
        comp = company(username=form.username.data, password=form.password.data)
        db.session.add(comp)
        db.session.commit()
        flash("thanks for registering")
        return redirect(url_for('complogin'))

    return render_template('register_comp.html', form=form)


# append companyname : companyinfo
@app.route("/prediction/student", methods=['GET', 'POST'])
# commerce=10,science=01,arts =00
def prediction_stud():
    form = predicform()
    if form.validate_on_submit():
        label01 = form.label1.data
        label02 = form.label2.data
        label03 = form.label3.data
        label04 = form.label4.data
        label05 = form.label5.data
        label06 = form.label6.data
        label07 = form.label7.data
        label08 = form.label8.data
        label09 = form.label9.data
        label10 = form.label10.data
        label11 = form.label11.data
        x = [label01, label02, label03, label04, label05, label06, label07, label08, label09, label10, label11]
        inputVar = pd.DataFrame([x], columns=['10th_p', '12th_p', 'degree_p', 'etest_p', 'mba_p', 'gender', 'Arts',
                                              'Commerce', 'Science', 'work_xp', 'mba_spl'], dtype=float)
        prediction = logmodel.predict(inputVar)
        if prediction == 0:
            return render_template('sorry.html')
        else:
            return redirect(url_for('company_list'))

    return render_template('predict_stud.html', form=form)


@app.route("/list/company", methods=['GET', 'POST'])
def company_list():
    form = companylisthere()
    allcomps = companyApprovedonly.query.all()
    return render_template("company_list.html", form=form, allcomp=allcomps)


@app.route("/company/req", methods=['POST', 'GET'])
def company_req():
    form = companyappr()
    if form.validate_on_submit():
        comp = companyApprovedonly(companyname=form.companyname.data, companyinfo=form.companyinfo.data)
        db.session.add(comp)
        db.session.commit()

        return redirect(url_for("welcome_comp"))

    return render_template("req_appr.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)