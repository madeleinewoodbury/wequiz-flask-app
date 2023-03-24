import mysql.connector
from config import DB_CONFIG
from uuid import uuid4

class Choice():
    def __init__(self, id, question, content, is_correct):
        self.id = id
        self.question = question
        self.content = content
        self.is_correct = int(is_correct)


class Question():
    def __init__(self, id, category, content, is_multiple_choice):
        self.id = id
        self.category = category
        self.content = content
        self.is_multiple_choice = is_multiple_choice
        self.choices = []
        self.quiz = None

    def add_choice(self, content, is_correct):
        id = str(uuid4())
        self.choices.append(Choice(id, self.id, content, is_correct))


class QuestionModel:
    def __init__(self):
        self.config = DB_CONFIG
    
    def __enter__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor(prepared=True)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
    
    def create(self, question):
        try:
            id = question.id
            quiz = question.quiz
            category = question.category
            content = question.content
            is_multiple_choice = question.is_multiple_choice

            query = """INSERT INTO Question (id, category, content, is_multiple_choice)
                        VALUES (%s, %s, %s, %s)"""
            values = (id, category, content, is_multiple_choice)
            self.cursor.execute(query, values)

            for choice in question.choices:
                self.create_choice(choice)

            if quiz:
                self.create_quizQuestion(quiz_id=quiz, question_id=id)
            
            return True
        except mysql.connector.Error as err:
            print(err)
            return False


    def create_choice(self, choice):
        id = choice.id
        question = choice.question
        content = choice.content
        is_correct = choice.is_correct

        query = """INSERT INTO Choice (id, question, content, is_correct)
                    VALUES (%s, %s, %s, %s)"""
        values = (id, question, content, is_correct)
        self.cursor.execute(query, values)

    def create_quizQuestion(self, quiz_id, question_id):
        query = """INSERT INTO QuizQuestion (quiz, question)
                    VALUES (%s, %s)"""
        values = (quiz_id, question_id)
        self.cursor.execute(query, values)

    def get_by_id(self, id):
        try:
            query = """SELECT * FROM Question WHERE id=(%s)"""
            self.cursor.execute(query, (id,))
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print(err)