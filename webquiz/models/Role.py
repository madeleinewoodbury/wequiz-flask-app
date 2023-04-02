import mysql.connector
from config import Database

class RoleTable(Database):
    def __init__(self):
        super().__init__()

    def get_choices(self):
        try:
            self.cursor.execute("SELECT * FROM UserRole ORDER BY name DESC")
            result = self.cursor.fetchall()
            choices = [(role[0], role[0]) for role in result]
            return choices
        except mysql.connector.Error as err:
            print(err)
