from flask import Flask, json, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO, emit, join_room, send

db = SQLAlchemy()
DB_NAME = "database.db"
app = Flask(__name__)
app.config['SECRET_KEY'] = '1f601a5ffe473ae4da49cd43ec646d3f'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def load_file(file_name="depts.json"):
    with open(file_name) as json_file:
        data = json.load(json_file)
        return data

def page_not_found(e):
  return render_template('404.html'), 404

def create_app():
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)
    app.register_error_handler(404, page_not_found)
    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    db.create_all(app=app)

socketio = SocketIO(app)
app = create_app()

if __name__ == "__main__":
    app.run(debug=False)