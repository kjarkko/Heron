from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from application.chats.models import Chat
from application.users.models import User
from application.chatusers.models import ChatUser


def _name_in_use(form, field):  # TODO
	q = Chat.query.filter(Chat.name == field.data).first()
	if q is not None:
		raise ValidationError('Name in use')


def _valid_user(form, field):
	usr = User.query.filter(User.username == field.data).first()
	if usr is None:
		raise ValidationError('No such user')


class ChatForm(FlaskForm):
	name = StringField("name", [_name_in_use])

	class Meta:
		csrf = False


class AddUserForm(FlaskForm):
	name = StringField("name", [_valid_user])

	class Meta:
		csrf = False
