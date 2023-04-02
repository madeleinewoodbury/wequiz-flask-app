import mysql.connector
from config import Database

class Quiz:
    def __init__(self, id, title, is_active, created_at):
        self.id = id
        self.title = title
        self.is_active = is_active
        self.created_at = created_at
        self.questions = []
    
    def add_question(self, question):
        self.questions.append(question)

    def __str__(self):
        return f"id: {self.id}\ntitle: {self.title}"
    

class QuizTable(Database):
    def __init__(self):
        super().__init__()
    
    def create(self, id, title):
        try:
            query = """INSERT INTO Quiz (id, title)
                        VALUES (%s, %s)"""
            values = (id, title)
            self.cursor.execute(query, values)
            return True
        except mysql.connector.Error as err:
            print(err)
            return False
        
    def get_by_id(self, id):
        try:
            query = """SELECT * FROM Quiz WHERE id=(%s)"""
            self.cursor.execute(query, (id,))
            result = self.cursor.fetchone()
            quiz = Quiz(*result)
            return quiz
        except mysql.connector.Error as err:
            print(err)
        
    def get_questions(self, quiz):
        try:
            query = """SELECT question FROM QuizQuestion WHERE quiz=(%s)"""
            self.cursor.execute(query, (quiz.id,))
            result = self.cursor.fetchall()
            for question in result:
                quiz.add_question(question[0])

            return True
        except mysql.connector.Error as err:
            print(err)
    