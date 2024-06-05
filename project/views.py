from flask import Blueprint, render_template
from flask_login import login_user, logout_user, login_required, current_user
views = Blueprint('views',__name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html",user = current_user)

@views.route('/home')
@login_required
def homePage():
    return render_template("home.html")
