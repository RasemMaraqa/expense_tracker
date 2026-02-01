from flask import Blueprint, request, jsonify , session , render_template, flash , redirect , url_for
from models import User
import jwt
from extensions.db import DB as db
from datetime import datetime, timedelta
from flask import current_app


login_route = Blueprint('login', __name__)







@login_route.route("/login" , methods=["GET", "POST"])
def login():
    user_id = session.get("user_id")
    if session.get("user_id"):
        return redirect(url_for("user.user_page", id=session["user_id"]))
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        
        
        if not email or not password:
            flash("Email and password required", "error")
            return render_template("login.html") , 400
        
        
        
        found_user = db.session.query(User).filter_by(email=email).first()
        
        
        if (not found_user) or (password != found_user.password):
        
            flash("invalid inputs" , "error")
            return render_template("./login.html") , 401
        
        session.clear()
        session["user_id"] = found_user.id
        session["username"] = found_user.username
        session.permanent = True

        return redirect(url_for("user.user_page", id=found_user.id))

    return render_template("login.html")
            
        
@login_route.route("/logout", methods=["POST"])
def logout():
    session.clear()         
    return redirect(url_for("login.login"))

    