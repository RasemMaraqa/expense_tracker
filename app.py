from flask import Flask, jsonify , request , render_template , redirect , url_for   , session ,Blueprint
from flask_sqlalchemy import SQLAlchemy
import jwt
from extensions.db import DB as db
from routes import  user_route , login_route , signup_route
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'af08f872d18b4fd0bfbee70c5132b54f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app) 
with app.app_context():
    db.create_all()

app.register_blueprint(signup_route)
app.register_blueprint(login_route)
app.register_blueprint(user_route)







app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


if __name__ == '__main__':
    app.run(debug=True)