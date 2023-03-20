from werkzeug.security import generate_password_hash, check_password_hash

class User():
    def __init__(self, id, role, first_name, last_name, email, password, created_at):
        self.id = id
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created_at = created_at
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
