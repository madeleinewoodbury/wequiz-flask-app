from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class QuestionForm(FlaskForm):
    category  = SelectField("Kategori", 
                           validators=[DataRequired()])
    content   = TextAreaField("Spørsmål", 
                                validators=[DataRequired(),
                                            Length(min=2, max=255)])
    is_multiple_choice  = BooleanField("Flervalgs spørsmål")
    answer    = TextAreaField("Riktig svar",
                             validators=[DataRequired()])
    submit    = SubmitField("Lagre Spørsmål")