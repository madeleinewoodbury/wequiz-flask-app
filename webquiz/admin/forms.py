from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length

class ChoiceForm(FlaskForm):
    content     = StringField("Svar alternativ", 
                           validators=[DataRequired(), 
                                       Length(min=2, max=45)])
    question_id = HiddenField()
    submit   = SubmitField("Legg til")


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


class QuizForm(FlaskForm):
    title     = StringField("Tittel", 
                           validators=[DataRequired(), 
                                       Length(min=2, max=45)])
    submit   = SubmitField("Lag Quiz")