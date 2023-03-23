from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import login_user, login_required, logout_user
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from models.User import UserModel
from models.UserRole import UserRoleModel
from user import User
from uuid import uuid4

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    with UserRoleModel() as db:
        result = db.get_choices()
        form.role.choices = result

    if form.validate_on_submit():
        role = form.role.data
        email = form.email.data
        password = form.password.data

        with UserModel() as db:
            result = db.get_user_by_email(email)
        if result:
            user = User(*result)
            if user.check_password(password):
                login_user(user, remember=True)
                if role.lower() == 'administrator':
                    if user.is_admin():
                        flash('Logged in successfully!', category='success')
                        return redirect(url_for('views.home'))
                    else:
                        flash('Not Authorized', category='error')
                else:
                    flash('Logged in successfully!', category='success')
                    return redirect(url_for('views.home'))
                
            flash('Invalid credentials', category='error')

    if form.errors:
        for message in form.errors.values():
            flash(message, category='error')
        

    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data
        password2 = form.password2.data

        if password != password2:
            flash('Passord må være like', category='error')
        else:
            with UserModel() as db:
                result = db.get_user_by_email(email)
                if result:
                    flash('Bruker allerede registrert med den epost adressen', category='error')
                else:
                    id = str(uuid4())    # generate unique id
                    new_user = User(id, firstname, lastname, email)
                    new_user.set_password(password)
                    if db.create(new_user):
                        flash('Ny bruker opprettet', category='success')
                        login_user(new_user, remember=True)
                        return redirect(url_for('views.home'))
                    else:
                        flash('En feil oppstod', category='error')

    if form.errors:
        for message in form.errors.values():
            flash(message, category='error')

    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))