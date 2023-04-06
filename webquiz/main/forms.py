from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length

class ChoiceAnswerForm(FlaskForm):
    question_id = HiddenField()
    answer     = RadioField(validators=[DataRequired()])
    submit    = SubmitField("Neste")

class TextAnswerForm(FlaskForm):
    question_id = HiddenField()
    answer   = TextAreaField(validators=[DataRequired(), Length(min=2, max=255)])
    submit    = SubmitField("Neste")

