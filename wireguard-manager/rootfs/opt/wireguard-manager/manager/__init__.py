from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '6a598f99f0915fd9f158ae5597aad87d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/wg.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from manager import routes
