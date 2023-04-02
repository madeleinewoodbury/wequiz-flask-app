from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    firstname = StringField("Fornavn", 
                            validators=[DataRequired("Fyll inn fornavn"), 
                                        Length(min=2, max=50)])
    lastname = StringField("Etternavn", 
                            validators=[DataRequired("Fyll inn etternavn"), 
                                        Length(min=2, max=50)])
    email     = EmailField("Epost", 
                           validators=[DataRequired("Fyll inn epost"), 
                                        Email(), 
                                        Length(max=50)])
    password  = PasswordField("Passord", 
                              validators=[DataRequired("Fyll inn passord"), 
                                          Length(min=8, max=32)])
    password2  = PasswordField("Gjenta passord", 
                              validators=[DataRequired("Fyll inn gjenta passord"), 
                                          Length(min=8, max=32)])
    submit    = SubmitField("Opprett bruker")


class LoginForm(FlaskForm):
    role     = SelectField("Logg inn som", 
                           validators=[DataRequired()])
    email    = EmailField("Epost", 
                          validators=[DataRequired("Fyll inn epost"), 
                                      Email()])
    password = PasswordField("Passord", 
                             validators=[DataRequired("Fyll inn passord")])
    submit   = SubmitField("Logg inn")