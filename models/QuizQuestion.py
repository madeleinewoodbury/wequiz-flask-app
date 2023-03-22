import mysql.connector
from config import DB_CONFIG

class QuizQuestionModel:
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
    
    def create(self, quiz_id, question_id):
        try:
            query = """INSERT INTO QuizQuestion (quiz, question)
                        VALUES (%s, %s)"""
            values = (quiz_id, question_id)
            self.cursor.execute(query, values)
            return True
        except mysql.connector.Error as err:
            print(err)
            return False
