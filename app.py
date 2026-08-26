from flask import Flask
from extensions.db import DB as db
from routes import  user_route , login_route , signup_route , frontend_route

app = Flask(__name__)

app.config['SECRET_KEY'] = 'af08f872d18b4fd0bfbee70c5132b54f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


db.init_app(app) 
with app.app_context():
    db.create_all()

app.register_blueprint(signup_route)
app.register_blueprint(login_route)
app.register_blueprint(user_route)
app.register_blueprint(frontend_route)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


if __name__ == '__main__':
    app.run(debug=False)
