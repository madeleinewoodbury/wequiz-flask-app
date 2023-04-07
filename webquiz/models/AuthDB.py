import mysql.connector
from config import Database
from webquiz.models.User import User
from uuid import uuid4

class AuthDB(Database):
    def __init__(self):
        super().__init__()
    
    def get_user_by_id(self, id):
        try:
            query = """SELECT id, firstname, lastname, email, password, role, created_at
                       FROM User WHERE id=(%s)"""
            self.cursor.execute(query, (id,))
            result = self.cursor.fetchone()
            user = User(*result)
            return user
        
        except mysql.connector.Error as err:
                print(err)
    
    def get_user_by_email(self, email):
        try:
            query = """SELECT id, firstname, lastname, email, password, role, created_at
                       FROM User WHERE email=(%s)"""
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()
            user = User(*result)
            return user        
        
        except mysql.connector.Error as err:
                print(err)
        except Exception as err:
                print(err)
        
        return None
    
    def user_exist(self, email):
        try:
            query = """SELECT id FROM User WHERE email=(%s)"""
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()
            
            if result:
                 return True

        except mysql.connector.Error as err:
                print(err)
        except Exception as err:
                print(err)
        
        return False

    def create(self, firstname, lastname, email, password):
         try:
              id = str(uuid4())
              user = User(id, firstname, lastname, email)
              user.set_password(password)

              query = """INSERT INTO User (id, firstname, lastname, email, password)
                         VALUES (%s, %s, %s, %s, %s)"""
              
              values = (user.id, 
                        user.firstname,
                        user.lastname,
                        user.email,
                        user.password)
              self.cursor.execute(query, values)
              return user
         except mysql.connector.Error as err:
              print(err)
              return False

    def get_user_roles(self):
        try:
            self.cursor.execute("SELECT * FROM UserRole ORDER BY name DESC")
            result = self.cursor.fetchall()
            return result
        
        except mysql.connector.Error as err:
              print(err)
              return False
