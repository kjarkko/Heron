from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField


class MessageForm(FlaskForm):

	text = StringField('Text')

	class Meta:
		csrf = False
