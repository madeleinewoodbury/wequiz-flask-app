from random import choices
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from forms.QuizForm import QuizForm
from forms.QuestionForm import QuestionForm
from forms.ChoiceForm import ChoiceForm
from models.Quiz import QuizModel
from models.Question import QuestionModel, Question, Choice
from models.Category import CategoryModel
from uuid import uuid4

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def home():
    if current_user.is_admin():
        return render_template('admin.html', user=current_user)
    else:
        return redirect(url_for('views.home'))
    

@admin.route('/quiz', methods=['GET', 'POST'])
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
                    return redirect(url_for('admin.question', title=title, id=id))
                else:
                    flash('Noe gikk galt', category='danger')
        if form.errors:
            for message in form.errors.values():
                flash(message, category='error')
        return render_template('quizForm.html', form=form)
    else:
        return redirect(url_for('views.home'))
    

@admin.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    title = request.args['title']
    id = request.args['id']
    if current_user.is_admin():
        form = QuestionForm()
        with CategoryModel() as db:
            result = db.get_categories()
            form.category.choices = result
        if form.validate_on_submit():
            category = form.category.data
            question_content = form.content.data
            answer_content = form.answer.data
            is_multiple_choice = int(form.is_multiple_choice.data)
            _question = Question(category, question_content, is_multiple_choice, id)
            _question.add_choice(answer_content, is_correct=True)

            with QuestionModel() as db:
                if db.create(_question):
                    flash('Spørsmål lagt til', 'success')
                    if form.choices.data > 0:
                        return redirect(url_for('admin.choice', question_id=_question.id))
                else:
                    flash('Noe gikk galt', category='danger')

            return redirect(url_for('views.home'))

        else:
            return render_template('questionForm.html', form=form, title=title, id=id)
    else:
        return redirect(url_for('views.home'))
    
@admin.route('/choice', methods=['GET', 'POST'])
@login_required
def choice():
    if current_user.is_admin():
        form = ChoiceForm()
        if request.args['question_id']:
            form.question_id = request.args['question_id']

        print(form.question_id)
        return render_template('choice.html', form=form)
    else:
        return redirect(url_for('views.home'))
