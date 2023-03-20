from flask import Blueprint, render_template, request
from forms.LoginForm import LoginForm

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        print(form.role.data)
        print(form.email.data)
        print(form.password.data)
    return render_template('login.html', form=form)