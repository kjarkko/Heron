from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length


class MessageForm(FlaskForm):

	text = StringField('Text', [InputRequired(), Length(min=1, max=2048)])
