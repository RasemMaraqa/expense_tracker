from flask import Flask ,Blueprint, request, jsonify , session



user_route = Blueprint('user', __name__)

@user_route.route("/user" , methods=["GET", "POST"])
def userpage():
    return jsonify({"message": "User route works!"})
    
    
