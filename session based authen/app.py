from functools import wraps
import uuid
from flask import Flask, g, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

db=SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(256), nullable=False)

class session(db.Model):
    id = db.Column(db.String(256), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    expire_at = db.Column(db.DateTime, nullable=False)

with app.app_context():
    db.create_all()    


def login_required(f):
    @wraps(f) 
    def decorated(*args, **kwargs):
        session_id = request.cookies.get("session_id")
        if not session_id:
            return jsonify({"message":"Missing session"})
        user_session= session.query.filter_by(id=session_id).first()
        if not user_session or user_session.expire_at < datetime.utcnow():
            return jsonify({"message":"Unothorized"}),401
        g.user_id=user_session.user_id
        return f(*args, **kwargs)
    return decorated


@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    exist_user = user.query.filter_by(username=username).first()
    if exist_user:
        return jsonify ({"message":"user already exist"})
    
    password_hash=generate_password_hash(password)
    new_user = user(username=username, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"User added successfully"}),201    

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    User = user.query.filter_by(username=username).first()
    if not User:
        return jsonify({"message":"Invalid username"}),401
    if not check_password_hash(User.password, password):
        return jsonify({"message":"Invalid Password"}),401
    
    session_id=str(uuid.uuid4())
    exire_at= datetime.utcnow() + timedelta(minutes=5)

    new_session = session(id=session_id, user_id=User.id, expire_at=exire_at)
    db.session.add(new_session)
    db.session.commit()

    response=make_response(jsonify({"meassage":"Login Successfull"}),200)
    response.set_cookie("session_id", session_id,expires=exire_at, httponly=True)

    return response


@app.route("/profile", methods=["GET"])
@login_required
def profile():
    current_user = user.query.get(g.user_id)
    return jsonify({"message":"user profile","username":current_user.username}),200

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session_id = request.cookies.get("session_id")
    Session = session.query.filter_by(id=session_id).first()

    if Session:
        db.session.delete(Session)
        db.session.commit()

    response = make_response(jsonify({"message":"Logout Successfully."}))
    return response    


if __name__ == "__main__":
    app.run(debug=True)