from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length

class ChoiceForm(FlaskForm):
    content     = StringField("Svar alternativ", 
                           validators=[DataRequired(), 
                                       Length(min=2, max=45)])
    question_id = HiddenField()
    submit   = SubmitField("Legg til")