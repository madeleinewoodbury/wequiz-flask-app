import mysql.connector
from config import DB_CONFIG

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
    
    def create(self, id, category, content, is_multiple_choice):
        try:
            query = """INSERT INTO Qustion (id, category, content, is_multiple_choice)
                        VALUES (%s, %s, %s, %s)"""
            values = (id, category, content, is_multiple_choice)
            self.cursor.execute(query, values)
            return True
        except mysql.connector.Error as err:
            print(err)
            return False
