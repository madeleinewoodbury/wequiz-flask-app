from hashlib import new
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from forms.LoginForm import LoginForm
from forms.QuizForm import QuizForm
from forms.QuestionForm import QuestionForm
from forms.RegisterForm import RegisterForm
from models.UserRole import UserRoleModel
from models.User import UserModel
from models.Quiz import QuizModel
from user import User
from uuid import uuid4

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
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
                        return redirect(url_for('views.admin'))
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


@views.route('/register', methods=['GET', 'POST'])
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
                        return redirect(url_for('views.home'))
                    else:
                        flash('En feil oppstod', category='error')

    if form.errors:
        for message in form.errors.values():
            flash(message, category='error')

    return render_template('register.html', form=form)

@views.route('/admin')
@login_required
def admin():
    if current_user.is_admin():
        return render_template('admin.html', user=current_user)
    else:
        return redirect(url_for('views.home'))

@views.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))

@views.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if current_user.is_admin():
        form = QuizForm()
        if form.validate_on_submit():
            title = form.title.data
            with QuizModel() as db:
                id = str(uuid4())    # generate unique id
                if db.create(id, title):
                    flash(f"Quizzen {title} opprettet", category='success')
                    return redirect(url_for('views.question', quiz_id=id, title=title))
                else:
                    flash('Noe gikk galt', category='danger')
        if form.errors:
            for message in form.errors.values():
                flash(message, category='error')
        return render_template('quizForm.html', form=form)
    else:
        return redirect(url_for('views.home'))
    
@views.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    title = request.args['title']
    if current_user.is_admin():
        print(current_user)
        form = QuestionForm()
        if form.validate_on_submit():
            return redirect(url_for('views.admin'))
        else:
            # print('id: ', form.quiz_id.data)
            return render_template('questionForm.html', form=form, title=title)
        #     title = form.title.data
        #     with QuizModel() as db:
        #         id = str(uuid4())    # generate unique id
        #         if db.create(id, title):
        #             flash(f"Quizzen {title} opprettet", category='success')
        #         else:
        #             flash('Noe gikk galt', category='danger')
        # if form.errors:
        #     for message in form.errors.values():
        #         flash(message, category='error')
        # return render_template('quizForm.html', form=form)
    else:
        return redirect(url_for('views.home'))