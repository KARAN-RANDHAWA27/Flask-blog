# Project/__init__.py
from flask import Flask
from .views import views
from .auth import auth
from project.db import db
from os import path
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_login import LoginManager
from .models import User

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'karan'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)  # Call the function to create the database

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def create_database(app):
    try:
        if not path.exists('project/' + DB_NAME):
            with app.app_context():
                try:
                    db.create_all()
                    print("Created Database")
                except Exception as e:
                    print(e,'oop')
    except Exception as e:
        print(e)
