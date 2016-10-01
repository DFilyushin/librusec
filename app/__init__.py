from flask import Flask
from flask_sqlalchemy import SQLAlchemy


librusec = Flask(__name__, static_url_path='/static', static_path='/static')
librusec.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:qwerty@127.0.0.1/books'
db = SQLAlchemy(librusec)

from app import views
