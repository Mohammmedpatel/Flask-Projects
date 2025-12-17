from functools import wraps
from flask import jsonify, request, g
import jwt
from app import app

def token_required(f):
    @wraps(f)
    def decorators(*args, **kwargs):
        token= request.cookies.get("token")

        if not token:
            return jsonify({"message":"Missing Token"})
    
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            g.user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"})
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"})


        return f(*args, **kwargs)
    
    return decorators