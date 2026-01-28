from flask import Blueprint, request, jsonify , session , render_template, flash

home_route = Blueprint('home', __name__)

@home_route.route("/", methods=["GET"])
def homepage():
    return render_template("home.html")
