from flask import Flask
from flask_login import LoginManager
from webquiz.models.AuthDB import AuthDB
from webquiz.main.views import main
from webquiz.auth.views import auth
from webquiz.admin.views import admin
from config import SECRET_KEY

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin, url_prefix='/admin')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        with AuthDB() as db:
            user = db.get_user_by_id(id)
        return user
    
    return app

