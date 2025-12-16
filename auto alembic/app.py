from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:Patelmd%%4042400@localhost:3306/testalembic"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(20) , nullable = False)
    email = db.Column(db.String(30) , nullable = False , unique = True)
    phone = db.Column(db.String(10) , nullable = False , unique = True)

class Subject(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    subject_name = db.Column(db.String(20) , nullable = False)
