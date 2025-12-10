from datetime import datetime, timedelta
from functools import wraps
import uuid
from flask import Flask, g, jsonify, make_response, request, session
from flask_sqlalchemy import SQLAlchemy
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///jwtuser.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.config["SECRET_KEY"]="Mohammed"

db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(256), nullable=False)

with app.app_context():
    db.create_all()    

def token_required(f):
    @wraps(f) 
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return jsonify({"message":"Missing token"})
        
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            g.user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message":"Token has expired."}),401
        except jwt.InvalidTokenError:
            return jsonify({"message":"Invalid token."}),401

        return f(*args, **kwargs)
    return decorated

@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    exist_user = User.query.filter_by(username=username).first()
    if exist_user:
        return jsonify ({"message":"user already exist"})
    
    password_hash=generate_password_hash(password)
    new_user = User(username=username, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"User added successfully"}),201    

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message":"Invalid username"}),401
    if not check_password_hash(user.password, password):
        return jsonify({"message":"Invalid Password"}),401
    
    expire_at= datetime.utcnow() + timedelta(minutes=5)

    token = jwt.encode(
        {
            "user_id":user.id,
            "username":user.username,
            "exp": expire_at
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    response=make_response(jsonify({"meassage":"Login Successfull"}),200)
    response.set_cookie("token", token, expires=expire_at, httponly=True)

    return response

@app.route("/profile", methods=["GET"])
@token_required
def profile():
    current_user = User.query.get(g.user_id)
    return jsonify({"message":"user profile","username":current_user.username}),200

@app.route("/logout", methods=["GET"])
@token_required
def logout():
    response = make_response(jsonify({"message":"Logout Successfully"}),200)
    response.delete_cookie("token")
    return response


if __name__=="__main__":
    app.run(debug=True)
