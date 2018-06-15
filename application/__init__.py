import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Flask application
app = Flask(__name__)

# Database
if os.environ.get('HEROKU'):
	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
	app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

# Application functionality
from application import views
from application.users import models, views
from application.chats import models, views
from application.messages import models, views
from application.chatusers import models

# User authentication
from application.users.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users_login"
login_manager.login_message = "Please login to use this functionality"


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)


try:
	db.create_all()
except Exception:
	pass
