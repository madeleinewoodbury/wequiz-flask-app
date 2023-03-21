from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_user, login_required
from forms.LoginForm import LoginForm
from models.UserRole import UserRoleModel
from models.User import UserModel
from user import User

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    with UserRoleModel() as db:
        result = db.get_choices()
        form.role.choices = result

    if form.validate_on_submit():
        print('hey')
        role = form.role.data
        email = form.email.data
        password = form.password.data

        with UserModel() as db:
            result = db.get_user_by_email(email)
        if result:
            user = User(*result)
            if user.check_password(password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                if role.lower() == 'administrator':
                    if user.is_admin():
                        return redirect(url_for('views.admin'))
                    else:
                        flash('Not Authorized', category='error')
                else:
                    return redirect(url_for('views.home'))
                
            flash('Invalid credentials', category='error')

    if form.errors:
        print(form.errors)
        for message in form.errors.values():
            flash(message, category='error')
        

    return render_template('login.html', form=form)


@views.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@views.route('/home')
def home():
    return render_template('home.html')