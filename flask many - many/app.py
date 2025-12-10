from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///one_to_many.db"

db = SQLAlchemy(app)

user_subject = db.Table(
    "user_subject",
    db.Column("user_id", db.Integer(), db.ForeignKey('user.id'), primary_key=True),
    db.Column("subject_id", db.Integer(), db.ForeignKey('subject.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable=False)  
    email = db.Column(db.String(20), nullable=False) 
    password = db.Column(db.String(20), nullable=False)  

    subjects = db.relationship("Subject", secondary=user_subject, backref="user")

    def __repr__(self):
        return f"<User:{self.username}>"

class Subject(db.Model):
    id = db.Column(db.Integer(), primary_key=True) 
    subject_name = db.Column(db.String(20), nullable=False) 

    def __repr__(self):
        return f"<Subject:{self.subject_name}>"

with app.app_context():
    db.create_all()