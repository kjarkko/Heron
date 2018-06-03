from flask_wtf import FlaskForm
from wtforms import StringField


def _valid_name(form, field):  # TODO
	pass


class ChatForm(FlaskForm):
	name = StringField("name", [_valid_name])

	class Meta:
		csrf = False
