from random import choice
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, SelectField, TextAreaField, BooleanField, FieldList, FormField, Form
from wtforms.validators import DataRequired, Length

class ChoiceForm(Form):
    content     = TextAreaField("Svar alternativ", validators=[Length(max=255)])
    choice_id = HiddenField()

class QuestionForm(FlaskForm):
    id        = HiddenField()
    category  = SelectField("Kategori",validators=[DataRequired()])
    content   = TextAreaField("Spørsmål", validators=[DataRequired(), Length(min=2, max=255)])
    is_multiple_choice  = BooleanField("Flervalgs spørsmål")
    answer    = TextAreaField("Riktig svar",validators=[DataRequired(),Length(min=2, max=255)])
    choices = FieldList(FormField(ChoiceForm), min_entries=4, max_entries=4)
    submit    = SubmitField("Lagre Spørsmål")


class QuizForm(FlaskForm):
    title     = StringField("Tittel", validators=[DataRequired(), Length(min=2, max=45)])
    submit   = SubmitField("Lag Quiz")