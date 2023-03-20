from flask import Flask
from flask_login import LoginManager
from models.User import UserModel
from user import User
from views import views
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

app.register_blueprint(views, url_prefix='/')

login_manager = LoginManager()
login_manager.login_view = 'views.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    with UserModel() as db:
        user = User(*db.get_user_by_id(id))
    return user

if __name__ == '__main__':
    app.run(port=5200, debug=True)