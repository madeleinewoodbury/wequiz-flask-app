from crypt import methods
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from webquiz.admin.forms import QuizForm, QuestionForm, ChoiceForm
from webquiz.models.Quiz import Quiz, QuizTable
from webquiz.models.Question import Question, QuestionTable
from webquiz.models.Category import CategoryTable
from webquiz.models.Choice import Choice
from uuid import uuid4

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
@login_required
def home():
    if current_user.is_admin():
        with QuizTable() as db:
            result = db.get_all()
            quizzes = []
            for quiz in result:
                quizzes.append(Quiz(*quiz))

        return render_template('admin.html', user=current_user, quizzes=quizzes)
    else:
        return redirect(url_for('main.home'))
    

@admin.route('/add-quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if current_user.is_admin():
        form = QuizForm()
        if form.validate_on_submit():
            title = form.title.data
            with QuizTable() as db:
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
        return redirect(url_for('main.home'))


@admin.route('/quiz', methods=['GET'])
@login_required
def quiz():
    if current_user.is_admin():
        id = request.args['id']

        with QuizTable() as db:
            quiz = db.get_by_id(id)
            if quiz:
                db.get_questions(quiz)
            else:
                return redirect(url_for('main.home'))

        with QuestionTable() as db:
            questions = []
            for question_id in quiz.questions:
                question = db.get_by_id(question_id)
                question = Question(*question)
                if len(question.content) > 45:
                    question.content = question.content[:45] + '...' 
                questions.append(question)
                
        return render_template('quiz.html', quiz=quiz, questions=questions)
    else:
        return redirect(url_for('main.home'))


@admin.route('/add-question', methods=['GET', 'POST'])
@login_required
def create_question():
    if current_user.is_admin():
        form = QuestionForm()
        quiz_id = request.args['quiz_id']
        
        with CategoryTable() as db:
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

            with QuestionTable() as db:
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
        return redirect(url_for('main.home'))
    

@admin.route('/question', methods=['GET'])
@login_required
def question():
    if current_user.is_admin():
        id = request.args['id']

        with QuestionTable() as db:
            result = db.get_by_id(id)
            question = Question(*result)
            question.answer = db.get_answer(id)
            choices = db.get_choices(id)

            for choice in choices:
                id, content = choice
                question.add_choice(id, content, False)

            return render_template('questionAdmin.html', question=question)

    else:
        return redirect(url_for('main.home'))
    

@admin.route('/delete/question', methods=['GET'])
@login_required
def delete_question():
    if current_user.is_admin():
        id = request.args['id']
        quiz_id = request.args['quiz']

        print('Attempting to delete: ', id)

        with QuestionTable() as db:
            if db.delete(id):
                flash('Spørsmål slettet', 'success')
        
        flash('Det oppstod en feil', 'danger')
        return redirect(url_for('admin.quiz', id=quiz_id))


    else:
        return redirect(url_for('main.home'))
    

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

            with QuestionTable() as db:
                if db.create_choice(new_choice):
                    flash('Svaralternativ opprettet', 'success')
                    return redirect(url_for('admin.question', id=question_id))

        return render_template('choice.html', form=form, id=question_id)
    else:
        return redirect(url_for('main.home'))



    

