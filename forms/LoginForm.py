from flask_wtf import FlaskForm
from wtforms import SelectField, EmailField, PasswordField, SubmitField

class LoginForm(FlaskForm):
    role = SelectField("Logg inn som")
    email = EmailField("Epost")
    password = PasswordField("Passord")
    submit = SubmitField("Logg inn")