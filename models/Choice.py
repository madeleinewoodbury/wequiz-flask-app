import mysql.connector
from config import DB_CONFIG

class ChoiceModel:
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
    
    def create(self, id, question, content, is_correct):
        try:
            query = """INSERT INTO Choice (id, question, content, is_correct)
                        VALUES (%s, %s, %s, %s)"""
            values = (id, question, content, is_correct)
            self.cursor.execute(query, values)
            return True
        except mysql.connector.Error as err:
            print(err)
            return False
