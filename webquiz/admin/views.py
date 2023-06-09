from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from webquiz.admin.forms import QuizForm, QuestionForm, SearchForm, CategoryForm, QuizSelectForm
from webquiz.main.views import quizzes
from webquiz.models.QuizDB import QuizDB

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
@login_required
def home():
    if current_user.is_admin():
        with QuizDB() as db:
            quizzes = db.get_quizzes()
            for quiz in quizzes:
                quiz.questions = db.get_questions(quiz.id)
                
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
        return render_template('forms/addQuiz.html', form=form)
    else:
        return redirect(url_for('main.home'))

@admin.route('/edit-quiz', methods=['GET', 'POST'])
@login_required
def update_quiz():
    if current_user.is_admin():
        id = request.args['id']
        form = QuizForm()

        if form.validate_on_submit():
            with QuizDB() as db:
                db.update_quiz(id, form.title.data)
            
            flash(f"Quizzen oppdatert", category='success')
            return redirect(url_for('admin.quiz', id=id))
        
        if form.errors:
            for message in form.errors.values():
                flash(message, category='error')

        with QuizDB() as db:
            quiz = db.get_quiz(id)
        
        form.title.data = quiz.title
        form.submit.label.text = "Lagre"
        return render_template('forms/editQuiz.html', form=form, id=id)

    else:
        return redirect(url_for('main.home'))

@admin.route('/delete/quiz', methods=['GET'])
@login_required
def delete_quiz():
    if current_user.is_admin():
        id = request.args['id']

        with QuizDB() as db:
            db.delete_quiz(id)
            flash('Quiz slettet', 'success')

        return redirect(url_for('admin.home'))

    else:
        return redirect(url_for('main.home'))
    
@admin.route('/quiz/results', methods=['GET'])
@login_required
def quiz_results():
    if current_user.is_admin():
        id = request.args['id']

        with QuizDB() as db:
            quiz = db.get_quiz(id)
            quizzes = db.get_user_quizzes_by_quiz(id)

            for q in quizzes:
                q.answers = db.get_answers_with_result(q.id)
                q.calculate_score()

        return render_template('quizResults.html', 
                               quizzes=quizzes, 
                               title=quiz.title, 
                               user=current_user)

    else:
        return redirect(url_for('main.home'))
    
@admin.route('/quiz/user_answers', methods=['GET'])
@login_required
def quiz_user_answers():
    if current_user.is_admin():
        id = request.args['id']

        with QuizDB() as db:
            user_quiz = db.get_user_quiz(id)
            user_quiz.questions = db.get_questions(user_quiz.quiz)
            user_quiz.answers = db.get_answers_with_result(id)
            user_quiz.calculate_score()    

        return render_template('userAnswer.html', 
                               quiz=user_quiz, 
                               answers=len(user_quiz.answers),
                               user=current_user)

    else:
        return redirect(url_for('main.home'))
    
@admin.route('/quiz', methods=['GET'])
@login_required
def quiz():
    if current_user.is_admin():
        id = request.args['id']

        with QuizDB() as db:
            quiz = db.get_quiz(id)
            quiz.questions = db.get_questions(id)

        return render_template('adminQuiz.html', quiz=quiz, user=current_user)
    else:
        return redirect(url_for('main.home'))

@admin.route('/activate', methods=['GET'])
@login_required
def activate():
    if current_user.is_admin():
        id = request.args['id']
        status = request.args['status']
        status_text = 'aktiv' if int(status) else 'ikke aktiv'

        with QuizDB() as db:
            db.update_status(id, status)
        
        flash(f'Status satt til {status_text}', 'success')
        return redirect(url_for('admin.quiz', id=id))
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
                if quiz_id:
                    db.create_quiz_question(quiz_id=quiz_id, question_id=id)
                
                db.create_choice(question_id=id, content=form.answer.data, is_correct=True)

                if multiple_choice:
                    for choice in form.choices:
                        if choice.content.data:
                            db.create_choice(question_id=id, 
                                             content=choice.content.data,
                                             is_correct=False)

            flash('Spørsmål lagt til', 'success')
            if quiz_id:
                return redirect(url_for('admin.quiz', id=quiz_id, user=current_user))
            else:
                return redirect(url_for('admin.question', user=current_user))
        return render_template('forms/addQuestion.html', form=form, quiz_id=quiz_id)
    
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
            if quiz_id:
                return redirect(url_for('admin.quiz', id=quiz_id))
            else:
                return redirect(url_for('admin.question_detail', id=id))

        form.id.data = question.id
        form.category.data = question.category
        form.content.data = question.content
        form.is_multiple_choice.data = question.is_multiple_choice
        form.answer.data = answer.content
        
        if quiz_id:
            return render_template('forms/editQuestion.html', form=form, quiz=quiz_id)
        else:
            return render_template('forms/editQuestion.html', form=form)

    else:
        return redirect(url_for('main.home'))

