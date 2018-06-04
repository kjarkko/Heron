from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from application.chats.models import Chat


def _valid_name(form, field):  # TODO
	q = Chat.query.filter(Chat.name == field.data).first()
	if q is not None:
		raise ValidationError('Name in use')


class ChatForm(FlaskForm):
	name = StringField("name", [_valid_name])

	class Meta:
		csrf = False
