from unittest import result
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
    

@admin.route('/add-quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if current_user.is_admin():
        form = QuizForm()
        if form.validate_on_submit():
            title = form.title.data
            with QuizModel() as db:
                id = str(uuid4())    # generate unique id
                if db.create(id, title):
                    flash(f"Quizzen {title} opprettet", category='success')
                    return redirect(url_for('admin.quiz', id=id))
                else:
                    flash('Noe gikk galt', category='danger')
        if form.errors:
            for message in form.errors.values():
                flash(message, category='error')
        return render_template('quizForm.html', form=form)
    else:
        return redirect(url_for('views.home'))
    

@admin.route('/add-question', methods=['GET', 'POST'])
@login_required
def create_question():
    if current_user.is_admin():
        form = QuestionForm()
        quiz_id = request.args['quiz_id']
        
        with CategoryModel() as db:
            result = db.get_categories()
            form.category.choices = result

        if form.validate_on_submit():
            id = str(uuid4())
            category = form.category.data
            content = form.content.data
            answer = form.answer.data
            is_multiple_choice = int(form.is_multiple_choice.data)
            question = Question(id, category, content, is_multiple_choice)
            question.quiz = quiz_id
            choice_id = str(uuid4())
            question.add_choice(choice_id, answer, is_correct=True)

            with QuestionModel() as db:
                if db.create(question):
                    flash('Spørsmål lagt til', 'success')
                    if is_multiple_choice:
                        return redirect(url_for('admin.choice', id=question.id))
                else:
                    flash('Noe gikk galt', category='danger')

            return redirect(url_for('admin.quiz', id=quiz_id))

        else:
            return render_template('questionForm.html', form=form, quiz_id=quiz_id)
    else:
        return redirect(url_for('views.home'))
    
@admin.route('/choice', methods=['GET', 'POST'])
@login_required
def choice():
    if current_user.is_admin():
        form = ChoiceForm()
        question_id = request.args['id']

        if form.validate_on_submit():
            id = str(uuid4())
            content = form.content.data
            new_choice = Choice(id, question_id, content, False)

            with QuestionModel() as db:
                if db.create_choice(new_choice):
                    flash('Svaralternativ opprettet', 'success')
                    return redirect(url_for('question', id=question_id))

        return render_template('choice.html', form=form, id=question_id)
    else:
        return redirect(url_for('views.home'))


@admin.route('/quiz', methods=['GET'])
@login_required
def quiz():
    if current_user.is_admin():
        id = request.args['id']

        with QuizModel() as db:
            quiz = db.get_by_id(id)
            if quiz:
                db.get_questions(quiz)
            else:
                return redirect(url_for('views.home'))

        with QuestionModel() as db:
            questions = []
            for question_id in quiz.questions:
                question = db.get_by_id(question_id)
                question = Question(*question)
                if len(question.content) > 45:
                    question.content = question.content[:45] + '...' 
                questions.append(question)
                
        return render_template('quiz.html', quiz=quiz, questions=questions)
    else:
        return redirect(url_for('views.home'))
    

@admin.route('/question', methods=['GET'])
@login_required
def question():
    if current_user.is_admin():
        id = request.args['id']

        with QuestionModel() as db:
            result = db.get_by_id(id)
            question = Question(*result)
            question.answer = db.get_answer(id)
            choices = db.get_choices(id)

            for choice in choices:
                id, content = choice
                question.add_choice(id, content, False)

            return render_template('questionAdmin.html', question=question)

    else:
        return redirect(url_for('views.home'))