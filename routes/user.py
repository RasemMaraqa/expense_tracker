from flask import Flask ,Blueprint, request, jsonify , session , render_template, flash , redirect , url_for , abort
from models import User
from models import Expense
from datetime import datetime
import random
from auth.token import login_required , admin_required
from extensions.db import DB as db


user_route = Blueprint('user', __name__)

@user_route.route("/user/<int:id>" , methods=["GET", "POST"])
@admin_required
def userpage(id):
    
        user = User.query.get(session["user_id"])
        if not user:
            flash("User not found" , "error")
            return redirect(url_for("login.login")) 
        
        expenses = Expense.query.filter_by(user_id=user.id).all()
        expenses_data = [
            {
            "id": e.id,
            "description": e.description,
            "amount": e.amount,
            "date": e.date
        }
        for e in expenses
]
        return render_template(
        "user.html",
        user=user,
        expenses=expenses
    )


@user_route.route("/")
@user_route.route("/user")
@login_required
def redirect_to_page():
            
    user_id = User.query.get(session["user_id"])
    if not user_id:
        return redirect(url_for("login.login"))
    return redirect(url_for("user.user_page"))
    
@user_route.route("/user/page")
@login_required
def user_page():
        
        user = User.query.get(session["user_id"])
    
        expenses = Expense.query.filter_by(user_id=user.id).all()
        expenses_data = [
            {
            "id": e.id,
            "description": e.description,
            "amount": e.amount,
            "date": e.date
        }
        for e in expenses
]
        return render_template(
        "user.html",
        user=user,
        expenses=expenses
    )


    
@user_route.route("/init_user")
@login_required
def init_user():
        
        user = User(
        username= "User"+str(random.randint(1,1000)) ,
        email="test"+str(random.randint(1,1000))+"@test.com",
        password="1234"
        )
   
    
        db.session.add(user)
        db.session.commit()
        return "User created"


@user_route.route("/init_admin")
def init_admin():
        
        user = User(
        username= "rasem" ,
        email="rasemmaraqa@gmail.com",
        password="code"
        , is_admin=True
        )
   
    
        db.session.add(user)
        db.session.commit()
        return "admin created"
    
@user_route.route("/add_expense" , methods=["POST"])
@login_required
def add_expense():
    
        user_f = User.query.get(session["user_id"])
        amount = request.form.get("amount")
        if not user_f:
            return "User dosen't exist"
        expense = Expense(
            description=request.form.get("description"),
            amount=float(amount),
            user_id=user_f.id
        )
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for("user.user_page"))    

@user_route.route("/delete_user/<int:i>")
@admin_required
def delete_user(i):
    user = User.query.filter_by(id = i).first()
    if not user:
        return "User dosen't exist"
    expenses = Expense.query.filter_by(user_id=user.id).all()
    for e in expenses: # i have deleted the expenses first cuz if i deleted the user first it will give an error something about foreign key constraint cuz user is parent table :)
        db.session.delete(e)
        db.session.delete(user)
  
        db.session.commit()
        return "User delete"

@user_route.route("/delete_expense/<int:expense_id>", methods=["GET","POST"])
@login_required
def delete_expense(expense_id):
    user = User.query.get(session["user_id"])
    print(user)
    
    if not user:
        return "User dosen't exist"
    
    expense = Expense.query.filter_by(id = expense_id, user_id = user.id).first()
    if not expense:
        return "Expense dosen't exist"
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for("user.user_page"))    



@user_route.route("/delete_expense/<int:userid>/<int:expense_id>")
@admin_required
def delete_expense_admin( userid,expense_id):
    user = User.query.filter_by(id = userid).first()
    if not user:
        return "User dosen't exist"
    
    expense = Expense.query.filter_by(id = expense_id, user_id = userid).first()
    if not expense:
        return "Expense dosen't exist"
    db.session.delete(expense)
    db.session.commit()
    return "Expense deleted"




@user_route.route("/view")
@admin_required
def view_users():
    users = User.query.all()
    expenses = Expense.query.all()
    users_data = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "expenses": [
                {
                    "id": e.id,
                    "amount": e.amount,
                    "date": e.date
                }
                for e in expenses if e.user_id == u.id
            ],
            "password": u.password
        }
        for u in users
    ]
    return jsonify(users_data)
