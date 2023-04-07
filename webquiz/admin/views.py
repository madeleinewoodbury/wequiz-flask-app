from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from webquiz.admin.forms import QuizForm, QuestionForm
from webquiz.models.QuizDB import QuizDB

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
@login_required
def home():
    if current_user.is_admin():
        with QuizDB() as db:
            quizzes = db.get_quizzes()

        return render_template('admin.html', 
                               user=current_user, 
                               quizzes=quizzes)
    else:
        return redirect(url_for('main.home'))
    

@admin.route('/add-quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if current_user.is_admin():
        form = QuizForm()
        if form.validate_on_submit():
            title = form.title.data

            with QuizDB() as db:
                id = db.create_quiz(title)
                quiz = db.get_quiz(id)
            
            if quiz:
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

@admin.route('/view_quiz', methods=['GET'])
@login_required
def view_quiz():
    if current_user.is_admin():
        id = request.args['id']

        with QuizDB() as db:
            quiz = db.get_quiz(id)
            db.get_questions(quiz)
            for question in quiz.questions:
                db.get_user_answers(question)

        return render_template('quizView.html', quiz=quiz)

    else:
        return redirect(url_for('main.home'))
    

@admin.route('/quiz', methods=['GET'])
@login_required
def quiz():
    if current_user.is_admin():
        id = request.args['id']

        with QuizDB() as db:
            quiz = db.get_quiz(id)
            db.get_questions(quiz)

        return render_template('adminQuiz.html', quiz=quiz)
    else:
        return redirect(url_for('main.home'))


@admin.route('/add-question', methods=['GET', 'POST'])
@login_required
def create_question():
    if current_user.is_admin():
        form = QuestionForm()
        quiz_id = request.args['quiz_id']

        with QuizDB() as db:
            result = db.get_categories()
            form.category.choices = [(name[0], name[0]) for name in result]

        if form.validate_on_submit():
            multiple_choice = int(form.is_multiple_choice.data)
            with QuizDB() as db:
                id = db.create_question(category=form.category.data, 
                                        content=form.content.data, 
                                        multiple_choice=multiple_choice)
                db.create_quiz_question(quiz_id=quiz_id, question_id=id)
                db.create_choice(question_id=id, content=form.answer.data, is_correct=True)

                if multiple_choice:
                    for choice in form.choices:
                        if choice.content.data:
                            db.create_choice(question_id=id, 
                                             content=choice.content.data,
                                             is_correct=False)

            flash('Spørsmål lagt til', 'success')
            return redirect(url_for('admin.quiz', id=quiz_id))

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
        with QuizDB() as db:
            question = db.get_question(id)
            answer = db.get_answer(id)
            alternatives = db.get_alternatives(id)
            categories = db.get_categories()

        choices = []
        for choice in alternatives:
            choices.append({'content': choice.content, 'choice_id': choice.id})

        form = QuestionForm(choices=choices)
        form.category.choices = [(name[0], name[0]) for name in categories]

        if form.validate_on_submit():
            multiple_choice = int(form.is_multiple_choice.data)

            with QuizDB() as db:
                db.update_question(id=id,
                                   category=form.category.data,
                                   content=form.content.data,
                                   is_multiple_choice=multiple_choice)
                answer = db.get_answer(question_id=id)
                db.update_choice(id=answer.id, content=form.answer.data)
                
                if multiple_choice:
                    for choice in form.choices:
                        choice_id, content = choice.choice_id.data, choice.content.data
                        if choice_id and content:
                            db.update_choice(choice_id, content)
                        elif content:
                            db.create_choice(id, content, False)
                        elif choice_id:
                            db.delete_choice(choice_id)
                else:
                    # delete choices if any
                    alternatives = db.get_alternatives(question_id=id)
                    for choice in alternatives:
                        db.delete_choice(choice.id)
            
            flash('Spørsmål oppdatert', 'success')
            return redirect(url_for('admin.quiz', id=quiz_id))

        form.id.data = question.id
        form.category.data = question.category
        form.content.data = question.content
        form.is_multiple_choice.data = question.is_multiple_choice
        form.answer.data = answer.content
        
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

        with QuizDB() as db:
            db.delete_question(id)
            flash('Spørsmål slettet', 'success')

        return redirect(url_for('admin.quiz', id=quiz_id))

    else:
        return redirect(url_for('main.home'))
    



    

