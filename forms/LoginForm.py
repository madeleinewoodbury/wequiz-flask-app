from flask_wtf import FlaskForm
from wtforms import SelectField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    role     = SelectField("Logg inn som", 
                           validators=[DataRequired()])
    email    = EmailField("Epost", 
                          validators=[DataRequired("Fyll inn epost"), 
                                      Email()])
    password = PasswordField("Passord", 
                             validators=[DataRequired("Fyll inn passord")])
    submit   = SubmitField("Logg inn")