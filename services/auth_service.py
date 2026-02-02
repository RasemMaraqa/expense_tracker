from models import User
from extensions.db import DB as db
from werkzeug.security import check_password_hash

def authenticate(email, password):
    user = db.session.query(User).filter_by(email=email).first()
    if not user:
        return None

    if not check_password_hash(user.password, password):
        return None

    return user
