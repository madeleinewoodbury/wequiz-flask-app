from werkzeug.security import generate_password_hash, check_password_hash

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
