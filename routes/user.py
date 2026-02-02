from flask import Flask ,Blueprint, request, jsonify , session , render_template, flash , redirect , url_for , abort
from models import User
from models import Expense
from datetime import datetime
import random
from decorators.decorators import login_required , admin_required
from extensions.db import DB as db



user_route = Blueprint('user', __name__)







    
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
        flash("Admin created" , "success")
        return redirect(url_for("login.login"))
    
@user_route.route("/add_expense" , methods=["POST"])
@login_required
def add_expense():
    
        user_f = db.session.get(User, session["user_id"])
        amount = request.form.get("amount")
        if not user_f:
            return "User dose'nt exist"
        data = request.get_json()
        if not data :
            return "No data provided"
        expense = Expense(
            description=data.get("description"),
            amount=float(data.get("amount")),
            user_id=user_f.id
        )
        db.session.add(expense)
        db.session.commit()
        return jsonify({
        "id": expense.id,
        "description": expense.description,
        "amount": expense.amount,
        "date": expense.date.strftime("%Y-%m-%d")
        }), 201
    
    
    
    
@user_route.route("/delete_expense/<int:expense_id>", methods=["DELETE"])
@login_required
def delete_expense(expense_id):
    user = db.session.get(User, session["user_id"])    
    if not user:
        return "User dose'nt exist"
    
    expense = db.session.query(Expense).filter_by(id = expense_id, user_id = user.id).first()
    if not expense:
        return "Expense dose'nt exist"
    db.session.delete(expense)
    db.session.commit()
    return "Expense deleted" 


@user_route.route("/delete_user/<int:i>", methods=["DELETE"])
@admin_required
def delete_user(i):
    user = db.session.get(User, i).first()
    if not user:
        return "User dose'nt exist"
    expenses = db.session.query(Expense).filter_by(user_id = i).all()
    for e in expenses: # i have deleted the expenses first cuz if i deleted the user first it will give an error something about foreign key constraint cuz user is parent table :)
        db.session.delete(e)
        db.session.delete(user)
  
        db.session.commit()
        return "User delete"



@user_route.route("/delete_expense/<int:userid>/<int:expense_id>")
@admin_required
def delete_expense_admin( userid,expense_id):
    user = db.session.get(User, userid)
    if not user:
        return "User dose'nt exist"
    
    
    expense = db.session.query(Expense).filter_by(id = expense_id, user_id = user.id).first()

    
    if not expense:
        return "Expense dose'nt exist"
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
            ]
            
        }
        for u in users
    ]
    return jsonify(users_data)
