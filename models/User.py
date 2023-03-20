import mysql.connector
from config import DB_CONFIG

class UserModel:
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

    def get_user_by_id(self, id):
        try:
            self.cursor.execute("SELECT * FROM Bruker WHERE id=(%s)", (id,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def get_user_by_email(self, email):
        try:
            self.cursor.execute("SELECT * FROM Bruker WHERE epost=(%s)", (email,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result