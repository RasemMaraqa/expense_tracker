from flask import Blueprint, request, render_template, redirect, url_for, flash
from models import User
from extensions.db import DB as db

signup_route = Blueprint("signup", __name__)

@signup_route.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            flash("All fields required", "error")
            return render_template("signup.html")

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "error")
            return render_template("signup.html")

        user = User(
            username=username,
            email=email,
            password=password  
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created! Please login.", "success")
        return redirect(url_for("login.login"))

    return render_template("signup.html")
