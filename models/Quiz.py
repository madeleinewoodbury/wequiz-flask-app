import mysql.connector
from config import DB_CONFIG

class Quiz():
    def __init__(self, id, title, is_active, created_at):
        self.id = id
        self.title = title
        self.is_active = is_active
        self.created_at = created_at
        self.questions = []
    
    def add_question(self, question):
        self.questions.append(question)

class QuizModel:
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
            self.cursor.execute(query, (id,))
            result = self.cursor.fetchall()

            for question in result:
                quiz.add_question(question)

            return quiz.questions
        except mysql.connector.Error as err:
            print*err
    