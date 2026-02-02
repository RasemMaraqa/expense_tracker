from models import User, Expense
from extensions.db import DB as db

def get_user_with_expenses(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return None, None

    expenses = Expense.query.filter_by(user_id=user.id).all()
    return user, expenses
