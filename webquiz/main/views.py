from hashlib import new
from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import login_required, current_user
from webquiz.models.UserQuiz import UserQuizTable, UserQuiz, Answer
from webquiz.models.Quiz import QuizTable, Quiz
from webquiz.models.Question import QuestionTable, Question
from webquiz.main.forms import ChoiceAnswerForm, TextAnswerForm
from uuid import uuid4

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/home')
@login_required
def home():
    if current_user.is_admin():
        return redirect(url_for('admin.home'))
    
    with QuizTable() as db:
        result = db.get_all()
        quizzes = []
        for quiz in result:
            quizzes.append(Quiz(*quiz))

    return render_template('home.html', user=current_user, quizzes=quizzes)

@main.route('/quiz')
@login_required
def quiz():
    quiz_id = request.args['id']

    # create new user quiz
    with UserQuizTable() as db:
        prev = db.get_by_user_and_quiz(quiz_id, current_user.id)
        
        # can only take a quiz max 3 times
        if len(prev) < 10:
            id = str(uuid4())
            new_quiz = UserQuiz(id, quiz_id, current_user.id)
            db.create(new_quiz)

            return redirect(url_for('main.quiz_question', 
                                    id=new_quiz.id, 
                                    quiz=quiz_id,
                                    current=0))

        else:
            return redirect(url_for('main.home'))


@main.route('/quiz-question', methods=['GET', 'POST'])
@login_required
def quiz_question():
    current = int(request.args['current'])
    id = request.args['id'] 
    quiz_id = request.args['quiz'] 

    with UserQuizTable() as db:
        quiz = db.get_by_id(id)
    
    if request.method == 'POST':
        multiple_choice = int(request.args['multiple_choice'])
        form = ChoiceAnswerForm() if multiple_choice else TextAnswerForm()
        question = quiz.questions[current-1]

        if multiple_choice:
            form.answer.choices = [(c.content, c.content) for c in question.choices]

        if form.validate():
            content = form.answer.data
            question_id = form.question_id.data
            answer = Answer(user_quiz=id, question=question_id, content=content)

            # save answer to database and get next question
            with UserQuizTable() as db:
                db.create_answer(answer)


    # get the next question
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
                                id=id,
                                quiz=quiz_id,
                                form=form, 
                                question=question.content,
                                multiple_choice = question.is_multiple_choice,
                                current=current)
    else:
        # review quiz before saving
        with UserQuizTable() as db:
            db.get_user_answers(quiz)
        # with QuestionTable() as db:
        #     for answer in quiz.answers:
        #         question = db.get_question(id=answer.question)
        #         answer.question.content = question.content
        
        return render_template('quiz.html', quiz=quiz)

    return render_template('home.html')