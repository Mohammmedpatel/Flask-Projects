from flask import jsonify, request
from flask_restful import Resource
from app import db
from app.auth.models import User
from app.auth.serde import UserSchema

class SignUpView(Resource):
    
    def post(self):
        data=request.get_json()

        existing_user=User.query.filter_by(username=data["username"]).count()
        print("existing", existing_user)

        if existing_user:
            return jsonify({"message":"username already exist"})
        
        existing_email=User.query.filter_by(email=data["email"]).count()

        if existing_email:
            return jsonify({"message":"email already exist"})
        
        user=UserSchema().load(data)

        new_user= User(**user)
        
        db.session.add(new_user)
        db.session.commit()

        return user, 201
