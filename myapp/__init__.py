from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///xsocial_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ILoveCODING168'  # os.getenv('SECRET_KEY', 'default_secret_key')

BASE_FOLDER_PATH = 'D:\\2024_Content Editor'
# Initialize the database
db = SQLAlchemy(app)

from myapp import route

with app.app_context():
    db.create_all()
