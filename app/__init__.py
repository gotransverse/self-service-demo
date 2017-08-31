import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, SECRET_KEY, MAIL_USERNAME, prodURLDefault, \
    MAIL_PASSWORD

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
app.secret_key = SECRET_KEY
app.prodURLDefault = prodURLDefault

from app import views, models
