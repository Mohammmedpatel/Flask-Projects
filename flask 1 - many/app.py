from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///one_to_many.db"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)  
    username = db.Column(db.String(20), nullable=False) 
    email = db.Column(db.String(20), nullable=False)  
    password = db.Column(db.String(20), nullable=False)  

    education_details = db.relationship(
        "EducationDetails",
        backref="user",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<User:{self.username}>"

class EducationDetails(db.Model):
    id = db.Column(db.Integer(), primary_key=True) 
    institute_name = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(20), nullable=False) 
    passing_year = db.Column(db.String(10), nullable=False) 

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<EducationDetails:{self.user_id}>"

with app.app_context():
    db.create_all()