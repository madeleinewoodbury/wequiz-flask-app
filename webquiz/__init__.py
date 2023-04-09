from flask import Flask, render_template
from flask_login import LoginManager, current_user
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
    
    # 404 not found
    def page_not_found(e):
        return render_template("notFound.html", user=current_user)

    app.register_error_handler(404, page_not_found)
    
    return app

