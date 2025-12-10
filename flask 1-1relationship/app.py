from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///one_to_one.db"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True) 
    username = db.Column(db.String(20), nullable=False) 
    email = db.Column(db.String(20), nullable=False)  
    password = db.Column(db.String(20), nullable=False)  

    personal_details = db.relationship(
        "PersonalDetails",
        backref="user",
        cascade="all, delete",
        uselist=False
    )

    def __repr__(self):
        return f"<User:{self.username}>"

class PersonalDetails(db.Model):
    id = db.Column(db.Integer(), primary_key=True) 
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)  

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), unique=True)

    def __repr__(self):
        return f"<PersonalDetails:{self.user_id}>"

with app.app_context():
    db.create_all()