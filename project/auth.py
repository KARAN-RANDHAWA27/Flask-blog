from flask import Blueprint,render_template,request,flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from project.db import db
from project.models import User
from flask_login import login_user,logout_user,login_required,current_user

auth = Blueprint('auth',__name__)

@auth.route('/',methods=['GET','POST'])
def loginPage():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Login Successfull", category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.homepage'))
            else:
                flash("Login Failed", category='error')
                return render_template("login.html",user=current_user)
        else:
            flash("Email does not exist", category='error')
            return redirect(url_for('auth.signUp'))
    return render_template("login.html",user = current_user)

@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Login Successfull", category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.homepage'))
            else:
                flash("Login Failed", category='error')
                return render_template("login.html",user=current_user)
        else:
            flash("Email does not exist", category='error')
            return redirect(url_for('auth.signUp'))
    return render_template("login.html",user = current_user)

@auth.route("/sign-up" , methods=['GET','POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('email')
        f_name = request.form.get('f_name')
        password = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email = email).first()
        if user:
            flash("Email Already Exist",category="error")
        elif len(email)<10:
            flash("Email must be valid", category='error')

        elif len(f_name)<3:
            flash("First name must be more than 3 characters", category='error')

        elif len(password)<8:
            flash("Password must be more than 8 characters", category='error')

        elif password != password2:
            flash("Password and confirm password did not match", category='error')

        else:
            new_user = User(email = email, f_name = f_name, password = generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash("Done", category='success')  
            return redirect(url_for('views.homepage'))      
    return render_template("signup.html",user = current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("logout.html",user = current_user)