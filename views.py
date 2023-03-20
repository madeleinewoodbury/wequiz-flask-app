import imp
from flask import Blueprint, render_template, request
from flask_login import login_user
from forms.LoginForm import LoginForm
from models.Role import RoleModel
from models.User import UserModel
from user import User

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    with RoleModel() as db:
        result = db.get_all()
        form.role.choices = result

    if request.method == 'POST':
        role = form.role.data
        email = form.email.data
        password = form.password.data

        with UserModel() as db:
            result = db.get_user_by_email(email)
            if result:
                user = User(*result)
                if user.check_password(password):
                    login_user(user, remember=True)
                    print('success')
                else:
                    print('wrong credentials')


    return render_template('login.html', form=form)