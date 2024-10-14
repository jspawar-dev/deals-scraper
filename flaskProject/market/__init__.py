from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'DATABASE_URI'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'SECRET_KEY'
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login_page'
    login_manager.login_message_category = 'info'
    with app.app_context():
        from . import routes
        from . import models
        db.create_all()

    return app

