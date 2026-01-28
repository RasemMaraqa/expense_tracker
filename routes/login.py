from flask import Blueprint, request, jsonify , session , render_template, flash
from models import User




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
            
        


    