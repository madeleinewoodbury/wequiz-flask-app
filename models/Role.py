import mysql.connector
from config import DB_CONFIG

class RoleModel:
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

    def get_all(self):
        try:
            self.cursor.execute("SELECT * FROM Rolle")
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(err)

    def get(self, id):
        try:
            self.cursor.execute("SELECT navn FROM Rolle WHERE id=(%s)", (id,))
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print(err)