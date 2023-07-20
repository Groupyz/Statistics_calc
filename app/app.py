from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from logger import init_logger


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
db = SQLAlchemy(app)
logger = init_logger()

from routes import *

with app.app_context():
    db.create_all()
