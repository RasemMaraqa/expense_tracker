from flask import Flask ,Blueprint, request, jsonify , session
from models import User
from models import Expense
from datetime import datetime
import random
from extensions.db import DB as db


user_route = Blueprint('user', __name__)

@user_route.route("/user/<int:i>" , methods=["GET", "POST"])
def userpage(i):
    
        user = User.query.filter_by(id = i).first()
        if not user:
            return "User dosen't exist"
        else :
            expenses = Expense.query.filter_by(user_id=user.id).all()
            expenses_data = [
            {
            "id": e.id,
            "amount": e.amount,
            "date": e.date
        }
            for e in expenses
]
            return jsonify({ "username": user.username , "email": user.email , "expenses": expenses_data}) 
   

    
@user_route.route("/init_user")
def init_user():
        
        user = User(
        username= "User"+str(random.randint(1,1000)) ,
        email="test"+str(random.randint(1,1000))+"@test.com",
        password="1234"
        )
   
    
        db.session.add(user)
        db.session.commit()
        return "User created"
    
@user_route.route("/init_expense/<int:userid>")
def init_expense(userid):
    
        user_f = User.query.filter_by(id = userid).first()
        if not user_f:
            return "User dosen't exist"
        expense = Expense(
            amount=random.uniform(10.0, 500.0),
            user_id=userid
        )
        db.session.add(expense)
        db.session.commit()
        return f"expense created for {user_f.username} "
    

@user_route.route("/delete_user/<int:i>")
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

@user_route.route("/delete_expense/<int:expense_id>")
def delete_expense(expense_id):
    expense = Expense.query.filter_by(id = expense_id).first()
    if not expense:
        return "Expense dosen't exist"
    db.session.delete(expense)
    db.session.commit()
    return "Expense deleted"


@user_route.route("/view")
def view_users():
    users = User.query.all()
    users_data = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email
        }
        for u in users
    ]
    return jsonify(users_data)
