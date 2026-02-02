from flask import Blueprint,  session , render_template, flash , redirect , url_for 
from models import User
from models import Expense
from decorators.decorators import login_required , admin_required
from extensions.db import DB as db
from services import get_user_with_expenses


frontend_route = Blueprint('frontend', __name__)



@frontend_route.route("/user/<int:id>" , methods=["GET", "POST"])
@admin_required
def userpage(id):
    
        user , expenses = get_user_with_expenses(id)
        if not user:
            flash("User not found" , "error")
            return redirect(url_for("login.login")) 
        
        

        return render_template(
        "user.html",
        user=user,
        expenses=expenses
    )

@frontend_route.route("/user")
@login_required
def user_page():
        user_id = session.get("user_id")
        user , expenses = get_user_with_expenses(user_id)

        return render_template(
        "user.html",
        user=user,
        expenses=expenses
    )


@frontend_route.route("/")
@login_required
def redirect_to_page():
             
    return redirect(url_for("frontend.user_page"))
    

