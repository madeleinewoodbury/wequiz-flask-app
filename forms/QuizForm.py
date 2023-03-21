from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class QuizForm(FlaskForm):
    title     = StringField("Tittel", 
                           validators=[DataRequired(), 
                                       Length(min=2, max=45)])
    submit   = SubmitField("Lag Quiz")