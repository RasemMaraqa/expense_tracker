
from extensions.db import DB as db
from models import User
from flask import  redirect , url_for , session , abort
from functools import wraps





def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated





def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):

        u = db.session.get(User, session["user_id"])
        if not u or not u.is_admin:
            return abort(401)  
        return f(*args, **kwargs)
    return decorated