@admin.route('/view_question')
@login_required
def question_detail():
    if current_user.is_admin():
        id = request.args['id']

        with QuizDB() as db:
            question = db.get_question(id)
            question.answer = db.get_answer(id)
            question.choices = db.get_alternatives(id)
            question.quizzes = db.get_quizzes_by_question(id)

        return render_template('questionView.html', question=question, user=current_user)
    else:
        return redirect(url_for('main.home'))
    
@admin.route('/questions', methods=['GET', 'POST'])
@login_required
def question():
    if current_user.is_admin():
        form = SearchForm()

        if request.method == 'POST':
            search_text = form.search.data
            category = form.category.data

            with QuizDB() as db:
                result = db.get_categories()
                questions = db.search_questions(category, search_text) 
                for q in questions:
                    q.answer = db.get_answer(q.id)           

        else:
            with QuizDB() as db:
                result = db.get_categories()
                questions = db.get_all_questions()
                for q in questions:
                    q.answer = db.get_answer(q.id)

        with QuizDB() as db:
            result = db.get_categories()
            form.category.choices = [(name[0], name[0]) for name in result]
            form.category.choices.insert(0, ('', 'Alle kategorier'))
        
        return render_template('adminQuestion.html', 
                               user=current_user, 
                               questions=questions,
                               form=form)
    else:
        return redirect(url_for('main.home'))

@admin.route('/add/quiz-question', methods=['GET', 'POST'])
@login_required
def add_quiz_question():
    if current_user.is_admin():
        id = request.args['id']
        form = QuizSelectForm()

        if request.method == 'POST':
            quiz = form.quiz.data
            with QuizDB() as db:
                db.create_quiz_question(quiz, id)
                flash('Spørsmål lagt til quiz', 'success')

            return redirect(url_for('admin.question_detail', id=id))
        
        with QuizDB() as db:
            quizzes = db.get_available_quizzes(id)
            if quizzes:
                choices = []
                for quiz in quizzes:
                    choices.append((quiz.id, quiz.title))

                form.quiz.choices = choices
                form.id.data = id
        
                return render_template('forms/addToQuiz.html', form=form)
            else:
                flash('Ingen tilgjengelige quizzer', 'error')
                return redirect(url_for('admin.question_detail', id=id))

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

        if quiz_id:
            return redirect(url_for('admin.quiz', id=quiz_id))
        else:
            return redirect(url_for('admin.question', id=id))

    else:
        return redirect(url_for('main.home'))

@admin.route('/delete/quizquestion', methods=['GET'])
@login_required
def delete_quiz_question():
    if current_user.is_admin():
        id = request.args['id']
        quiz_id = request.args['quiz']

        with QuizDB() as db:
            if db.delete_quiz_question(quiz_id, id):
                flash('Spørsmål slettet fra quiz', 'success')
            else: 
                flash('Det oppstod en feil', 'error')

        return redirect(url_for('admin.quiz', id=quiz_id))

    else:
        return redirect(url_for('main.home'))

@admin.route('/add-category', methods=['GET', 'POST'])
@login_required
def create_category():
    if current_user.is_admin():
        form = CategoryForm()

        if form.validate_on_submit():
            name = form.name.data

            with QuizDB() as db:
                result = db.get_categories()
                categories = [c[0].lower() for c in result]
                if name.lower() in categories:
                    flash(f'Kategorien {name} er allerede i databasen', 'error')
                    return render_template('forms/addCategory.html', form=form)
                else:
                    if db.create_category(name):
                        flash(f"Kategorien {name} opprettet", category='success')
                    else:
                        flash('En feil oppstod', 'error')

                    return redirect(url_for('admin.question'))

        if form.errors:
            for message in form.errors.values():
                flash(message, category='error')
        return render_template('forms/addCategory.html', form=form)
    else:
        return redirect(url_for('main.home'))