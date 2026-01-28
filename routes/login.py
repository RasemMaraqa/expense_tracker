from flask import Blueprint, request, jsonify , session , render_template, flash , redirect , url_for
from models import User
import jwt
from datetime import datetime, timedelta
from flask import current_app



login_route = Blueprint('login', __name__)
@login_route.route("/login" , methods=["GET", "POST"])
def loginpage():
    if request.method == "POST":
        email = request.form.get['email']
        found_user = User.query.filter_by(email = email).first()
        if found_user and request.form.get['password'] == found_user.password:
            session['user_id'] = found_user.id
            return render_template("./login.html", username=found_user.username)
        else:
            flash("invalid inputs" , "error")
            return render_template("./login.html")
    else:
        if "user_id" in session:
            user = session["user"]
            flash(f"you are already logged in! , {user}", "info")
            return render_template("./user.html")

        return render_template("./login.html")
            
        

login_route = Blueprint('login', __name__)



@login_route.route("/login" , methods=["GET","POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("user.user_page", id=session["user_id"]))
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        if not email or not password:
            flash("Email and password required", "error")
            return render_template("login.html")
        found_user = User.query.filter_by(email = email).first()
        if found_user and request.form.get('pass') == found_user.password:
            session['user_id'] = found_user.id
            session["username"] = found_user.username
            return redirect(url_for("user.user_page", id=found_user.id))
        else:
            flash("invalid inputs" , "error")
            return render_template("./login.html")
    else:
        if "user_id" in session:
            user = session["user_id"]
            flash(f"you are already logged in! , {user}", "info")
            return render_template("./user.html")

        return render_template("./login.html")
            
        
@login_route.route("/logout")
def logout():
    session.clear()         
    return redirect(url_for("login.login"))

    