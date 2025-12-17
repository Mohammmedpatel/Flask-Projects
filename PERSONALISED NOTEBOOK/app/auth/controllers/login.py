from flask import jsonify, make_response, request, g
from flask_restful import Resource
from datetime import datetime, timedelta
from app.auth.models import User
import jwt
from app import app


class LoginView(Resource):

    def post(self):
        credentials= request.get_json()

        user= User.query.filter_by(username=credentials["username"]).first()

        if not user:
            return {"message": "Invalid username"}, 401
        
        if not user.verify_password(credentials["password"]):
            return {"message": "Invalid password"}, 401
        
        expire_at= datetime.utcnow()+ timedelta(minutes=30)

        token= jwt.encode(
            {
                "user_id":user.id,
                "email":user.email,
                "exp":expire_at
            },
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )

        response= make_response(jsonify({"message":"Login Successfull"}))
        response.set_cookie("token",token,expires=expire_at)

        return response