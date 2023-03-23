from email.policy import default
from unicodedata import category
from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField,BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class QuestionForm(FlaskForm):
    category  = SelectField("Kategori", 
                           validators=[DataRequired()])
    content   = TextAreaField("Spørsmål", 
                                validators=[DataRequired(),
                                            Length(min=2, max=255)])
    is_multiple_choice  = BooleanField("Flervalgs spørsmål")
    answer    = TextAreaField("Riktig svar",
                             validators=[DataRequired()])
    choices = IntegerField("Antall alternativer",
                           validators=[NumberRange(min=0, max=10)])
    submit    = SubmitField("Lagre Spørsmål")