from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///user.db"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String(20),nullable=False)

with app.app_context():
    db.create_all()  

@app.route("/hello")
def home():
    return "hello"

@app.route("/add",methods=["POST"])
def add_stu():
    data = request.get_json()
    db.session.add(data)
    db.session.commit()
    return jsonify({"message":"Successfully added"})

if __name__=="__main__":
    app.run(debug=True)