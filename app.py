from flask import Flask, jsonify , request , render_template , redirect , url_for   , session ,Blueprint
from flask_sqlalchemy import SQLAlchemy
import jwt
from routes import  user_route
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

app.register_blueprint(user_route)





app.config['SECRET_KEY'] = 'af08f872d18b4fd0bfbee70c5132b54f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


if __name__ == '__main__':
    app.run(debug=True)