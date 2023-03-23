import mysql.connector
from config import DB_CONFIG

class CategoryModel:
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

    def get_categories(self):
        try:
            self.cursor.execute("SELECT * FROM Category ORDER BY name DESC")
            result = self.cursor.fetchall()
            choices = [(name[0], name[0]) for name in result]
            return choices
        except mysql.connector.Error as err:
            print(err)
