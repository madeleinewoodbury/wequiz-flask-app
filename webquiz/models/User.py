from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from config import Database

class User:
    def __init__(self, id, firstname, lastname, email, password=None, role=None, createdAt=None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.role = role
        self.createdAt = createdAt
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_admin(self):
        return self.role.lower() == 'administrator'
                
    def get_id(self):
        return self.id      # string value
    
    def is_authenticated(self):
        return self.is_authenticated
    
    def is_active(self):
        return self.is_active
    
    def is_anonymous(self):
        return self.is_anonymous


class UserTable(Database):
    def __init__(self):
        super().__init__()
    
    def get_user_by_id(self, id):
        try:
            query = """SELECT id, firstname, lastname, email, password, role, created_at
                       FROM User WHERE id=(%s)"""
            self.cursor.execute(query, (id,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def get_user_by_email(self, email):
        try:
            query = """SELECT id, firstname, lastname, email, password, role, created_at
                       FROM User WHERE email=(%s)"""
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def create(self, user):
         try:
              query = """INSERT INTO User (id, firstname, lastname, email, password)
                         VALUES (%s, %s, %s, %s, %s)"""
              values = (user.id, 
                        user.firstname,
                        user.lastname,
                        user.email,
                        user.password)
              self.cursor.execute(query, values)
              return True
         except mysql.connector.Error as err:
              print(err)
              return False
