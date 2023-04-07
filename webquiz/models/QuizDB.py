import mysql.connector
from config import Database
from webquiz.models.Quiz import QuizTable, Quiz
from webquiz.models.Question import QuestionTable, Question, Choice

class Answer:
    def __init__(self, user_quiz, question, content):
        self.user_quiz = user_quiz
        self.question = question
        self.content = content
        self.question_content = None
        self.is_correct = False

class UserQuiz:
    def __init__(self, id, quiz, user, date_taken=None):
        self.id = id
        self.quiz = quiz
        self.user = user
        self.date_taken = date_taken
        self.answers = []
        self.questions = []
        self.results = []
        self.current = 0
    
    def add_answer(self, answer):
        self.answers.append(answer)

    def add_question(self, question):
        self.questions.append(question)

    def add_results(self, results):
        pass
    

class UserQuizTable(Database):
    def __init__(self):
        super().__init__()
    
    def create(self, user_quiz):
        try:
            query = """INSERT INTO UserQuiz (id, quiz, user)
                        VALUES (%s, %s, %s)"""
            values = (user_quiz.id, user_quiz.quiz, user_quiz.user)
            self.cursor.execute(query, values)
            return True
        except mysql.connector.Error as err:
            print(err)
            return False
        
    def create_answer(self, answer):
        try:
            query = """INSERT INTO Answer (user_quiz, question, content)
                        VALUES (%s, %s, %s)"""
            values = (answer.user_quiz, answer.question, answer.content)
            self.cursor.execute(query, values)
            return True
        except mysql.connector.Error as err:
            print(err)
            return False
        
    def get_by_id(self, id):
        try:
            query = """SELECT * FROM UserQuiz WHERE id=(%s)"""
            self.cursor.execute(query, (id,))
            result = self.cursor.fetchone()
            user_quiz = UserQuiz(*result)
            self.get_quiz_questions(user_quiz)
            return user_quiz
        except mysql.connector.Error as err:
            print(err)
    
    def get_all(self):
        try:
            query = """SELECT * FROM UserQuiz"""
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(err)

    def get_by_user(self, user_id):
        try:
            query = """SELECT * FROM UserQuiz WHERE user=(%s)"""
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(err)

    def get_by_user_and_quiz(self, quiz_id, user_id):
        try:
            query = """SELECT * FROM UserQuiz WHERE quiz=(%s) AND user=(%s)"""
            self.cursor.execute(query, (quiz_id, user_id))
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(err)

    def get_user_answer(self, quiz_id, question_id):
        try:
            query = """SELECT content FROM Answer WHERE user_quiz=(%s) AND question=(%s)"""
            self.cursor.execute(query, (quiz_id, question_id))
            result = self.cursor.fetchone()
            answer = Answer(quiz_id, question_id, content=result[0])
            return answer
        except mysql.connector.Error as err:
            print(err)

    def get_user_answers_by_question(self, question_id):
        try:
            query = """SELECT content, date_taken FROM Answer
                       INNER JOIN UserQuiz ON UserQuiz.id = Answer.user_quiz 
                       WHERE question=(%s)"""
            self.cursor.execute(query, (question_id,))
            result = self.cursor.fetchall()
            print(result)
        except mysql.connector.Error as err:
            print(err)

    def update_answer(self, quiz_id, question_id, new_content):
        try:
            query = """UPDATE Answer SET content=(%s) WHERE user_quiz=(%s) AND question=(%s)"""
            self.cursor.execute(query, (new_content, quiz_id, question_id))
            return True
        except mysql.connector.Error as err:
            print(err)

    def get_answers(self, user_quiz):
        try:
            query = """SELECT * FROM Answer WHERE user_quiz=(%s)"""
            self.cursor.execute(query, (user_quiz.id,))
            result = self.cursor.fetchall()
            for answer in result:
                user_quiz.add_answer(Answer(*answer))

            return True
        except mysql.connector.Error as err:
            print(err)
    
    def get_quiz_questions(self, user_quiz):
        with QuizTable() as db:
            quiz = db.get_by_id(user_quiz.quiz)
            db.get_questions(quiz)
        
        for id in quiz.questions:
            with QuestionTable() as db:
                question = db.get_question(id)
                question.choices = db.get_choices(question.id)
                user_quiz.add_question(question)

    def get_user_answers(self, user_quiz):
        self.get_answers(user_quiz)
        if user_quiz.answers:
            for answer in user_quiz.answers:
                # get question
                with QuestionTable() as db:
                    question = db.get_question(answer.question)
                    answer.question_content = question.content

    def check_answers(self, quiz):
        try:
            query = """SELECT Q.id, Q.content, A.content,
                       (SELECT C.content FROM Choice AS C WHERE C.question = A.question AND C.is_correct=1)
                        FROM Answer AS A INNER JOIN Question AS Q ON Q.id = A.question
                        WHERE A.user_quiz=(%s)"""
            
            self.cursor.execute(query, (quiz.id,))
            result = self.cursor.fetchall()
            for item in result:
                question_id, question, user_answer, correct_answer = item
                answer = Answer(quiz.id, question_id, user_answer)
                answer.question_content = question
                if user_answer == correct_answer:
                    answer.is_correct = True

                quiz.add_answer(answer)    

        except mysql.connector.Error as err:
            print(err)