from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import InputRequired, Length
from application.chats.models import Chat
from application.users.models import User
from application.chatusers.models import ChatUser


def _name_in_use(form, field):
	if Chat.exists(field.data):
		raise ValidationError('Name in use')


def _valid_user(form, field):
	if not User.exists(field.data):
		raise ValidationError('No such user')


class ChatForm(FlaskForm):
	name = StringField(
		"name",
		[InputRequired(), Length(min=1, max=16), _name_in_use]
	)


class AddUserForm(FlaskForm):
	name = StringField(
		"name",
		[InputRequired(), Length(min=3, max=16), _valid_user]
	)
