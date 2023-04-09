from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import login_user, login_required, logout_user
from webquiz.auth.forms import LoginForm, RegisterForm
from webquiz.models.AuthDB import AuthDB

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    with AuthDB() as db:
        result = db.get_user_roles()
        form.role.choices = [(role[0], role[0]) for role in result]

    if form.validate_on_submit():
        role = form.role.data
        email = form.email.data
        password = form.password.data

        with AuthDB() as db:
            user = db.get_user_by_email(email)
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            if role.lower() == 'administrator':
                if user.is_admin():
                    flash('Logged in successfully!', category='success')
                    return redirect(url_for('admin.home'))
                else:
                    flash('Not Authorized', category='error')
            else:
                flash('Logged in successfully!', category='success')
                return redirect(url_for('main.home'))
            
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
            with AuthDB() as db:
                if db.user_exist(email):
                    flash('Bruker allerede registrert med den epost adressen', category='error')
                else:
                    new_user = db.create(firstname, lastname, email, password)
                    if new_user:
                        flash('Ny bruker opprettet', category='success')
                        login_user(new_user, remember=True)
                        return redirect(url_for('main.home'))
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