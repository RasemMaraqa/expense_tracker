from flask import Blueprint, request , session , render_template, flash , redirect , url_for
from models import User
from extensions.db import DB as db
from services import authenticate


login_route = Blueprint('login', __name__)







@login_route.route("/login" , methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("frontend.user_page"))
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        
        
        if not email or not password:
            flash("Email and password required", "error")
            return render_template("login.html") , 400
        
        
        
        found_user = authenticate(email,password)
        
        
        if (not found_user) :
        
            flash("invalid inputs" , "error")
            return render_template("./login.html") , 401
        
        session.clear()
        session["user_id"] = found_user.id
        session.permanent = True

        return redirect(url_for("frontend.user_page"))

    return render_template("login.html")
            
        
@login_route.route("/logout", methods=["POST"])
def logout():
    session.clear()         
    return redirect(url_for("login.login"))

    