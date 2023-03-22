from unicodedata import category
from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField, HiddenField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length

class QuestionForm(FlaskForm):
    category  = SelectField("Kategori", 
                            choices=[("Alle", "Alle"), ("Databaser", "Databaser")], 
                           validators=[DataRequired()])
    content   = TextAreaField("Spørsmål", 
                                validators=[DataRequired(),
                                            Length(min=8, max=255)])
    is_multiple_choice  = BooleanField("Flervalgs spørsmål")
    answer    = TextAreaField("Riktig svar",
                             validators=[DataRequired()])
    choices = IntegerField("Antall alternativer",
                           validators=[Length(max=10)])
    quiz_id   = HiddenField()
    submit    = SubmitField("Lagre Spørsmål")