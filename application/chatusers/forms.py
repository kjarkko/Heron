from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, ValidationError
from application.chats.models import Chat
from application.users.models import User


def _valid_chat(form, field):
	pass
# 	if chat.query.get(field.data) == None:
# 		raise ValidationError('no such chat')


def _valid_user(form, field):
	pass
# 	if User.query.get(field.data) == None:
# 		raise ValidationError('no such user')


class ChatUserForm(FlaskForm):
	chat_id = IntegerField('chat_id', [_valid_chat])
	user_id = IntegerField('user_id', [_valid_user])
	admin = BooleanField('admin')

	class Meta:
		csrf = False
