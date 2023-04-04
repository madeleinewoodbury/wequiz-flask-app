import mysql.connector
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from webquiz.admin.forms import QuizForm, QuestionForm
from webquiz.models.Quiz import Quiz, QuizTable
from webquiz.models.Question import Question, QuestionTable, Choice
from webquiz.models.Category import CategoryTable

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
                question = db.get_question(question_id)
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
            question = Question(id=str(uuid4()),
                                category=form.category.data,
                                content=form.content.data,
                                is_multiple_choice=int(form.is_multiple_choice.data))
            answer = Choice(id=str(uuid4()), 
                            question=question.id, 
                            content=form.answer.data, 
                            is_correct=True)
            question.answer = answer
            question.quiz = quiz_id

            if question.is_multiple_choice:
                for choice in form.choices:
                    if choice.content.data:
                        question.add_choice(id=str(uuid4()), 
                                            content=choice.content.data)

            try:
                with QuestionTable() as db:
                    db.create(question)

                flash('Spørsmål lagt til', 'success')
                return redirect(url_for('admin.quiz', id=quiz_id))
                
            except mysql.connector.Error as err:
                print(err)
                flash('Noe gikk galt', category='danger')

        return render_template('questionForm.html', form=form, quiz_id=quiz_id)
    
    else:
        return redirect(url_for('main.home'))
    

@admin.route('/edit-question', methods=['GET', 'POST'])
@login_required
def update_question():
    if current_user.is_admin():
        id = request.args['id']
        quiz_id = request.args['quiz']

        # get the form data
        with QuestionTable() as db:
            question = db.get_question(id)
            question.answer = db.get_answer(id)
            question.choices = db.get_alternatives(id)

        choices = []
        for choice in question.choices:
            choices.append({'content': choice.content, 'choice_id': choice.id})

        form = QuestionForm(choices=choices)

        with CategoryTable() as db:
            result = db.get_categories()
            form.category.choices = result

        if form.validate_on_submit():
            question = Question(id=id, 
                                category=form.category.data, 
                                content=form.content.data, 
                                is_multiple_choice=int(form.is_multiple_choice.data))

            # update question 
            with QuestionTable() as db:
                question.answer = db.get_answer(id)
                question.answer.content = form.answer.data

                db.update(question)
                db.update_choice(question.answer)

                if question.is_multiple_choice:
                    for choice in form.choices:
                        choice_id, content = choice.choice_id.data, choice.content.data
                        if choice_id and content:
                            db.update_choice(Choice(choice_id, question.id, content, False))
                        elif content:
                            db.create_choice(Choice(str(uuid4()), question.id, content, False))
                        elif choice_id:
                            db.delete_choice(choice_id)
                else:
                    # delete choices if any
                    db.delete_alternatives(question.id)

            flash('Spørsmål oppdatert', 'success')
            return redirect(url_for('admin.quiz'), id=quiz_id)

        form.id.data = question.id
        form.category.data = question.category
        form.content.data = question.content
        form.is_multiple_choice.data = question.is_multiple_choice
        form.answer.data = question.answer.content
        
        return render_template('editQuestion.html', 
                               form=form, 
                               quiz=quiz_id)

    else:
        return redirect(url_for('main.home'))

@admin.route('/delete/question', methods=['GET'])
@login_required
def delete_question():
    if current_user.is_admin():
        id = request.args['id']
        quiz_id = request.args['quiz']

        try:
            with QuestionTable() as db:
                db.delete(id)
            
            flash('Spørsmål slettet', 'success')
        except mysql.connector.Error as err:
            print(err)
            flash('Det oppstod en feil', 'danger')

        return redirect(url_for('admin.quiz', id=quiz_id))

    else:
        return redirect(url_for('main.home'))
    



    

