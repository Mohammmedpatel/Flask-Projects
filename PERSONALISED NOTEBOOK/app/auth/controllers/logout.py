from flask import jsonify, make_response
from flask_restful import Resource


class LogOutView(Resource):
    
    def get(self):
        response= make_response(jsonify({"message":"Logout Successfully"}))
        response.delete_cookie('token')
        return response