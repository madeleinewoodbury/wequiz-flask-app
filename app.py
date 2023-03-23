from flask import Flask
from flask_login import LoginManager
from models.User import UserModel
from user import User
from views import views
from admin import admin
from auth import auth
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    with UserModel() as db:
        user = User(*db.get_user_by_id(id))
    return user

if __name__ == '__main__':
    app.run(port=5200, debug=True)