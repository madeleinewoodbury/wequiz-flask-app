from flask import Blueprint, redirect, render_template, url_for, request, flash
from flask_login import login_required, current_user
from webquiz.models.QuizDB import QuizDB
from webquiz.main.forms import ChoiceAnswerForm, TextAnswerForm

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/home')
@login_required
def home():
    if current_user.is_admin():
        return redirect(url_for('admin.home'))
    
    with QuizDB() as db:
        user_quizzes = db.get_user_quizzes(current_user.id)
        for quiz in user_quizzes:
            quiz.answers = db.get_answers_with_result(quiz.id)
            quiz.calculate_score()
        
    return render_template('home.html', user=current_user, quizzes=user_quizzes)

@main.route('/quizzes')
@login_required
def quizzes():
    if current_user.is_admin():
        return redirect(url_for('admin.home'))
    
    with QuizDB() as db:
        quizzes = db.get_quizzes()
        user_attempts = {}
        for quiz in quizzes:
            user_attempts[quiz.id] = db.get_quiz_attempts(quiz.id, current_user.id)
            quiz.questions = db.get_questions_v2(quiz.id)
        
    return render_template('quizzes.html', 
                           user=current_user, 
                           quizzes=quizzes,
                           attempts=user_attempts)

@main.route('/quiz')
@login_required
def quiz():
    quiz_id = request.args['id']

    with QuizDB() as db:
        quiz = db.get_quiz(quiz_id)
        if not quiz.is_active:
            flash('Denne quizzen er ikke lenger aktiv', 'error')        
            return redirect(url_for('main.home'))
        
        prev_attempts = db.get_quiz_attempts(quiz_id, current_user.id)
    
        # can only take a quiz max 3 times
        if prev_attempts < 3: 
            id = db.create_user_quiz(quiz_id=quiz_id, user_id=current_user.id)
            return redirect(url_for('main.quiz_question',
                                    user_quiz_id=id, 
                                    quiz_id=quiz_id,
                                    current=0))
        else:
            flash('Du har ingen flere forsøk for denne quizzen', 'error')
            return redirect(url_for('main.home'))


@main.route('/quiz-question', methods=['GET', 'POST'])
@login_required
def quiz_question():
    current = int(request.args['current'])
    user_quiz_id = request.args['user_quiz_id'] 
    quiz_id = request.args['quiz_id'] 

    with QuizDB() as db:
        quiz = db.get_quiz(quiz_id)
        quiz.questions = db.get_questions_v2(quiz_id)
        for q in quiz.questions:
            q.choices = db.get_choices(q.id)        

    if request.method == 'POST':
        multiple_choice = int(request.args['multiple_choice'])
        question = quiz.questions[current-1]
        if multiple_choice:
            form = ChoiceAnswerForm()
            form.answer.choices = [(c.content, c.content) for c in question.choices]
        else:
            form = TextAnswerForm()

        if form.validate():
            content = form.answer.data
            question_id = form.question_id.data

            # save answer to database and get next question
            with QuizDB() as db:
                db.create_answer(user_quiz_id, question_id, content)
    
    if quiz.questions and current < len(quiz.questions):
        question = quiz.questions[current]
        current += 1

        if question.is_multiple_choice:
            form = ChoiceAnswerForm()
            form.answer.choices = [(c.content, c.content) for c in question.choices]
        else:
            form = TextAnswerForm()
    
        form.answer.data = ""
        form.question_id.data = question.id
        return render_template('question.html', 
                                user_quiz_id=user_quiz_id,
                                quiz_id=quiz_id,
                                form=form, 
                                question=question.content,
                                multiple_choice = question.is_multiple_choice,
                                current=current)
    else:
        # review quiz before saving
        with QuizDB() as db:
            user_quiz = db.get_user_quiz(user_quiz_id)
            user_quiz.answers = db.get_user_answers_by_user_quiz(user_quiz_id)

            for answer in user_quiz.answers:
                question = db.get_question(id=answer.question)
                answer.question_content = question.content

        return render_template('quiz.html', quiz=user_quiz)


@main.route('/edit-answer', methods=['GET', 'POST'])
@login_required
def edit_answer():
    quiz_id = request.args['quiz_id']
    question_id = request.args['question_id']

    with QuizDB() as db:
        question = db.get_question(question_id)
        question.choices = db.get_choices(question_id)

    if question.is_multiple_choice:
        form = ChoiceAnswerForm() 
        form.answer.choices = [(c.content, c.content) for c in question.choices]
    else:
        form = TextAnswerForm()
        
    if form.validate_on_submit():
        with QuizDB() as db:
            db.update_answer(quiz_id, question_id, form.answer.data)
            user_quiz = db.get_user_quiz(quiz_id)
            user_quiz.answers = db.get_user_answers_by_user_quiz(quiz_id)

        return render_template('quiz.html', quiz=user_quiz)

    with QuizDB() as db:
        answer = db.get_user_answer(quiz_id, question_id)

    form.answer.data = answer.content
    form.question_id.data = question.id
    return render_template('editAnswer.html', 
                            quiz_id=quiz_id,
                            form=form, 
                            question=question)

@main.route('/user_quiz/results')
@login_required
def quiz_results():
    id = request.args['id']

    with QuizDB() as db:
        user_quiz = db.get_user_quiz(id)
        user_quiz.questions = db.get_questions_v2(user_quiz.quiz)
        user_quiz.answers = db.get_answers_with_result(id)
        user_quiz.calculate_score()
        attempts = db.get_quiz_attempts(user_quiz.quiz, current_user.id)

    return render_template('results.html', 
                           quiz=user_quiz, 
                           answers=len(user_quiz.answers),
                           attempts=attempts,
                           user=current_user)
